import { apiPost } from './client'
import type { LoginRequest, LoginResponse } from '../types'

export function loginTablet(data: LoginRequest): Promise<LoginResponse> {
  return apiPost<LoginResponse>('/customer/auth/login', data)
}
