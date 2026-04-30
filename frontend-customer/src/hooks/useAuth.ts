import { useAuthStore } from '../store/authStore'
import { loginTablet } from '../api/auth'
import type { LoginRequest } from '../types'

export function useAuth() {
  const { login, logout, isAuthenticated, storeId, tableId, sessionId } = useAuthStore()

  const handleLogin = async (data: LoginRequest) => {
    const response = await loginTablet(data)
    login({
      token: response.token,
      storeId: response.store_id,
      tableId: response.table_id,
      storeCode: data.store_code,
      tableNumber: data.table_number,
      sessionId: response.session_id,
    })
  }

  return {
    isAuthenticated: isAuthenticated(),
    storeId,
    tableId,
    sessionId,
    login: handleLogin,
    logout,
  }
}
