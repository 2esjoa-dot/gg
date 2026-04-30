export type AdminRole = 'store_admin' | 'hq_admin'

export interface AdminLoginRequest {
  store_code: string
  username: string
  password: string
}

export interface AdminLoginResponse {
  token: string
  role: AdminRole
  store_id: number
  username: string
}

export interface RegisterAccountRequest {
  username: string
  password: string
}

export interface Table {
  id: number
  store_id: number
  table_number: number
  session_active: boolean
  current_total: number
}

export interface CreateTableRequest {
  table_number: number
  password: string
}

export interface HistoryOrder {
  id: number
  order_number: string
  items: HistoryOrderItem[]
  total_amount: number
  created_at: string
  completed_at: string
}

export interface HistoryOrderItem {
  menu_name: string
  quantity: number
  unit_price: number
  subtotal: number
}

export interface MenuItem {
  id: number
  store_id: number
  category_id: number
  name: string
  price: number
  description: string | null
  image_url: string | null
  display_order: number
  is_active: boolean
}

export interface Category {
  id: number
  store_id: number
  name: string
  display_order: number
}

export interface CreateMenuItemRequest {
  name: string
  price: number
  description?: string
  category_id: number
  image_url?: string
  is_active?: boolean
}

export interface UpdateMenuItemRequest {
  name?: string
  price?: number
  description?: string
  category_id?: number
  image_url?: string
  is_active?: boolean
}

export interface UpdateMenuOrderRequest {
  items: { item_id: number; display_order: number }[]
}

export interface Store {
  id: number
  name: string
  code: string
  address: string | null
  created_at: string
}

export interface CreateStoreRequest {
  name: string
  code: string
  address?: string
}

export interface ApiError {
  detail: string
  status_code?: number
}
