import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AuthState {
  token: string | null
  storeId: number | null
  tableId: number | null
  storeCode: string | null
  tableNumber: number | null
  sessionId: number | null

  login: (data: {
    token: string
    storeId: number
    tableId: number
    storeCode: string
    tableNumber: number
    sessionId: number | null
  }) => void
  logout: () => void
  setSessionId: (sessionId: number) => void
  isAuthenticated: () => boolean
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      token: null,
      storeId: null,
      tableId: null,
      storeCode: null,
      tableNumber: null,
      sessionId: null,

      login: (data) =>
        set({
          token: data.token,
          storeId: data.storeId,
          tableId: data.tableId,
          storeCode: data.storeCode,
          tableNumber: data.tableNumber,
          sessionId: data.sessionId,
        }),

      logout: () =>
        set({
          token: null,
          storeId: null,
          tableId: null,
          storeCode: null,
          tableNumber: null,
          sessionId: null,
        }),

      setSessionId: (sessionId: number) => set({ sessionId }),

      isAuthenticated: () => get().token !== null,
    }),
    {
      name: 'table-order-auth',
    }
  )
)
