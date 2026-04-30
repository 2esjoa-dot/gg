import { apiPost } from './client'
import type { AdminLoginRequest, AdminLoginResponse, RegisterAccountRequest } from '../types'

export function loginAdmin(data: AdminLoginRequest): Promise<AdminLoginResponse> {
  return apiPost<AdminLoginResponse>('/admin/auth/login', data)
}

export function registerAccount(data: RegisterAccountRequest): Promise<{ id: number; username: string }> {
  return apiPost('/admin/auth/register', data)
}
