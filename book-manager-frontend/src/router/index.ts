// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import Login from '@/views/Login.vue'
// import { isLoggedIn } from '@/utils/auth'  // Import isLoggedIn function for authentication

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { requiresAuth: true },  // This route requires authentication
  },
  {
    path: '/login',
    name: 'login',
    component: Login,  // Login view
  },
]

// Create a new Vue Router instance
const router = createRouter({
  history: createWebHistory(),
  routes,  // Define the routes for navigation
})

// Global route guard to ensure authentication
router.beforeEach((to, from, next) => {
  // If the route requires authentication and the user isn't logged in, redirect to login
  if (to.meta.requiresAuth && !isLoggedIn()) {
    next('/login')  // Redirect to login if no token found
  } else {
    next()  // Proceed to the route
  }
})

// Helper function to check if the user is logged in
export function isLoggedIn() {
  const token = localStorage.getItem('token')  // Check if the token exists in localStorage
  return !!token  // Return true if token exists, else false
}

export default router  // Export the router to be used in the app
