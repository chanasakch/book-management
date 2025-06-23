// Check if the user is logged in by verifying the presence of a token in localStorage
export function isLoggedIn(): boolean {
  return !!localStorage.getItem('token')  // Returns true if token exists
}

// Log out by removing the token from localStorage
export function logout(): void {
  localStorage.removeItem('token')  // Clears token to log out
}