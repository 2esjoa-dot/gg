import { describe, it, expect, beforeEach } from 'vitest'
import { useAuthStore } from '../../../src/store/authStore'

describe('authStore', () => {
  beforeEach(() => {
    useAuthStore.getState().logout()
  })

  it('로그인 시 인증 정보가 저장된다', () => {
    useAuthStore.getState().login({
      token: 'test-token',
      storeId: 1,
      tableId: 5,
      storeCode: 'gangnam',
      tableNumber: 5,
      sessionId: 10,
    })

    const state = useAuthStore.getState()
    expect(state.token).toBe('test-token')
    expect(state.storeId).toBe(1)
    expect(state.tableId).toBe(5)
    expect(state.isAuthenticated()).toBe(true)
  })

  it('로그아웃 시 인증 정보가 초기화된다', () => {
    useAuthStore.getState().login({
      token: 'test-token',
      storeId: 1,
      tableId: 5,
      storeCode: 'gangnam',
      tableNumber: 5,
      sessionId: 10,
    })
    useAuthStore.getState().logout()

    expect(useAuthStore.getState().token).toBeNull()
    expect(useAuthStore.getState().isAuthenticated()).toBe(false)
  })

  it('세션 ID를 업데이트할 수 있다', () => {
    useAuthStore.getState().login({
      token: 'test-token',
      storeId: 1,
      tableId: 5,
      storeCode: 'gangnam',
      tableNumber: 5,
      sessionId: null,
    })
    useAuthStore.getState().setSessionId(20)
    expect(useAuthStore.getState().sessionId).toBe(20)
  })
})
