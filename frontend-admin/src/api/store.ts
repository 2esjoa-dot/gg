import { apiGet, apiPost } from './client'
import type { Store, CreateStoreRequest } from '../types'

export function getStores(): Promise<Store[]> {
  return apiGet<Store[]>('/hq/stores')
}

export function createStore(data: CreateStoreRequest): Promise<Store> {
  return apiPost<Store>('/hq/stores', data)
}
