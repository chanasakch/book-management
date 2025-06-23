// src/services/bookApi.ts
import axios from 'axios'

// Create axios instance with a base URL for the backend API
const api = axios.create({
  baseURL: 'http://localhost:8000',  // Backend API URL
})

// JWT Interceptor: Attach token to every request if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')  // Retrieve token from localStorage
  if (token) {
    config.headers.Authorization = `Bearer ${token}`  // Attach token to header
  }
  return config
})

// Book-related API functions
export const getBooks = () => api.get('/books')  // Fetch all books
export const getBook = (id: number) => api.get(`/books/${id}`)  // Fetch a specific book by id
export const createBook = (data: any) => api.post('/books', data)  // Create a new book
export const updateBook = (id: number, data: any) => api.put(`/books/${id}`, data)  // Update a book
export const deleteBook = (id: number) => api.delete(`/books/${id}`)  // Delete a book
export const getBooksPaginated = (page: number, pageSize: number = 5) => {
  const skip = (page - 1) * pageSize
  return api.get(`/books?skip=${skip}&limit=${pageSize}`)  // Fetch books with pagination
}

// Auth-related API functions
export const login = (username: string, password: string) =>
  api.post('/login', { username, password })  // Login API

export const register = (username: string, password: string) =>
  api.post('/register', { username, password })  // Register API

export const getProfile = () => api.get('/me')  // Fetch user profile
