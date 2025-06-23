<template>
  <div class="auth-container">
    <!-- Switch Between Login and Register -->
    <!-- Login Form -->
    <div v-if="isLogin">
      <form @submit.prevent="handleLogin" class="auth-form">
        <h2>Login</h2>
        <input v-model="username" type="text" placeholder="Username" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit" :disabled="loading">
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
        <!-- Toast Notification -->
        <div v-if="toast.message" :class="['toast', toast.type]">{{ toast.message }}</div>
        <p>Don't have an account? <a href="#" @click="toggleForm">Register here</a></p>
      </form>
    </div>

    <!-- Register Form -->
    <div v-else>
      <form @submit.prevent="handleRegister" class="auth-form">
        <h2>Register</h2>
        <input v-model="username" type="text" placeholder="Username" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit" :disabled="loading">
          {{ loading ? 'Registering...' : 'Register' }}
        </button>
        <!-- Toast Notification -->
        <div v-if="toast.message" :class="['toast', toast.type]">{{ toast.message }}</div>
        <p>Already have an account? <a href="#" @click="toggleForm">Login here</a></p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

/**
 * State variables
 * username - Stores the entered username
 * password - Stores the entered password
 * loading - Tracks loading state for button disable
 * toast - Object to manage toast notifications
 */
const username = ref('')
const password = ref('')
const loading = ref(false)
const toast = ref({ message: '', type: '' }) // Toast message state
const router = useRouter()

/**
 * To toggle between Login and Register form
 */
const isLogin = ref(true)

const toggleForm = () => {
  isLogin.value = !isLogin.value
}

/**
 * Function to show toast messages
 * @param msg - Message to display
 * @param type - Type of the toast (success/error)
 */
const showToast = (msg: string, type: 'success' | 'error') => {
  toast.value = { message: msg, type }

  // Remove toast message after a short duration
  setTimeout(() => {
    toast.value.message = ''
  }, 10000)
}

/**
 * Handle Login form submission
 */
const handleLogin = async () => {
  loading.value = true
  try {
    // Sending login request to the backend
    const res = await axios.post('http://localhost:8000/login', {
      username: username.value,
      password: password.value,
    })
    // Store token in localStorage
    localStorage.setItem('token', res.data.access_token)
    // Redirect to home page after successful login
    router.push('/') 
  } catch (err: any) {
    // Show error message if login fails
    showToast(err.response?.data?.detail || 'Login failed', 'error')
  } finally {
    loading.value = false
  }
}

/**
 * Handle Register form submission
 */
const handleRegister = async () => {
  loading.value = true
  try {
    // Sending register request to the backend
    await axios.post('http://localhost:8000/register', {
      username: username.value,
      password: password.value,
    })
    // Show success message and redirect to login page
    showToast('Registration successful! You can now login.', 'success')
    router.push('/login') 
  } catch (err: any) {
    // Show error message if registration fails
    showToast(err.response?.data?.detail || 'Registration failed', 'error')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* General Styles for the Auth Container */
.auth-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f3f4f6;
  font-family: 'Segoe UI', sans-serif; 
}

/* Form Styles */
.auth-form {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  font-family: inherit;
}

.auth-form h2,
.auth-form p,
.auth-form a,
.auth-form input,
.auth-form button {
  font-family: inherit; /* Consistent font */
}

.auth-form h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

/* Input Styles */
.auth-form input {
  width: 100%;
  padding: 0.65rem 0.75rem;
  margin-bottom: 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 1rem;
  box-sizing: border-box;
  transition: border 0.2s;
}

/* Focus Effect for Inputs */
.auth-form input:focus {
  border-color: #2563eb;
  outline: none;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2);
}

/* Button Styles */
.auth-form button {
  width: 100%;
  padding: 0.75rem;
  background-color: #2563eb;
  color: white;
  font-size: 1rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
}

/* Disable button when loading */
.auth-form button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Toast Styles */
.toast {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  text-align: center;
  transition: opacity 0.4s ease;
  opacity: 1;
  margin-top: 8px;
}

/* Toast hidden state */
.toast.hidden {
  opacity: 0;
}

/* Success and Error Toast Styles */
.toast.success {
  background-color: #d1fae5;
  color: #065f46;
}

.toast.error {
  background-color: #fee2e2;
  color: #991b1b;
}

/* Error Message Styling */
.error-msg {
  margin-top: 1rem;
  color: #dc2626;
  text-align: center;
}
</style>
