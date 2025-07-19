<template>
  <div class="app">
    <h2>Inject NAT untuk PPPoE</h2>
    <form @submit.prevent="submit">
      <input v-model="username" placeholder="Username PPPoE" required />
      <button :disabled="loading">{{ loading ? 'Memproses...' : 'Submit' }}</button>
    </form>
    <p v-if="message" :class="status">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const username = ref('')
const message = ref('')
const status = ref('')
const loading = ref(false)

const submit = async () => {
  loading.value = true
  message.value = ''
  status.value = ''

  try {
    const form = new FormData()
    form.append('username', username.value)

    const res = await fetch('/inject-nat', {
      method: 'POST',
      body: form
    })

    const data = await res.json()
    status.value = data.status
    message.value = data.message

    if (data.status === 'success') {
      setTimeout(() => {
        window.location.href = 'http://domain'
      }, 1500)
    }
  } catch (err) {
    status.value = 'error'
    message.value = 'Gagal menghubungi server.'
  }

  loading.value = false
}
</script>

<style>
.app {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  font-family: sans-serif;
}
input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
}
button {
  padding: 8px 16px;
}
.success { color: green }
.error { color: red }
</style>
