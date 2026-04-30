import { apiRequest } from './client'
import type { Category, MenuItem } from '../types'

interface CategoryWithItems {
  category: Category
  items: MenuItem[]
}

export async function fetchCategories(): Promise<Category[]> {
  return apiRequest<Category[]>('/customer/menu/categories')
}

export async function fetchMenu(): Promise<CategoryWithItems[]> {
  return apiRequest<CategoryWithItems[]>('/customer/menu/')
}
