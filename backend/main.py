from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import db
from datetime import date, timedelta

from stats import build_user_context, format_context
from llm import chat

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "LifeOS Backend is running!"}


@app.get("/api/daily-records")
def get_daily_records():

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM daily_records"
    )

    records = cursor.fetchall()

    cursor.close()

    return records

@app.post("/api/daily-records")
def create_daily_record(data: dict):

    cursor = db.cursor()

    sql = """
    INSERT INTO daily_records
    (
        user_id,
        record_date,
        study_minutes,
        creation_minutes,
        reading_minutes,
        exercise_minutes,
        sleep_hours,
        mood_score,
        energy_score,
        summary
    )
    VALUES
    (
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s
    )
    """

    values = (
        data["user_id"],
        data["record_date"],
        data["study_minutes"],
        data["creation_minutes"],
        data["reading_minutes"],
        data["exercise_minutes"],
        data["sleep_hours"],
        data["mood_score"],
        data["energy_score"],
        data["summary"]
    )


    cursor.execute(sql, values)

    db.commit()

    cursor.close()


    return {
        "message":"记录创建成功"
    }


@app.delete("/api/daily-records/{record_id}")
def delete_daily_record(record_id: int):

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM daily_records WHERE id=%s",
        (record_id,)
    )

    db.commit()

    cursor.close()

    return {"message": "记录删除成功"}


@app.get("/api/dashboard")
def get_dashboard():

    cursor = db.cursor(dictionary=True)

    # 今日记录
    cursor.execute(
        """
        SELECT *
        FROM daily_records
        WHERE user_id=1 AND record_date=CURDATE()
        ORDER BY id DESC
        LIMIT 1
        """
    )
    today = cursor.fetchone()

    # 累计统计
    cursor.execute(
        """
        SELECT
            COUNT(*)              AS total_days,
            SUM(study_minutes)    AS total_study,
            SUM(creation_minutes) AS total_creation,
            SUM(reading_minutes)  AS total_reading,
            SUM(exercise_minutes) AS total_exercise,
            AVG(sleep_hours)      AS avg_sleep,
            AVG(mood_score)       AS avg_mood,
            AVG(energy_score)     AS avg_energy
        FROM daily_records
        WHERE user_id=1
        """
    )
    overall = cursor.fetchone()

    # 目标统计
    cursor.execute(
        """
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN status='in_progress' THEN 1 ELSE 0 END) AS in_progress
        FROM goals
        WHERE user_id=1
        """
    )
    goals = cursor.fetchone()

    cursor.close()

    return {
        "today": today,
        "overall": overall,
        "goals": goals
    }

@app.get("/api/profile/{user_id}")
def get_profile(user_id:int):

    cursor = db.cursor(dictionary=True)


    # 查询个人信息
    cursor.execute(
        """
        SELECT *
        FROM personal_info
        WHERE user_id=%s
        """,
        (user_id,)
    )

    personal = cursor.fetchone()


    # 查询健康信息
    cursor.execute(
        """
        SELECT *
        FROM health_profile
        WHERE user_id=%s
        """,
        (user_id,)
    )

    health = cursor.fetchone()


    cursor.close()


    return {
        "personal_info": personal,
        "health_profile": health
    }


@app.put("/api/profile/{user_id}")
def update_profile(user_id: int, data: dict):

    cursor = db.cursor(dictionary=True)

    # 基础信息（身高体重）：有则更新，无则插入
    cursor.execute(
        "SELECT id FROM personal_info WHERE user_id=%s",
        (user_id,)
    )
    exists = cursor.fetchone()

    if exists:
        cursor.execute(
            """
            UPDATE personal_info
            SET height=%s, current_weight=%s
            WHERE user_id=%s
            """,
            (data.get("height"), data.get("current_weight"), user_id)
        )
    else:
        cursor.execute(
            """
            INSERT INTO personal_info (user_id, height, current_weight)
            VALUES (%s, %s, %s)
            """,
            (user_id, data.get("height"), data.get("current_weight"))
        )

    # 健康档案：有则更新，无则插入
    cursor.execute(
        "SELECT id FROM health_profile WHERE user_id=%s",
        (user_id,)
    )
    exists = cursor.fetchone()

    if exists:
        cursor.execute(
            """
            UPDATE health_profile
            SET blood_type=%s, allergies=%s, health_status=%s,
                exercise_habit=%s, description=%s
            WHERE user_id=%s
            """,
            (
                data.get("blood_type"),
                data.get("allergies"),
                data.get("health_status"),
                data.get("exercise_habit"),
                data.get("description"),
                user_id
            )
        )
    else:
        cursor.execute(
            """
            INSERT INTO health_profile
            (user_id, blood_type, allergies, health_status, exercise_habit, description)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                user_id,
                data.get("blood_type"),
                data.get("allergies"),
                data.get("health_status"),
                data.get("exercise_habit"),
                data.get("description")
            )
        )

    db.commit()

    cursor.close()

    return {"message": "档案更新成功"}

# ---------- 目标 CRUD ----------

GOAL_TYPES = ("ultimate", "long_term", "mid_term", "short_term")


@app.get("/api/goals")
def get_goals(user_id: int = 1):
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, user_id, parent_goal_id, title, description, goal_type, "
        "priority, progess, status, start_date, deadline, created_at "
        "FROM goals WHERE user_id=%s ORDER BY priority, id",
        (user_id,),
    )
    rows = cursor.fetchall()
    cursor.close()
    # DB 列 progess → API 字段 progress
    for r in rows:
        r["progress"] = float(r.pop("progess") or 0)
        if r.get("deadline") is not None:
            r["deadline"] = str(r["deadline"])
    return rows


@app.post("/api/goals")
def create_goal(data: dict):
    title = data.get("title")
    if not title:
        raise HTTPException(status_code=400, detail="标题不能为空")
    goal_type = data.get("goal_type", "short_term")
    if goal_type not in GOAL_TYPES:
        raise HTTPException(status_code=400, detail="目标类型不合法")
    deadline = data.get("deadline") or None
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO goals
        (user_id, parent_goal_id, title, description, goal_type, priority, progess, status, deadline)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            data.get("user_id", 1),
            data.get("parent_goal_id"),
            title,
            data.get("description"),
            goal_type,
            data.get("priority", 3),
            data.get("progress", 0),
            data.get("status", "in_progress"),
            deadline,
        ),
    )
    new_id = cursor.lastrowid
    cursor.close()
    return {"message": "目标创建成功", "id": new_id}


@app.put("/api/goals/{goal_id}")
def update_goal(goal_id: int, data: dict):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id FROM goals WHERE id=%s", (goal_id,))
    if not cursor.fetchone():
        cursor.close()
        raise HTTPException(status_code=404, detail="目标不存在")
    mapping = {
        "title": "title",
        "description": "description",
        "goal_type": "goal_type",
        "priority": "priority",
        "progress": "progess",
        "status": "status",
        "deadline": "deadline",
    }
    fields, values = [], []
    for key, col in mapping.items():
        if key in data:
            val = data[key]
            if key == "goal_type" and val not in GOAL_TYPES:
                cursor.close()
                raise HTTPException(status_code=400, detail="目标类型不合法")
            if key == "deadline":
                val = val or None
            fields.append(f"{col}=%s")
            values.append(val)
    if not fields:
        cursor.close()
        raise HTTPException(status_code=400, detail="没有可更新的字段")
    values.append(goal_id)
    cursor.execute(f"UPDATE goals SET {', '.join(fields)} WHERE id=%s", values)
    cursor.close()
    return {"message": "目标更新成功"}


@app.delete("/api/goals/{goal_id}")
def delete_goal(goal_id: int):
    cursor = db.cursor()
    # 先解除子目标关联，再删除（parent_goal_id 外键默认 RESTRICT）
    cursor.execute("UPDATE goals SET parent_goal_id=NULL WHERE parent_goal_id=%s", (goal_id,))
    cursor.execute("DELETE FROM goals WHERE id=%s", (goal_id,))
    affected = cursor.rowcount
    cursor.close()
    if affected == 0:
        raise HTTPException(status_code=404, detail="目标不存在")
    return {"message": "目标删除成功"}

@app.get("/api/ai/analyze")
def ai_analyze():

    cursor = db.cursor(dictionary=True)


    cursor.execute(
        """
        SELECT 
            AVG(study_minutes) as avg_study,
            AVG(creation_minutes) as avg_creation,
            AVG(sleep_hours) as avg_sleep,
            AVG(mood_score) as avg_mood,
            AVG(energy_score) as avg_energy
        FROM daily_records
        """
    )


    data = cursor.fetchone()


    cursor.close()


    return {

        "analysis":

        f"""
        根据你的LifeOS记录：

        📚 平均学习时间：
        {round(data['avg_study'],1)} 分钟

        🎨 平均创作时间：
        {round(data['avg_creation'],1)} 分钟

        😴 平均睡眠：
        {round(data['avg_sleep'],1)} 小时

        😃 平均心情：
        {round(data['avg_mood'],1)} 分

        ⚡ 平均能量：
        {round(data['avg_energy'],1)} 分


        建议：
        保持当前学习节奏，
        继续关注睡眠和运动平衡。
        """
    }

@app.get("/api/analysis")
def get_analysis(days: int = 30):

    cursor = db.cursor(dictionary=True)

    cutoff = date.today() - timedelta(days=days)

    cursor.execute(
        """
        SELECT
            record_date,
            study_minutes,
            creation_minutes,
            reading_minutes,
            exercise_minutes,
            sleep_hours,
            mood_score,
            energy_score
        FROM daily_records
        WHERE user_id=1 AND record_date >= %s
        ORDER BY record_date
        """,
        (cutoff,)
    )

    records = cursor.fetchall()

    cursor.close()

    return records


@app.post("/api/ai/chat")
def ai_chat(data: dict):

    user_id = data.get("user_id", 1)

    # 只保留合法的 user / assistant 消息，并过滤空内容
    history = [
        {"role": m.get("role"), "content": m.get("content", "")}
        for m in data.get("messages", [])
        if m.get("role") in ("user", "assistant") and m.get("content")
    ]

    # 1. 聚合用户私有数据，拼进 system 提示词
    stats = build_user_context(user_id)
    context_text = format_context(stats)

    system_prompt = (
        "你是 LifeOS 的个人 AI 助手，基于用户的私有数据做个性化状态分析与建议。\n\n"
        "【用户私有数据】\n"
        + context_text
        + "\n\n【要求】\n"
        "- 用中文、亲切自然的语气回答\n"
        "- 分析必须基于上述真实数据，不要编造数字或事实\n"
        "- 结合用户的目标给出可执行的建议\n"
        "- 如果某项数据不足，如实说明并建议用户补充每日记录"
    )

    messages = [{"role": "system", "content": system_prompt}] + history

    # 2. 调用 DeepSeek
    try:
        reply = chat(messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI 调用失败：{e}")

    return {"reply": reply}