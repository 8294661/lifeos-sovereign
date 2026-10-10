from datetime import date

from database import db


def _num(v, nd=1):
    """把 DB 返回的值转成 round 后的 float；None 保持 None。"""
    if v is None:
        return None
    return round(float(v), nd)


def build_user_context(user_id=1):
    """从 MySQL 聚合用户私有数据，返回结构化统计 dict。"""
    cursor = db.cursor(dictionary=True)

    # 1. 用户基础信息
    cursor.execute(
        "SELECT username, gender, birthday FROM user WHERE id=%s", (user_id,)
    )
    user = cursor.fetchone() or {}

    cursor.execute(
        "SELECT height, current_weight FROM personal_info WHERE user_id=%s", (user_id,)
    )
    personal = cursor.fetchone() or {}

    cursor.execute(
        "SELECT blood_type, allergies, health_status, exercise_habit "
        "FROM health_profile WHERE user_id=%s",
        (user_id,),
    )
    health = cursor.fetchone() or {}

    # 2. 每日记录统计
    cursor.execute(
        """
        SELECT
            COUNT(*)              AS total_days,
            MIN(record_date)      AS first_date,
            MAX(record_date)      AS last_date,
            AVG(study_minutes)    AS avg_study,
            AVG(creation_minutes) AS avg_creation,
            AVG(reading_minutes)  AS avg_reading,
            AVG(exercise_minutes) AS avg_exercise,
            AVG(sleep_hours)      AS avg_sleep,
            AVG(mood_score)       AS avg_mood,
            AVG(energy_score)     AS avg_energy
        FROM daily_records
        WHERE user_id=%s
        """,
        (user_id,),
    )
    rec = cursor.fetchone() or {}

    cursor.execute(
        "SELECT summary FROM daily_records WHERE user_id=%s "
        "ORDER BY record_date DESC LIMIT 1",
        (user_id,),
    )
    latest = cursor.fetchone()

    # 3. 目标列表
    cursor.execute(
        "SELECT title, goal_type, progess, status, deadline "
        "FROM goals WHERE user_id=%s ORDER BY priority, id",
        (user_id,),
    )
    goals = cursor.fetchall() or []

    # 4. 家人（轻量，仅用于语气参考）
    cursor.execute(
        "SELECT name, relationship FROM family_members WHERE user_id=%s", (user_id,)
    )
    family = cursor.fetchall() or []

    cursor.close()

    # 计算年龄 / BMI
    age = None
    if user.get("birthday"):
        b = user["birthday"]
        today = date.today()
        age = today.year - b.year - ((today.month, today.day) < (b.month, b.day))

    bmi = None
    h = personal.get("height")
    w = personal.get("current_weight")
    if h and w:
        bmi = _num(float(w) / ((float(h) / 100) ** 2), 1)

    return {
        "profile": {
            "username": user.get("username"),
            "gender": user.get("gender"),
            "age": age,
            "height": _num(personal.get("height")),
            "weight": _num(personal.get("current_weight")),
            "bmi": bmi,
            "blood_type": health.get("blood_type"),
            "allergies": health.get("allergies"),
            "health_status": health.get("health_status"),
            "exercise_habit": health.get("exercise_habit"),
        },
        "records": {
            "total_days": rec.get("total_days"),
            "first_date": str(rec["first_date"]) if rec.get("first_date") else None,
            "last_date": str(rec["last_date"]) if rec.get("last_date") else None,
            "avg_study": _num(rec.get("avg_study"), 0),
            "avg_creation": _num(rec.get("avg_creation"), 0),
            "avg_reading": _num(rec.get("avg_reading"), 0),
            "avg_exercise": _num(rec.get("avg_exercise"), 0),
            "avg_sleep": _num(rec.get("avg_sleep"), 1),
            "avg_mood": _num(rec.get("avg_mood"), 1),
            "avg_energy": _num(rec.get("avg_energy"), 1),
            "latest_summary": latest["summary"] if latest else None,
        },
        "goals": [
            {
                "title": g.get("title"),
                "type": g.get("goal_type"),
                "progress": _num(g.get("progess"), 1),
                "status": g.get("status"),
                "deadline": str(g["deadline"]) if g.get("deadline") else None,
            }
            for g in goals
        ],
        "family": [
            {"name": f.get("name"), "relationship": f.get("relationship")}
            for f in family
        ],
    }


def _fmt(v):
    return "未知" if v is None else f"{v:g}"


def format_context(stats):
    """把统计 dict 渲染成给大模型读的中文文本块。"""
    p = stats["profile"]
    r = stats["records"]
    lines = []

    lines.append("【基本信息】")
    lines.append(
        f"姓名：{p.get('username') or '未知'}，性别：{p.get('gender') or '未知'}，"
        f"年龄：{_fmt(p.get('age'))} 岁"
    )
    lines.append(
        f"身高：{_fmt(p.get('height'))} cm，体重：{_fmt(p.get('weight'))} kg，"
        f"BMI：{_fmt(p.get('bmi'))}"
    )
    lines.append(
        f"血型：{p.get('blood_type') or '未知'}，健康状况：{p.get('health_status') or '未填写'}，"
        f"运动习惯：{p.get('exercise_habit') or '未填写'}"
    )
    if p.get("allergies"):
        lines.append(f"过敏史：{p['allergies']}")

    lines.append("")
    lines.append("【每日记录统计】")
    if r.get("total_days"):
        lines.append(f"共记录 {r['total_days']} 天（{r['first_date']} ~ {r['last_date']}）")
        lines.append(
            f"平均每天：学习 {_fmt(r['avg_study'])} 分钟、创作 {_fmt(r['avg_creation'])} 分钟、"
            f"阅读 {_fmt(r['avg_reading'])} 分钟、运动 {_fmt(r['avg_exercise'])} 分钟、"
            f"睡眠 {_fmt(r['avg_sleep'])} 小时"
        )
        lines.append(f"平均心情 {_fmt(r['avg_mood'])} / 10，平均能量 {_fmt(r['avg_energy'])} / 10")
        if r.get("latest_summary"):
            lines.append(f"最近一次记录总结：{r['latest_summary']}")
    else:
        lines.append("暂无每日记录数据")

    lines.append("")
    lines.append("【目标】")
    if stats["goals"]:
        for g in stats["goals"]:
            dl = f"，截止 {g['deadline']}" if g.get("deadline") else ""
            lines.append(
                f"- {g['title']}（类型：{g['type']}，进度：{_fmt(g['progress'])}%，"
                f"状态：{g['status']}{dl}）"
            )
    else:
        lines.append("暂无目标")

    if stats["family"]:
        lines.append("")
        lines.append("【家人】")
        for f in stats["family"]:
            lines.append(f"- {f['name']}（{f['relationship']}）")

    return "\n".join(lines)
