<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts'
import { GOAL_TYPE_LABEL } from '../goalMeta'

const API = 'http://127.0.0.1:8000'

const records = ref([])
const goals = ref([])
const loading = ref(true)

const el1 = ref(null)
const el2 = ref(null)
const el3 = ref(null)

let charts = []

// 验证过的分类配色（dataviz 参考色板）
const COLORS = {
    study: '#2a78d6',
    creation: '#eb6834',
    reading: '#1baf7a',
    exercise: '#eda100',
    sleep: '#4a3aa7',
    mood: '#e87ba4',
    energy: '#008300',
}

const INK = {
    axis: '#898781',
    axisLine: '#c3c2b7',
    split: '#e1e0d9',
    legend: '#52514e',
}

const stats = computed(() => {
    const rs = records.value
    if (!rs.length) return null
    const avg = (key) => (rs.reduce((s, r) => s + (r[key] ?? 0), 0) / rs.length).toFixed(1)
    return {
        days: rs.length,
        study: avg('study_minutes'),
        sleep: avg('sleep_hours'),
        mood: avg('mood_score'),
    }
})

function makeLine(data, name, color) {
    return {
        name,
        type: 'line',
        smooth: true,
        data,
        symbol: 'circle',
        symbolSize: 6,
        lineStyle: { width: 2, color },
        itemStyle: { color },
    }
}

function baseOption(xData, yName) {
    return {
        tooltip: { trigger: 'axis' },
        grid: { left: 56, right: 20, top: 48, bottom: 32 },
        xAxis: {
            type: 'category',
            data: xData,
            axisLine: { lineStyle: { color: INK.axisLine } },
            axisTick: { show: false },
            axisLabel: { color: INK.axis },
        },
        yAxis: {
            type: 'value',
            name: yName,
            nameTextStyle: { color: INK.legend },
            splitLine: { lineStyle: { color: INK.split } },
            axisLabel: { color: INK.axis },
        },
    }
}

function renderCharts() {
    const dates = records.value.map((r) => r.record_date)
    const col = (key) => records.value.map((r) => r[key])

    const c1 = echarts.init(el1.value)
    c1.setOption({
        ...baseOption(dates, '分钟'),
        legend: { data: ['学习', '创作', '阅读', '运动'], textStyle: { color: INK.legend } },
        series: [
            makeLine(col('study_minutes'), '学习', COLORS.study),
            makeLine(col('creation_minutes'), '创作', COLORS.creation),
            makeLine(col('reading_minutes'), '阅读', COLORS.reading),
            makeLine(col('exercise_minutes'), '运动', COLORS.exercise),
        ],
    })

    const c2 = echarts.init(el2.value)
    c2.setOption({
        ...baseOption(dates, '小时'),
        series: [makeLine(col('sleep_hours'), '睡眠', COLORS.sleep)],
    })

    const c3 = echarts.init(el3.value)
    c3.setOption({
        ...baseOption(dates, '分'),
        legend: { data: ['心情', '能量'], textStyle: { color: INK.legend } },
        yAxis: {
            type: 'value',
            name: '分',
            min: 0,
            max: 10,
            nameTextStyle: { color: INK.legend },
            splitLine: { lineStyle: { color: INK.split } },
            axisLabel: { color: INK.axis },
        },
        series: [
            makeLine(col('mood_score'), '心情', COLORS.mood),
            makeLine(col('energy_score'), '能量', COLORS.energy),
        ],
    })

    charts = [c1, c2, c3]
}

function onResize() {
    charts.forEach((c) => c && c.resize())
}

onMounted(async () => {
    try {
        const res = await axios.get(`${API}/api/analysis?days=30`)
        records.value = res.data
        renderCharts()
        const gres = await axios.get(`${API}/api/goals`)
        goals.value = gres.data
    } catch (e) {
        console.error(e)
    } finally {
        loading.value = false
    }
    window.addEventListener('resize', onResize)
})

onBeforeUnmount(() => {
    window.removeEventListener('resize', onResize)
    charts.forEach((c) => c && c.dispose())
})
</script>

<template>
<div>
    <h1>📊 数据分析</h1>
    <p class="subtitle">近 30 天个人行为数据趋势</p>

    <div v-if="stats" class="stat-row">
        <div class="stat"><div class="lbl">统计天数</div><div class="val">{{ stats.days }}</div></div>
        <div class="stat"><div class="lbl">日均学习</div><div class="val">{{ stats.study }}<span> 分钟</span></div></div>
        <div class="stat"><div class="lbl">日均睡眠</div><div class="val">{{ stats.sleep }}<span> 小时</span></div></div>
        <div class="stat"><div class="lbl">平均心情</div><div class="val">{{ stats.mood }}<span> / 10</span></div></div>
    </div>

    <div class="chart-box">
        <div class="chart-title">学习 / 创作 / 阅读 / 运动（分钟）</div>
        <div ref="el1" class="chart"></div>
    </div>
    <div class="chart-box">
        <div class="chart-title">睡眠时长（小时）</div>
        <div ref="el2" class="chart"></div>
    </div>
    <div class="chart-box">
        <div class="chart-title">心情 / 能量（0-10 分）</div>
        <div ref="el3" class="chart"></div>
    </div>

    <h2>🎯 目标进度</h2>
    <div v-if="goals.length" class="goal-list">
        <div v-for="g in goals" :key="g.id" class="goal">
            <div class="goal-head">
                <span class="goal-title">{{ g.title }}</span>
                <span class="goal-type">{{ GOAL_TYPE_LABEL[g.goal_type] || g.goal_type }}</span>
                <span v-if="g.deadline" class="goal-deadline">截止 {{ g.deadline }}</span>
            </div>
            <div class="goal-bar">
                <div class="goal-fill" :style="{ width: (g.progress || 0) + '%' }"></div>
            </div>
            <span class="goal-pct">{{ g.progress || 0 }}%</span>
        </div>
    </div>
    <div v-else class="empty">暂无目标，去「<router-link to="/goals">目标</router-link>」添加</div>
</div>
</template>

<style>
.subtitle { color: #6b7280; margin-top: -8px; margin-bottom: 20px; }

.stat-row {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 16px;
    margin-bottom: 20px;
}

.stat {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 18px 20px;
}

.stat .lbl { color: #6b7280; font-size: 13px; margin-bottom: 6px; }
.stat .val { font-size: 26px; font-weight: 700; color: #1f2937; }
.stat .val span { font-size: 13px; font-weight: 400; color: #6b7280; }

.chart-box {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
}

.chart-title {
    font-size: 15px;
    font-weight: 600;
    color: #374151;
    margin-bottom: 8px;
}

.chart { width: 100%; height: 320px; }

h2 { margin: 24px 0 12px; }

.goal-list { display: flex; flex-direction: column; gap: 12px; }

.goal {
    display: flex;
    align-items: center;
    gap: 12px;
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 14px 20px;
}

.goal-head { display: flex; align-items: center; gap: 10px; min-width: 200px; }
.goal-title { font-weight: 700; color: #1f2937; }
.goal-type { font-size: 12px; padding: 2px 10px; border-radius: 999px; background: #dbeafe; color: #2563eb; }
.goal-deadline { font-size: 13px; color: #9ca3af; }

.goal-bar { flex: 1; height: 8px; background: #e5e7eb; border-radius: 999px; overflow: hidden; }
.goal-fill { height: 100%; background: #2563eb; border-radius: 999px; }
.goal-pct { font-size: 13px; color: #374151; font-weight: 600; min-width: 44px; text-align: right; }

.empty { color: #9ca3af; padding: 20px; background: #fff; border: 1px dashed #d1d5db; border-radius: 12px; }
</style>
