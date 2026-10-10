<script setup>
import { ref, nextTick } from 'vue'
import axios from 'axios'


const API = 'http://127.0.0.1:8000/api/ai/chat'

const messages = ref([])
const input = ref('')
const loading = ref(false)
const listEl = ref(null)


function scrollToBottom() {
    nextTick(() => {
        if (listEl.value) {
            listEl.value.scrollTop = listEl.value.scrollHeight
        }
    })
}


const send = async () => {
    const text = input.value.trim()
    if (!text || loading.value) return

    messages.value.push({ role: 'user', content: text })
    input.value = ''
    loading.value = true
    scrollToBottom()

    try {
        const res = await axios.post(API, { messages: messages.value })
        messages.value.push({ role: 'assistant', content: res.data.reply })
    } catch (e) {
        const detail = e.response?.data?.detail || e.message || '请求失败，请检查后端服务是否已启动'
        messages.value.push({ role: 'assistant', content: '⚠️ ' + detail })
    } finally {
        loading.value = false
        scrollToBottom()
    }
}
</script>


<template>

<div class="chat-wrap">

    <h1>🤖 LifeOS AI助手</h1>
    <p class="subtitle">基于你的个人数据做个性化状态分析与建议</p>

    <div ref="listEl" class="chat-list">

        <div class="msg assistant">
            <div class="bubble">
                你好，我是 LifeOS AI 助手 🤖 我已经读取了你的个人数据，想了解作息、心情、目标进展都可以问我～
            </div>
        </div>

        <div v-for="(m, i) in messages" :key="i" class="msg" :class="m.role">
            <div class="bubble">{{ m.content }}</div>
        </div>

        <div v-if="loading" class="msg assistant">
            <div class="bubble typing">
                <span></span><span></span><span></span>
            </div>
        </div>

    </div>

    <div class="chat-input">
        <input
            v-model="input"
            placeholder="输入你的问题，例如：帮我分析一下最近的作息"
            @keyup.enter="send"
            :disabled="loading"
        />
        <button @click="send" :disabled="loading || !input.trim()">
            {{ loading ? '分析中…' : '发送' }}
        </button>
    </div>

</div>

</template>


<style>

.chat-wrap {
    display: flex;
    flex-direction: column;
    height: calc(100vh - 80px);
}

.subtitle {
    color: #6b7280;
    margin-top: -8px;
    margin-bottom: 16px;
}

.chat-list {
    flex: 1;
    overflow-y: auto;
    padding: 8px 0;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.msg {
    display: flex;
}

.msg.user {
    justify-content: flex-end;
}

.msg.assistant {
    justify-content: flex-start;
}

.bubble {
    max-width: 70%;
    padding: 12px 16px;
    border-radius: 12px;
    line-height: 1.6;
    white-space: pre-wrap;
    word-break: break-word;
}

.msg.user .bubble {
    background: #2563eb;
    color: #fff;
    border-bottom-right-radius: 4px;
}

.msg.assistant .bubble {
    background: #fff;
    color: #1f2937;
    border: 1px solid #e5e7eb;
    border-bottom-left-radius: 4px;
}

.typing {
    display: flex;
    gap: 4px;
    align-items: center;
}

.typing span {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #9ca3af;
    animation: blink 1.2s infinite;
}

.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }

@keyframes blink {
    0%, 80%, 100% { opacity: 0.2; }
    40% { opacity: 1; }
}

.chat-input {
    display: flex;
    gap: 10px;
    margin-top: 16px;
}

.chat-input input {
    flex: 1;
    padding: 12px;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    font-size: 14px;
}

.chat-input button {
    padding: 12px 24px;
    background: #2563eb;
    color: #fff;
    border: none;
    border-radius: 8px;
    cursor: pointer;
}

.chat-input button:disabled {
    background: #93c5fd;
    cursor: not-allowed;
}

</style>
