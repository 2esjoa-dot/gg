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
  status: 'pending' | 'preparing' | 'completed'
  total_amount: number
  items: OrderItem[]
  created_at: string
}

export interface OrderItem {
  id: number
  menu_name: string
  quantity: number
  unit_price: number
  subtotal: number
}
