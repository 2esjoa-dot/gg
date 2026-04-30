import { useAuthStore } from '../store/authStore'

const BASE_URL = '/api'

export class ApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public detail?: string
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    if (response.status === 401) {
      useAuthStore.getState().logout()
    }
    const error = await response.json().catch(() => ({ detail: '요청에 실패했습니다' }))
    throw new ApiError(error.detail || '요청에 실패했습니다', response.status, error.detail)
  }
  return response.json()
}

function getHeaders(): Record<string, string> {
  const token = useAuthStore.getState().token
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  }
  if (token) headers['Authorization'] = `Bearer ${token}`
  return headers
}

export async function apiGet<T>(endpoint: string): Promise<T> {
  const response = await fetch(`${BASE_URL}${endpoint}`, { headers: getHeaders() })
  return handleResponse<T>(response)
}

export async function apiPost<T>(endpoint: string, body?: unknown): Promise<T> {
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    method: 'POST',
    headers: getHeaders(),
    body: body ? JSON.stringify(body) : undefined,
  })
  return handleResponse<T>(response)
}
