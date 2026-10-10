<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API = 'http://127.0.0.1:8000'

const form = ref({
    height: null,
    current_weight: null,
    blood_type: '',
    allergies: '',
    health_status: '',
    exercise_habit: '',
    description: '',
})

onMounted(async () => {
    try {
        const res = await axios.get(`${API}/api/profile/1`)
        const d = res.data
        if (d.personal_info) {
            form.value.height = d.personal_info.height
            form.value.current_weight = d.personal_info.current_weight
        }
        if (d.health_profile) {
            form.value.blood_type = d.health_profile.blood_type || ''
            form.value.allergies = d.health_profile.allergies || ''
            form.value.health_status = d.health_profile.health_status || ''
            form.value.exercise_habit = d.health_profile.exercise_habit || ''
            form.value.description = d.health_profile.description || ''
        }
    } catch (e) {
        console.error(e)
    }
})

const saveProfile = async () => {
    try {
        await axios.put(`${API}/api/profile/1`, form.value)
        alert('档案已更新')
    } catch (e) {
        alert('更新失败：' + (e.response?.data?.detail || e.message))
    }
}
</script>

<template>
<div>
    <h1>👤 我的档案</h1>
    <p class="subtitle">编辑后点击保存，通过 PUT 接口更新到 MySQL</p>

    <div class="form">
        <h2>📏 基础信息</h2>
        <label>身高 (cm)</label>
        <input v-model.number="form.height" type="number">

        <label>体重 (kg)</label>
        <input v-model.number="form.current_weight" type="number">

        <h2>❤️ 健康档案</h2>
        <label>血型</label>
        <input v-model="form.blood_type" placeholder="如：A / B / AB / O">

        <label>过敏史</label>
        <input v-model="form.allergies" placeholder="如：无 / 花粉过敏">

        <label>健康状况</label>
        <input v-model="form.health_status" placeholder="如：良好">

        <label>运动习惯</label>
        <input v-model="form.exercise_habit" placeholder="如：每周跑步 3 次">

        <label>补充说明</label>
        <textarea v-model="form.description"></textarea>

        <button @click="saveProfile">保存档案</button>
    </div>
</div>
</template>

<style>
.subtitle { color: #6b7280; margin-top: -8px; margin-bottom: 20px; }

.form {
    display: flex;
    flex-direction: column;
    max-width: 420px;
    gap: 10px;
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 24px;
}

.form h2 { margin: 8px 0 4px; font-size: 16px; }
.form h2:first-child { margin-top: 0; }

input, textarea {
    padding: 8px;
    border: 1px solid #d1d5db;
    border-radius: 6px;
}

button {
    margin-top: 12px;
    padding: 10px;
    background: #2563eb;
    color: #fff;
    border: none;
    border-radius: 6px;
    cursor: pointer;
}
</style>
