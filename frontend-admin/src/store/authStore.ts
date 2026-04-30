import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { AdminRole } from '../types'

interface AdminAuthState {
  token: string | null
  role: AdminRole | null
  storeId: number | null
  username: string | null

  login: (data: { token: string; role: AdminRole; storeId: number; username: string }) => void
  logout: () => void
  isAuthenticated: () => boolean
  isHQAdmin: () => boolean
}

export const useAdminAuthStore = create<AdminAuthState>()(
  persist(
    (set, get) => ({
      token: null,
      role: null,
      storeId: null,
      username: null,

      login: (data) =>
        set({
          token: data.token,
          role: data.role,
          storeId: data.storeId,
          username: data.username,
        }),

      logout: () =>
        set({ token: null, role: null, storeId: null, username: null }),

      isAuthenticated: () => get().token !== null,
      isHQAdmin: () => get().role === 'hq_admin',
    }),
    {
      name: 'table-order-admin-auth',
    }
  )
)
