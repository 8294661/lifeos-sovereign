<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API = 'http://127.0.0.1:8000'

const form = ref({
    user_id: 1,
    record_date: new Date().toISOString().slice(0, 10),
    study_minutes: 0,
    creation_minutes: 0,
    reading_minutes: 0,
    exercise_minutes: 0,
    sleep_hours: 0,
    mood_score: 0,
    energy_score: 0,
    summary: '',
})

const records = ref([])
const goals = ref([])

const loadRecords = async () => {
    try {
        const res = await axios.get(`${API}/api/daily-records`)
        records.value = res.data
    } catch (e) {
        console.error(e)
    }
}

const loadGoals = async () => {
    try {
        const res = await axios.get(`${API}/api/goals`)
        goals.value = res.data
    } catch (e) {
        console.error(e)
    }
}

const submitRecord = async () => {
    try {
        await axios.post(`${API}/api/daily-records`, form.value)
        alert('记录保存成功')
        await loadRecords()
    } catch (e) {
        alert('保存失败：' + (e.response?.data?.detail || e.message))
    }
}

const deleteRecord = async (id) => {
    if (!confirm('确定删除这条记录吗？')) return
    try {
        await axios.delete(`${API}/api/daily-records/${id}`)
        await loadRecords()
    } catch (e) {
        alert('删除失败：' + (e.response?.data?.detail || e.message))
    }
}

const setGoalProgress = async (g, val) => {
    g.progress = val
    try {
        await axios.put(`${API}/api/goals/${g.id}`, { progress: val })
    } catch (e) {
        alert('更新失败：' + (e.response?.data?.detail || e.message))
    }
}

onMounted(() => {
    loadRecords()
    loadGoals()
})
</script>

<template>
<div>
    <h1>📝 每日记录</h1>

    <div class="form">
        <label>学习时间 (分钟)</label>
        <input v-model.number="form.study_minutes" type="number">

        <label>创作时间 (分钟)</label>
        <input v-model.number="form.creation_minutes" type="number">

        <label>阅读 (分钟)</label>
        <input v-model.number="form.reading_minutes" type="number">

        <label>运动 (分钟)</label>
        <input v-model.number="form.exercise_minutes" type="number">

        <label>睡眠 (小时)</label>
        <input v-model.number="form.sleep_hours" type="number" step="0.1">

        <label>心情 (0-10)</label>
        <input v-model.number="form.mood_score" type="number" min="0" max="10">

        <label>能量 (0-10)</label>
        <input v-model.number="form.energy_score" type="number" min="0" max="10">

        <label>总结</label>
        <textarea v-model="form.summary"></textarea>

        <button @click="submitRecord">保存记录</button>
    </div>

    <h2>🎯 目标进度</h2>
    <div v-if="goals.length" class="goals">
        <div v-for="g in goals" :key="g.id" class="goal">
            <span class="goal-title">{{ g.title }}</span>
            <div class="bar"><div class="fill" :style="{ width: (g.progress || 0) + '%' }"></div></div>
            <span class="pct">{{ g.progress || 0 }}%</span>
            <input type="range" min="0" max="100" :value="g.progress || 0"
                   @change="setGoalProgress(g, Number($event.target.value))">
        </div>
    </div>
    <div v-else class="empty">暂无目标，去「<router-link to="/goals">目标</router-link>」添加</div>

    <h2>📋 历史记录</h2>
    <div v-if="records.length" class="list">
        <div v-for="r in records" :key="r.id" class="row">
            <div class="row-main">
                <div class="date">{{ r.record_date }}</div>
                <div class="metrics">
                    学习 {{ r.study_minutes }}m · 创作 {{ r.creation_minutes }}m ·
                    阅读 {{ r.reading_minutes }}m · 运动 {{ r.exercise_minutes }}m ·
                    睡眠 {{ r.sleep_hours }}h · 心情 {{ r.mood_score }} · 能量 {{ r.energy_score }}
                </div>
                <div v-if="r.summary" class="summary">📝 {{ r.summary }}</div>
            </div>
            <button class="del" @click="deleteRecord(r.id)">删除</button>
        </div>
    </div>
    <div v-else class="empty">暂无记录</div>
</div>
</template>

<style>
.form {
    display: flex;
    flex-direction: column;
    width: 420px;
    gap: 10px;
}

input, textarea {
    padding: 8px;
    border: 1px solid #d1d5db;
    border-radius: 6px;
}

.form button {
    margin-top: 12px;
    padding: 10px;
    background: #2563eb;
    color: #fff;
    border: none;
    border-radius: 6px;
    cursor: pointer;
}

h2 { margin: 32px 0 12px; }

.goals { display: flex; flex-direction: column; gap: 10px; max-width: 560px; }

.goal {
    display: flex;
    align-items: center;
    gap: 12px;
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 10px 14px;
}

.goal-title { font-weight: 600; color: #1f2937; white-space: nowrap; }

.bar { flex: 1; height: 8px; background: #e5e7eb; border-radius: 999px; overflow: hidden; }

.fill { height: 100%; background: #2563eb; border-radius: 999px; }

.pct { font-size: 13px; color: #374151; font-weight: 600; min-width: 40px; text-align: right; }

.goal input[type="range"] { width: 120px; }

.list { display: flex; flex-direction: column; gap: 12px; }

.row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 16px 20px;
}

.row-main { flex: 1; }
.date { font-weight: 700; color: #1f2937; margin-bottom: 4px; }
.metrics { color: #6b7280; font-size: 14px; }
.summary { color: #4b5563; margin-top: 6px; font-size: 14px; }

.del {
    background: #fee2e2;
    color: #dc2626;
    border: none;
    border-radius: 6px;
    padding: 8px 14px;
    cursor: pointer;
}

.empty { color: #9ca3af; padding: 20px; background: #fff; border: 1px dashed #d1d5db; border-radius: 12px; }
</style>
