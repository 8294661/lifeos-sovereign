<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { GOAL_TYPE_GROUPS, GOAL_STATUS_LABEL } from '../goalMeta'

const API = 'http://127.0.0.1:8000'

const goals = ref([])
const form = ref(emptyForm())
const editingId = ref(null)

function emptyForm() {
  return {
    title: '',
    description: '',
    goal_type: 'short_term',
    deadline: '',
    priority: 3,
    progress: 0,
  }
}

const grouped = computed(() =>
  GOAL_TYPE_GROUPS.map((g) => ({
    ...g,
    items: goals.value.filter((x) => x.goal_type === g.key),
  })),
)

const load = async () => {
  try {
    goals.value = (await axios.get(`${API}/api/goals`)).data
  } catch (e) {
    console.error(e)
  }
}

const submit = async () => {
  if (!form.value.title.trim()) {
    alert('标题不能为空')
    return
  }
  try {
    if (editingId.value) {
      await axios.put(`${API}/api/goals/${editingId.value}`, form.value)
    } else {
      await axios.post(`${API}/api/goals`, form.value)
    }
    reset()
    await load()
  } catch (e) {
    alert('保存失败：' + (e.response?.data?.detail || e.message))
  }
}

const edit = (g) => {
  editingId.value = g.id
  form.value = {
    title: g.title,
    description: g.description || '',
    goal_type: g.goal_type,
    deadline: g.deadline || '',
    priority: g.priority ?? 3,
    progress: g.progress ?? 0,
  }
}

const reset = () => {
  editingId.value = null
  form.value = emptyForm()
}

const setProgress = async (g, val) => {
  g.progress = val
  try {
    await axios.put(`${API}/api/goals/${g.id}`, { progress: val })
  } catch (e) {
    alert('更新失败：' + (e.response?.data?.detail || e.message))
  }
}

const remove = async (g) => {
  if (!confirm(`删除目标「${g.title}」？其子目标会解除关联。`)) return
  try {
    await axios.delete(`${API}/api/goals/${g.id}`)
    await load()
  } catch (e) {
    alert('删除失败：' + (e.response?.data?.detail || e.message))
  }
}

onMounted(load)
</script>

<template>
<div>
  <h1>🎯 目标</h1>
  <p class="subtitle">终极 → 长期 → 中期 → 短期，层层拆解</p>

  <div class="form-card">
    <h3>{{ editingId ? '编辑目标' : '新增目标' }}</h3>
    <div class="form">
      <label>标题</label>
      <input v-model="form.title" type="text" placeholder="例如：增重到 65kg">

      <label>类型</label>
      <select v-model="form.goal_type">
        <option v-for="g in GOAL_TYPE_GROUPS" :key="g.key" :value="g.key">{{ g.label }}</option>
      </select>

      <label>描述（可选）</label>
      <textarea v-model="form.description" placeholder="怎么做、做到什么程度"></textarea>

      <label>截止日期（可选）</label>
      <input v-model="form.deadline" type="date">

      <div class="form-row">
        <div>
          <label>优先级</label>
          <input v-model.number="form.priority" type="number" min="1" max="5">
        </div>
        <div>
          <label>初始进度 %</label>
          <input v-model.number="form.progress" type="number" min="0" max="100">
        </div>
      </div>

      <div class="form-actions">
        <button class="primary" @click="submit">{{ editingId ? '保存修改' : '添加目标' }}</button>
        <button v-if="editingId" class="ghost" @click="reset">取消编辑</button>
      </div>
    </div>
  </div>

  <div v-for="group in grouped" :key="group.key" class="group">
    <h2>{{ group.label }} <span class="count">{{ group.items.length }}</span></h2>
    <div v-if="group.items.length" class="goal-list">
      <div v-for="g in group.items" :key="g.id" class="goal">
        <div class="goal-main">
          <div class="goal-head">
            <span class="goal-title">{{ g.title }}</span>
            <span class="badge" :class="g.status">{{ GOAL_STATUS_LABEL[g.status] || g.status }}</span>
            <span v-if="g.deadline" class="deadline">截止 {{ g.deadline }}</span>
          </div>
          <div v-if="g.description" class="goal-desc">{{ g.description }}</div>
          <div class="progress-row">
            <div class="bar"><div class="fill" :style="{ width: (g.progress || 0) + '%' }"></div></div>
            <span class="pct">{{ g.progress || 0 }}%</span>
            <input
              class="slider"
              type="range"
              min="0" max="100"
              :value="g.progress || 0"
              @change="setProgress(g, Number($event.target.value))"
            >
          </div>
        </div>
        <div class="goal-actions">
          <button class="edit" @click="edit(g)">编辑</button>
          <button class="del" @click="remove(g)">删除</button>
        </div>
      </div>
    </div>
    <div v-else class="empty">暂无{{ group.label }}，点上方添加</div>
  </div>
</div>
</template>

<style>
.subtitle { color: #6b7280; margin-top: -8px; margin-bottom: 20px; }

.form-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 28px;
}

.form-card h3 { margin: 0 0 16px; color: #1f2937; }

.form { display: flex; flex-direction: column; gap: 10px; }
.form label { font-size: 13px; color: #6b7280; }
.form input, .form select, .form textarea {
  padding: 8px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
}
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

.form-actions { display: flex; gap: 10px; margin-top: 12px; }
.primary { background: #2563eb; color: #fff; border: none; border-radius: 6px; padding: 10px 16px; cursor: pointer; }
.ghost { background: #fff; color: #6b7280; border: 1px solid #d1d5db; border-radius: 6px; padding: 10px 16px; cursor: pointer; }

.group { margin-bottom: 28px; }
.group h2 { margin: 0 0 12px; color: #1f2937; }
.count { color: #9ca3af; font-size: 14px; font-weight: 400; }

.goal-list { display: flex; flex-direction: column; gap: 12px; }
.goal {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 16px 20px;
}
.goal-main { flex: 1; }
.goal-head { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.goal-title { font-weight: 700; color: #1f2937; }
.badge { font-size: 12px; padding: 2px 10px; border-radius: 999px; background: #f3f4f6; color: #6b7280; }
.badge.in_progress { background: #dbeafe; color: #2563eb; }
.badge.completed { background: #dcfce7; color: #16a34a; }
.badge.paused { background: #fef3c7; color: #d97706; }
.deadline { font-size: 13px; color: #9ca3af; }
.goal-desc { color: #6b7280; font-size: 14px; margin-top: 6px; }

.progress-row { display: flex; align-items: center; gap: 12px; margin-top: 10px; }
.bar { flex: 1; height: 8px; background: #e5e7eb; border-radius: 999px; overflow: hidden; }
.fill { height: 100%; background: #2563eb; border-radius: 999px; transition: width 0.2s; }
.pct { font-size: 13px; color: #374151; font-weight: 600; min-width: 44px; text-align: right; }
.slider { width: 140px; }

.goal-actions { display: flex; gap: 8px; }
.edit { background: #e0e7ff; color: #4338ca; border: none; border-radius: 6px; padding: 8px 14px; cursor: pointer; }
.del { background: #fee2e2; color: #dc2626; border: none; border-radius: 6px; padding: 8px 14px; cursor: pointer; }

.empty { color: #9ca3af; padding: 20px; background: #fff; border: 1px dashed #d1d5db; border-radius: 12px; }
</style>
