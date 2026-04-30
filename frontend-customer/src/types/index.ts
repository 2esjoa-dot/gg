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

export interface CartItem {
  menuItem: MenuItem
  quantity: number
}

export interface Order {
  id: number
  order_number: string
  status: OrderStatus
  total_amount: number
  items: OrderItem[]
  created_at: string
}

export type OrderStatus = 'pending' | 'preparing' | 'completed'

export interface OrderItem {
  id: number
  menu_item_id: number
  menu_name: string
  quantity: number
  unit_price: number
  subtotal: number
}

export interface CreateOrderRequest {
  store_id: number
  table_id: number
  session_id?: number
  items: CreateOrderItemRequest[]
}

export interface CreateOrderItemRequest {
  menu_item_id: number
  quantity: number
}

export interface CreateOrderResponse {
  id: number
  order_number: string
  session_id: number
  total_amount: number
}

export interface LoginRequest {
  store_code: string
  table_number: number
  password: string
}

export interface LoginResponse {
  token: string
  store_id: number
  table_id: number
  session_id: number | null
}

export interface ApiError {
  detail: string
  status_code?: number
}
