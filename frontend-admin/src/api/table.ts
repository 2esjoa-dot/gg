import { apiGet, apiPost } from './client'
import type { Table, CreateTableRequest, HistoryOrder } from '../types'

export function getTables(): Promise<Table[]> {
  return apiGet<Table[]>('/admin/tables')
}

export function createTable(data: CreateTableRequest): Promise<Table> {
  return apiPost<Table>('/admin/tables', data)
}

export function completeTable(tableId: number): Promise<void> {
  return apiPost(`/admin/tables/${tableId}/complete`)
}

export function getTableHistory(tableId: number, from?: string, to?: string): Promise<HistoryOrder[]> {
  const params = new URLSearchParams()
  if (from) params.set('from', from)
  if (to) params.set('to', to)
  const query = params.toString() ? `?${params.toString()}` : ''
  return apiGet<HistoryOrder[]>(`/admin/tables/${tableId}/history${query}`)
}
