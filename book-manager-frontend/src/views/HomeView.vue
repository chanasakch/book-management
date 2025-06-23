<template>
  <div class="container">
    <!-- Header Bar - Displays the logo and logout button -->
    <div class="header-bar">
      <div class="header-left">
        <h1 class="header">
          <img src="@/assets/icons/innovationai.jpg" class="icon" />
          Book Manager
        </h1>
      </div>
      <div class="header-right">
        <button @click="handleLogout" class="logout-btn">Logout</button>
      </div>
    </div>

    <!-- Add Book Button - Button to open the modal for adding a new book -->
    <div class="add-book-wrapper">
      <button class="btn primary" @click="showAddModal = true">
        <svg xmlns="http://www.w3.org/2000/svg" class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"
          stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19" />
          <line x1="5" y1="12" x2="19" y2="12" />
        </svg>
        Add Book
      </button>
    </div>

    <!-- Toast Notification - For displaying success or error messages -->
    <div v-if="toast.message" :class="['toast', toast.type]">{{ toast.message }}</div>

    <!-- Pagination & Controls - For managing pagination and selecting rows per page -->
    <div class="pagination-wrapper">
      <label class="rows-per-page">
        Rows per page:
        <select v-model.number="pageSize" @change="fetchBooks" class="rows-select">
          <option :value="5">5</option>
          <option :value="10">10</option>
          <option :value="20">20</option>
        </select>
      </label>
      <span>{{ pageStart }} - {{ pageEnd }} of {{ total }}</span>
      <input v-model.number="goToPage" @keyup.enter="changePage(goToPage)" class="page-input" type="number" min="1"
        :max="totalPages" :placeholder="`Page #`" />
      <span>/ {{ totalPages }}</span>
      <button :disabled="currentPage === 1" @click="changePage(currentPage - 1)">
        <svg xmlns="http://www.w3.org/2000/svg" class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"
          stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="15 18 9 12 15 6" />
        </svg>
      </button>
      <button :disabled="books.length < pageSize" @click="changePage(currentPage + 1)">
        <svg xmlns="http://www.w3.org/2000/svg" class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"
          stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="9 18 15 12 9 6" />
        </svg>
      </button>
    </div>

    <!-- Loading / Error - Shows loading message or error if data fetch fails -->
    <div v-if="loading" class="loading">Loading books...</div>
    <div v-else-if="error" class="error">❌ {{ error }}</div>

    <!-- Book Table - Displays books in a table with edit and delete options -->
    <table v-else class="book-table">
      <thead>
        <tr>
          <th>Title</th>
          <th>Author</th>
          <th>Year</th>
          <th>Genre</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <!-- Iterates over books and displays them in table rows -->
        <tr v-for="book in books" :key="book.id">
          <td>{{ book.title }}</td>
          <td>{{ book.author }}</td>
          <td>{{ book.published_year || 'N/A' }}</td>
          <td>{{ book.genre }}</td>
          <td class="action-buttons">
            <!-- Edit button for modifying book details -->
            <button class="btn edit" @click="startEdit(book)">
              <svg xmlns="http://www.w3.org/2000/svg" class="svg-icon" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 20h9" />
                <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4 12.5-12.5z" />
              </svg>
              Edit
            </button>
            <!-- Delete button for removing a book -->
            <button class="btn delete" @click="confirmDelete(book.id)">
              <svg xmlns="http://www.w3.org/2000/svg" class="svg-icon" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="3 6 5 6 21 6" />
                <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6m5 0V4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v2" />
              </svg>
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Modal for Add/Edit Book -->
    <div v-if="showAddModal || showEditModal" class="modal">
      <div class="modal-content">
        <h2>{{ showAddModal ? 'Add New Book' : 'Edit Book' }}</h2>
        <form @submit.prevent="showAddModal ? addBook() : saveEdit(editBookId)">
          <input v-model="activeBook.title" type="text" maxlength="150" placeholder="Title"
            title="Max 150 characters" />
          <span v-if="showValidation && !activeBook.title.trim()" class="input-error">Title is required.</span>
          <input v-model="activeBook.author" placeholder="Author" maxlength="100" title="Max 100 characters" />
          <span v-if="showValidation && !activeBook.author.trim()" class="input-error">Author is required.</span>
          <input v-model="activeBook.published_year" type="text" inputmode="numeric" maxlength="4" @input="onYearInput"
            placeholder="Year" title="Only 4-digit year" />
          <input v-model="activeBook.genre" placeholder="Genre" maxlength="50" title="Max 50 characters" />
          <div class="modal-actions">
            <button type="submit" class="btn success">Save</button>
            <button type="button" class="btn" @click="showAddModal ? cancelAdd() : cancelEdit()">Cancel</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Confirm Delete Modal - Asks user for confirmation before deleting a book -->
    <div v-if="showConfirmDelete" class="modal">
      <div class="modal-content confirm-delete">
        <div class="delete-icon-wrapper">
          <img src="@/assets/icons/delete.png" alt="Trash Icon" />
        </div>
        <h3>Delete Book</h3>
        <p>Are you sure you want to delete this book? This action cannot be undone.</p>
        <div class="modal-actions">
          <button class="btn delete" @click="confirmDeleteBook">Yes, Delete</button>
          <button class="btn" @click="showConfirmDelete = false">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Confirm Logout Modal - Asks user for confirmation before logging out -->
    <div v-if="showConfirmLogout" class="modal">
      <div class="modal-content confirm-logout">
        <div class="delete-icon-wrapper">
          <img src="@/assets/icons/power.png" alt="Exit Icon" />
        </div>
        <h3>Logout</h3>
        <p>Are you sure you want to log out?</p>
        <div class="modal-actions">
          <button class="btn logout-success" @click="confirmLogout">Yes, Logout</button>
          <button class="btn" @click="showConfirmLogout = false">Cancel</button>
        </div>
      </div>
    </div>

  </div>
</template>


<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import { getBooksPaginated, createBook, deleteBook, updateBook } from '../services/bookApi'
import axios from 'axios'
import { useRouter } from 'vue-router'

// Router and Logout Logic
const router = useRouter()

const handleLogout = () => {
  showConfirmLogout.value = true
}

const confirmLogout = () => {
  localStorage.removeItem('token')
  router.push('/login')
  showConfirmLogout.value = false
}

// Token Validation for Protected Route
const token = localStorage.getItem('token')
axios.get('http://localhost:8000/protected-endpoint', {
  headers: {
    Authorization: `Bearer ${token}`
  }
})

const toast = ref({ message: '', type: '' })
const books = ref<any[]>([])
const loading = ref(true)
const error = ref('')
const currentPage = ref(1)
const pageSize = ref(5)

const newBook = ref({ title: '', author: '', published_year: undefined, genre: '' })
const editBook = ref({ title: '', author: '', published_year: undefined, genre: '' })
const showAddModal = ref(false)
const showEditModal = ref(false)
const editBookId = ref<number | null>(null)
const activeBook = computed(() => showAddModal.value ? newBook.value : editBook.value)

const showConfirmDelete = ref(false)
const deleteTargetId = ref<number | null>(null)
const showConfirmLogout = ref(false)

const total = ref(0)
const pageStart = computed(() => (currentPage.value - 1) * pageSize.value + 1)
const pageEnd = computed(() =>
  pageStart.value + (Array.isArray(books.value) ? books.value.length : 0) - 1
)

const goToPage = ref<number>(1)
const totalPages = computed(() => {
  return pageSize.value > 0 ? Math.ceil(total.value / pageSize.value) : 1
})

// Toast Notification Logic
function showToast(msg: string, type: 'success' | 'error') {
  toast.value = { message: msg, type }
  setTimeout(() => {
    const el = document.querySelector('.toast')
    if (el) el.classList.add('hidden')
  }, 2500)
  setTimeout(() => {
    toast.value.message = ''
  }, 2900)
}

// Fetching Books (Paginated)
const fetchBooks = async () => {
  loading.value = true
  try {
    const res = await getBooksPaginated(currentPage.value, pageSize.value)
    const response = res.data as { data: any[], total: number }
    books.value = response.data
    total.value = response.total
  } catch (err: any) {
    error.value = err.message || 'Failed to load books'
  } finally {
    loading.value = false
  }
}

onMounted(fetchBooks)

// Year Input Validation
const onYearInput = (e: Event) => {
  const input = e.target as HTMLInputElement
  input.value = input.value.replace(/\D/g, '').slice(0, 4)
  activeBook.value.published_year = input.value
}

const showValidation = ref(false)

// Add Book Logic
const addBook = async () => {
  showValidation.value = true
  if (!newBook.value.title.trim() || !newBook.value.author.trim()) return
  try {
    await createBook(newBook.value)
    showToast('Book added successfully.', 'success')
    showAddModal.value = false
    await fetchBooks()
    newBook.value = { title: '', author: '', published_year: undefined, genre: '' }
    showValidation.value = false
  } catch (err: any) {
    error.value = err.message || 'Failed to add book'
    showToast('Failed to add book.', 'error')
  }
}

// Delete Book Logic
const confirmDelete = (id: number) => {
  deleteTargetId.value = id
  showConfirmDelete.value = true
}

const confirmDeleteBook = async () => {
  if (deleteTargetId.value === null) return
  try {
    await deleteBook(deleteTargetId.value)
    books.value = books.value.filter(book => book.id !== deleteTargetId.value)
    showToast('Book deleted successfully.', 'success')
  } catch (err: any) {
    error.value = err.message || 'Failed to delete book'
    showToast('Failed to delete book.', 'error')
  } finally {
    showConfirmDelete.value = false
    deleteTargetId.value = null
  }
}

// Edit Book Logic
const startEdit = (book: any) => {
  editBook.value = { ...book }
  editBookId.value = book.id
  showEditModal.value = true
}

const cancelEdit = () => {
  showEditModal.value = false
  editBookId.value = null
  editBook.value = { title: '', author: '', published_year: undefined, genre: '' }
  showValidation.value = false
}

const cancelAdd = () => {
  showAddModal.value = false
  newBook.value = { title: '', author: '', published_year: undefined, genre: '' }
  showValidation.value = false
}

const saveEdit = async (id: number | null) => {
  if (id === null) return
  showValidation.value = true
  if (!editBook.value.title.trim() || !editBook.value.author.trim()) return
  try {
    const res = await updateBook(id, editBook.value)
    const index = books.value.findIndex(b => b.id === id)
    if (index !== -1) books.value[index] = res.data
    cancelEdit()
    showValidation.value = false
    showToast('Book updated successfully.', 'success')
  } catch (err: any) {
    error.value = err.message || 'Failed to update book'
    showToast('Failed to update book.', 'error')
  }
}

// Pagination Logic
const changePage = (page: number) => {
  if (!page || isNaN(page) || page < 1) page = 1
  if (page > totalPages.value) page = totalPages.value

  currentPage.value = page
  goToPage.value = page
  fetchBooks()
}

watch(pageSize, () => fetchBooks()) // Re-fetch books when page size changes
</script>


<style scoped lang="scss">
// ==========================
// 1. General Layout and Container
// ==========================
.container {
  padding: 2rem;
  margin: auto;
  font-family: 'Segoe UI', sans-serif;
}

// ==========================
// 2. Header and Icon Styling
// ==========================
.header {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #2c3e50;
}

.icon {
  width: 4rem;
  height: 4rem;
  border-radius: 50%;
  object-fit: cover;
  object-position: center;
}

// ==========================
// 3. Header Bar
// ==========================
.header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.header-left {
  display: flex;
  align-items: center;
}

.header-right {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  align-items: center;
}

// ==========================
// 4. Logout Button
// ==========================
.logout-btn {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #d1d5db;
  color: #374151;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.logout-btn:hover {
  background-color: #b1b6b7;
}

// ==========================
// 5. Add Book Button
// ==========================
.add-book-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-top: 1rem;
}

.btn.primary {
  background-color: #2563eb;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.btn.primary:hover {
  background-color: #1e40af;
}

// ==========================
// 6. Pagination
// ==========================
.pagination-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 0.5rem;
  margin-bottom: 1rem;

  .rows-per-page {
    display: flex;
    align-items: center;
    gap: 0.25rem;
  }

  .rows-select {
    border: 1px solid #d0d5dd;
    border-radius: 4px;
    height: 26px;
  }

  .page-input {
    width: 50px;
    padding: 0.25rem 0.5rem;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    font-size: 0.9rem;
  }

  button {
    padding: 0.3rem 0.6rem;
    background-color: #e5e7eb;
    border: none;
    border-radius: 4px;
    cursor: pointer;

    &:disabled {
      opacity: 0.4;
      cursor: not-allowed;
    }
  }
}

// ==========================
// 7. Pagination Controls
// ==========================
.pagination-controls label {
  font-size: 0.9rem;
  color: #4b5563;

  select {
    margin-left: 0.5rem;
    padding: 0.2rem 0.4rem;
  }
}

.pagination-buttons button {
  padding: 0.3rem 0.75rem;
  background-color: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 0.85rem;
  cursor: pointer;

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

// ==========================
// 8. Add Book Button (Right Float)
// ==========================
.add-book {
  margin-top: 1rem;
  float: right;
}

// ==========================
// 9. General Button Styles
// ==========================
.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  font-size: 0.9rem;
  cursor: pointer;

  &.primary {
    background-color: #2563eb;
    color: white;
  }

  &.edit {
    background-color: #facc15;
    color: #333;
  }

  &.delete {
    background-color: #dc2626;
    color: white;
  }

  &.success {
    background-color: #1e40af;
    color: white;
  }
}

// ==========================
// 10. Book Table
// ==========================
.book-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: auto;

  th,
  td {
    padding: 0.75rem;
    border: 1px solid #e5e7eb;
    text-align: left;
    white-space: normal;
    word-break: break-word;
  }

  th:last-child,
  td:last-child {
    width: auto;
    text-align: center;
    white-space: nowrap;
  }

  th {
    background-color: #f3f4f6;
  }
}

// ==========================
// 11. Action Buttons (Edit/Delete)
// ==========================
.action-buttons {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;

  button {
    min-width: 80px;
    text-align: center;
  }

  @media (max-width: 640px) {
    flex-direction: column;
  }
}

// ==========================
// 12. Modal and Modal Content
// ==========================
.modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-content {
  background: #ffffff;
  padding: 2rem;
  border-radius: 1rem;
  width: 80vw;
  max-width: 480px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  animation: fadeIn 0.2s ease-in-out;

  h2 {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 1.25rem;
    color: #111827;
  }

  input {
    width: 100%;
    margin-bottom: 1rem;
    padding: 0.65rem 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    font-size: 1rem;
    transition: border 0.2s;
    box-sizing: border-box;

    &:focus {
      border-color: #2563eb;
      outline: none;
      box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2);
    }
  }
}

// ==========================
// 13. Modal Confirmation (Logout and Delete)
// ==========================
.modal-content.confirm-logout {
  max-width: 400px;
  text-align: center;
  background-color: #fff;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  animation: fadeIn 0.2s ease-in-out;
}

.modal-content.confirm-logout h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #b91c1c;
  margin-bottom: 0.5rem;
}

.modal-content.confirm-logout p {
  font-size: 0.95rem;
  color: #374151;
  margin-bottom: 1.5rem;
}

.modal-content.confirm-logout .btn.logout-success {
  background-color: #dc2626;
  color: white;

  &:hover {
    background-color: #b91c1c;
  }
}

// ==========================
// 14. Modal Confirmation for Delete
// ==========================
.modal-content.confirm-delete {
  max-width: 400px;
  text-align: center;

  h3 {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: #b91c1c;
  }

  p {
    font-size: 0.95rem;
    color: #374151;
    margin-bottom: 1.5rem;
  }

  .btn.delete {
    background-color: #dc2626;
    color: white;

    &:hover {
      background-color: #b91c1c;
    }
  }

  .btn:not(.delete) {
    background-color: #e5e7eb;
    color: #374151;

    &:hover {
      background-color: #d1d5db;
    }
  }
}

// ==========================
// 15. Modal Actions (Cancel, Save, etc.)
// ==========================
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;

  .btn {
    padding: 0.5rem 1rem;
    font-size: 0.95rem;
    border-radius: 0.375rem;

    &.success {
      background-color: #2563eb;
      color: white;

      &:hover {
        background-color: #1e40af;
      }
    }

    &:not(.success) {
      background-color: #e5e7eb;
      color: #374151;

      &:hover {
        background-color: #d1d5db;
      }
    }
  }
}

// ==========================
// 16. Keyframes for Animations
// ==========================
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(16px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

// ==========================
// 17. Loading, Error, and Toast Notifications
// ==========================
.loading {
  color: #6b7280;
}

.error {
  color: #dc2626;
  font-weight: 500;
  margin-bottom: 1rem;
}

.input-error {
  color: #dc2626;
  font-size: 0.8rem;
  margin-top: -0.75rem;
  margin-bottom: 0.75rem;
  display: block;
}

.toast {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  text-align: center;
  transition: opacity 0.4s ease;
  opacity: 1;

  &.hidden {
    opacity: 0;
  }

  &.success {
    background-color: #d1fae5;
    color: #065f46;
  }

  &.error {
    background-color: #fee2e2;
    color: #991b1b;
  }
}

// ==========================
// 18. SVG Icon Styling
// ==========================
.svg-icon {
  width: 1rem;
  height: 1rem;
  vertical-align: middle;
}

// ==========================
// 19. Delete Icon Wrapper
// ==========================
.delete-icon-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 1rem;

  img {
    background-color: #fee2e2;
    padding: 1rem;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    object-fit: contain;
  }
}

// ==========================
// 20. Delete Icon Styling
// ==========================
.delete-icon-wrapper img {
  background-color: #fee2e2;
  padding: 1rem;
  border-radius: 50%;
  width: 35px;
  height: 35px;
  object-fit: contain;
}
</style>

