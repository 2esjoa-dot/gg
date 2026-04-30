import { apiGet } from './client'
import type { Category, MenuItem } from '../types'

export function getMenuByStore(storeId: number): Promise<{ categories: Category[]; items: MenuItem[] }> {
  return apiGet(`/customer/menu/${storeId}`)
}
