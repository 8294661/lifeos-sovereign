# LifeOS · Sovereign

> Your life operating system — your data stays yours.

A **local-first** personal growth app: health, goals, daily records, data analysis, and an AI assistant — all running on your own machine, storing data in your own MySQL, not someone else's cloud.

## Why LifeOS

Most similar products lock your data in a vendor's servers — hard to export, and privacy rests on their word. LifeOS goes the other way:

| Dimension | Typical products | LifeOS |
| --- | --- | --- |
| Data storage | Vendor cloud DB | Your own MySQL |
| Account | Must sign up for a third-party account | No sign-up, works locally |
| Data portability | Limited export, closed formats | Data is plain SQL — export/back up anytime |
| Code | Closed-source black box | Fully open source, auditable |
| Network dependency | Unusable offline | Core features work offline |

**In one line: your data is sovereign — it stays in your hands, not on someone else's server.**

## Features

- 📝 **Daily records** — study / creation / reading / exercise / sleep / mood / energy, one entry for the whole day.
- 🎯 **Goal management** — ultimate → long-term → mid-term → short-term, freely addable, with draggable progress bars.
- 📊 **Data analysis** — 30-day behavior trends (ECharts) plus a goal-progress overview.
- 🤖 **AI assistant** — personalized analysis and suggestions based on your real data.

## About privacy (honest notes)

- Your **raw data** (records, goals, profile) lives only in your local MySQL — never uploaded to any cloud.
- The **AI assistant** optionally sends an **aggregated statistical summary** to DeepSeek's API to generate analysis (skip it and the app stays offline).
- The DeepSeek API key and MySQL password live in your local `.env` (Git-ignored) and never enter the repository.

## Tech stack

Vue 3 · FastAPI · MySQL · ECharts · DeepSeek

## Project structure

```
.
├── backend/
│   ├── main.py       # routes (daily records / goal CRUD / analysis / AI)
│   ├── config.py     # reads config from .env
│   ├── database.py   # MySQL connection
│   ├── stats.py      # data aggregation
│   ├── llm.py        # DeepSeek client
│   └── schema.sql    # database schema
└── frontend/
    └── src/views/    # dashboard / profile / daily / goals / analysis / AI
```

## Quick start

### 1. Database

```sql
CREATE DATABASE lifeos CHARACTER SET utf8mb4;
```

Then import `backend/schema.sql`.

### 2. Backend

```bash
cd backend
python -m venv venv
venv/Scripts/pip install -r requirements.txt   # Windows; use venv/bin/pip on Linux/Mac
cp .env.example .env                            # fill in DEEPSEEK_API_KEY and your MySQL password
venv/Scripts/python -m uvicorn main:app --port 8000
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 .

## Security tips

- Frontend and backend bind to `localhost` by default — local-only. Don't expose them via `--host 0.0.0.0`.
- Set MySQL's `bind-address` to `127.0.0.1` to avoid LAN exposure.

## License

[MIT](LICENSE)

---

## 中文说明

> 你的人生操作系统 —— 数据留在你自己手里。

一个**本地优先（local-first）**的个人成长管理应用：健康、目标、每日记录、数据分析、AI 助手，全部跑在你自己的机器上，数据存进你自己的 MySQL，而不是任何人的云。

### 为什么选它

大多数同类产品把你的数据锁在别人的服务器里——想导出难、隐私靠对方一句话。LifeOS 走的是另一条路：

| 维度 | 常见产品 | LifeOS |
| --- | --- | --- |
| 数据存储 | 厂商云数据库 | 你自己的 MySQL |
| 账号 | 必须注册第三方账号 | 无需注册，本地即用 |
| 数据迁移 | 导出受限、格式封闭 | 数据就是 SQL，想导出导出、想备份备份 |
| 代码 | 闭源黑盒 | 完全开源，可审计 |
| 联网依赖 | 断网不可用 | 核心功能断网也能跑 |

**一句话：你的数据主权，在你手里，不在别人的服务器上。**

### 功能

- 📝 **每日记录**：学习 / 创作 / 阅读 / 运动 / 睡眠 / 心情 / 能量，一条记录全天状态。
- 🎯 **目标管理**：终极 → 长期 → 中期 → 短期，层层拆解、自由添加、进度条随手拖。
- 📊 **数据分析**：近 30 天行为趋势可视化（ECharts）+ 目标进度一览。
- 🤖 **AI 助手**：基于你的真实数据做个性化分析与建议。

### 关于隐私（诚实说明）

- 你的**原始数据**（记录、目标、档案）只存本机 MySQL，不上传任何云。
- 使用 **AI 助手**时，后端会把**聚合后的统计摘要**发给 DeepSeek 的 API 生成分析（可选功能，不用它就不联网）。
- DeepSeek API 密钥和 MySQL 密码都保存在本地 `.env`（已被 Git 忽略），不会进仓库。

### 技术栈

Vue 3 · FastAPI · MySQL · ECharts · DeepSeek

### 快速开始

#### 1. 数据库

```sql
CREATE DATABASE lifeos CHARACTER SET utf8mb4;
```

然后导入 `backend/schema.sql`。

#### 2. 后端

```bash
cd backend
python -m venv venv
venv/Scripts/pip install -r requirements.txt     # Windows；Linux/Mac 用 venv/bin/pip
cp .env.example .env                              # 填上你的 DEEPSEEK_API_KEY 和 MySQL 密码
venv/Scripts/python -m uvicorn main:app --port 8000
```

#### 3. 前端

```bash
cd frontend
npm install
npm run dev
```

浏览器打开 http://localhost:5173 。

### 安全提示

- 前后端默认只绑定 `localhost`，仅本机可访问；别用 `--host 0.0.0.0` 暴露到公网。
- 把 MySQL 的 `bind-address` 设为 `127.0.0.1`，避免局域网暴露。

### License

[MIT](LICENSE)
