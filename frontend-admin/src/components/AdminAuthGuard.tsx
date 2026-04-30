import { ReactNode } from 'react'
import { Navigate } from 'react-router-dom'
import { useAdminAuthStore } from '../store/authStore'

export default function AdminAuthGuard({ children }: { children: ReactNode }) {
  const isAuthenticated = useAdminAuthStore((s) => s.isAuthenticated())

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}

export function RoleGuard({ role, children }: { role: string; children: ReactNode }) {
  const currentRole = useAdminAuthStore((s) => s.role)

  if (currentRole !== role) {
    return <Navigate to="/" replace />
  }

  return <>{children}</>
}
