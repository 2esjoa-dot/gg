import { apiGet, apiPost } from './client'
import type { CreateOrderRequest, CreateOrderResponse, Order } from '../types'

export function createOrder(data: CreateOrderRequest): Promise<CreateOrderResponse> {
  return apiPost<CreateOrderResponse>('/customer/orders', data)
}

export function getOrdersBySession(sessionId: number): Promise<Order[]> {
  return apiGet<Order[]>(`/customer/orders/session/${sessionId}`)
}
