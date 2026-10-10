<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API = 'http://127.0.0.1:8000'

const data = ref({ today: null, overall: null, goals: null })

const fmt = (v) => (v == null ? '—' : v)

onMounted(async () => {
    try {
        const res = await axios.get(`${API}/api/dashboard`)
        data.value = res.data
    } catch (e) {
        console.error(e)
    }
})
</script>

<template>
<div>
    <h1>🏠 首页</h1>
    <p class="subtitle">LifeOS 个人成长管理面板</p>

    <div class="cards">
        <div class="card">
            <div class="label">累计记录</div>
            <div class="value">{{ fmt(data.overall?.total_days) }} <span>天</span></div>
        </div>
        <div class="card">
            <div class="label">累计学习</div>
            <div class="value">{{ fmt(data.overall?.total_study) }} <span>分钟</span></div>
        </div>
        <div class="card">
            <div class="label">累计创作</div>
            <div class="value">{{ fmt(data.overall?.total_creation) }} <span>分钟</span></div>
        </div>
        <div class="card">
            <div class="label">平均睡眠</div>
            <div class="value">{{ fmt(data.overall?.avg_sleep) }} <span>小时</span></div>
        </div>
        <div class="card">
            <div class="label">平均心情</div>
            <div class="value">{{ fmt(data.overall?.avg_mood) }} <span>/ 10</span></div>
        </div>
        <div class="card">
            <div class="label">平均能量</div>
            <div class="value">{{ fmt(data.overall?.avg_energy) }} <span>/ 10</span></div>
        </div>
    </div>

    <h2>📅 今日打卡</h2>
    <div v-if="data.today" class="today">
        <div class="today-grid">
            <div>📚 学习 <b>{{ data.today.study_minutes }} 分钟</b></div>
            <div>🎨 创作 <b>{{ data.today.creation_minutes }} 分钟</b></div>
            <div>📖 阅读 <b>{{ data.today.reading_minutes }} 分钟</b></div>
            <div>🏃 运动 <b>{{ data.today.exercise_minutes }} 分钟</b></div>
            <div>😴 睡眠 <b>{{ data.today.sleep_hours }} 小时</b></div>
            <div>😃 心情 <b>{{ data.today.mood_score }}</b></div>
            <div>⚡ 能量 <b>{{ data.today.energy_score }}</b></div>
        </div>
        <p v-if="data.today.summary" class="summary">📝 {{ data.today.summary }}</p>
    </div>
    <div v-else class="empty">
        今天还没有打卡，去「<router-link to="/daily">每日记录</router-link>」填写吧～
    </div>

    <h2>🎯 目标进度</h2>
    <div class="cards">
        <div class="card">
            <div class="label">目标总数</div>
            <div class="value">{{ fmt(data.goals?.total) }} <span>个</span></div>
        </div>
        <div class="card">
            <div class="label">进行中</div>
            <div class="value">{{ fmt(data.goals?.in_progress) }} <span>个</span></div>
        </div>
    </div>
</div>
</template>

<style>
.subtitle { color: #6b7280; margin-top: -8px; margin-bottom: 20px; }

.cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 16px;
    margin-bottom: 8px;
}

.card {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 18px 20px;
}

.card .label { color: #6b7280; font-size: 13px; margin-bottom: 6px; }
.card .value { font-size: 28px; font-weight: 700; color: #1f2937; }
.card .value span { font-size: 13px; font-weight: 400; color: #6b7280; }

.today {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 20px;
}

.today-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 12px;
}

.today-grid div { color: #4b5563; }
.today-grid b { color: #1f2937; }
.summary { margin-top: 16px; color: #4b5563; }

.empty {
    color: #9ca3af;
    padding: 20px;
    background: #fff;
    border: 1px dashed #d1d5db;
    border-radius: 12px;
}

h2 { margin: 24px 0 12px; }
</style>
