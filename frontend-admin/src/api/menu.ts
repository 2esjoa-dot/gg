import { apiGet, apiPost, apiPut, apiDelete, apiPatch, apiUpload } from './client'
import type { MenuItem, Category, CreateMenuItemRequest, UpdateMenuItemRequest, UpdateMenuOrderRequest } from '../types'

export function getMenuItems(): Promise<MenuItem[]> {
  return apiGet<MenuItem[]>('/admin/menu')
}

export function getCategories(): Promise<Category[]> {
  return apiGet<Category[]>('/admin/menu/categories')
}

export function createMenuItem(data: CreateMenuItemRequest): Promise<MenuItem> {
  return apiPost<MenuItem>('/admin/menu', data)
}

export function updateMenuItem(itemId: number, data: UpdateMenuItemRequest): Promise<MenuItem> {
  return apiPut<MenuItem>(`/admin/menu/${itemId}`, data)
}

export function deleteMenuItem(itemId: number): Promise<void> {
  return apiDelete(`/admin/menu/${itemId}`)
}

export function updateMenuOrder(data: UpdateMenuOrderRequest): Promise<void> {
  return apiPatch('/admin/menu/order', data)
}

export function uploadMenuImage(file: File): Promise<{ image_url: string }> {
  return apiUpload('/admin/menu/upload-image', file)
}
