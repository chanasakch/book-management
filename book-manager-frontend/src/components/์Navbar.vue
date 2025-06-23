<template>
  <div class="navbar">
    <h1 class="header">Book Manager</h1>
    <button class="logout-button" @click="handleLogout">Logout</button>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

// ฟังก์ชัน Logout
const router = useRouter()
const handleLogout = () => {
  // ลบ token ที่เก็บใน localStorage
  localStorage.removeItem('token')

  // รีไดเรคไปที่หน้า login
  router.push('/login')
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between; /* ทำให้ Header กับปุ่ม Logout อยู่คนละข้าง */
  align-items: center; /* จัดแนวกลางแนวตั้ง */
  padding: 10px 20px;
  background-color: #2563eb;
  color: white;
}

.header {
  font-size: 1.5rem;
  font-weight: bold;
}

.logout-button {
  padding: 0.5rem 1rem;
  background-color: #dc2626;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.logout-button:hover {
  background-color: #b91c1c;
}
</style>
