import { describe, it, expect, beforeEach } from 'vitest'
import { useAdminAuthStore } from '../../../src/store/authStore'

describe('adminAuthStore', () => {
  beforeEach(() => {
    useAdminAuthStore.getState().logout()
  })

  it('로그인 시 관리자 정보가 저장된다', () => {
    useAdminAuthStore.getState().login({
      token: 'admin-token',
      role: 'store_admin',
      storeId: 1,
      username: 'admin1',
    })

    const state = useAdminAuthStore.getState()
    expect(state.token).toBe('admin-token')
    expect(state.role).toBe('store_admin')
    expect(state.isAuthenticated()).toBe(true)
    expect(state.isHQAdmin()).toBe(false)
  })

  it('본사 관리자 역할을 올바르게 감지한다', () => {
    useAdminAuthStore.getState().login({
      token: 'hq-token',
      role: 'hq_admin',
      storeId: 0,
      username: 'hqadmin',
    })

    expect(useAdminAuthStore.getState().isHQAdmin()).toBe(true)
  })

  it('로그아웃 시 정보가 초기화된다', () => {
    useAdminAuthStore.getState().login({
      token: 'admin-token',
      role: 'store_admin',
      storeId: 1,
      username: 'admin1',
    })
    useAdminAuthStore.getState().logout()

    expect(useAdminAuthStore.getState().token).toBeNull()
    expect(useAdminAuthStore.getState().role).toBeNull()
    expect(useAdminAuthStore.getState().isAuthenticated()).toBe(false)
  })
})
