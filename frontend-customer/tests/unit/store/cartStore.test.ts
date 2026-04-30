import { describe, it, expect, beforeEach } from 'vitest'
import { useCartStore } from '../../../src/store/cartStore'
import type { MenuItem } from '../../../src/types'

const mockItem: MenuItem = {
  id: 1,
  store_id: 1,
  category_id: 1,
  name: '시그니처 버거',
  price: 12000,
  description: null,
  image_url: null,
  display_order: 1,
  is_active: true,
}

const mockItem2: MenuItem = {
  id: 2,
  store_id: 1,
  category_id: 1,
  name: '치즈 피자',
  price: 15000,
  description: null,
  image_url: null,
  display_order: 2,
  is_active: true,
}

describe('cartStore', () => {
  beforeEach(() => {
    useCartStore.getState().clearCart()
  })

  it('아이템을 추가할 수 있다', () => {
    useCartStore.getState().addItem(mockItem)
    expect(useCartStore.getState().items).toHaveLength(1)
    expect(useCartStore.getState().items[0].quantity).toBe(1)
  })

  it('동일 아이템 추가 시 수량이 증가한다', () => {
    useCartStore.getState().addItem(mockItem)
    useCartStore.getState().addItem(mockItem)
    expect(useCartStore.getState().items).toHaveLength(1)
    expect(useCartStore.getState().items[0].quantity).toBe(2)
  })

  it('아이템당 최대 수량은 50개이다', () => {
    useCartStore.getState().addItem(mockItem)
    useCartStore.getState().updateQuantity(1, 50)
    useCartStore.getState().addItem(mockItem)
    expect(useCartStore.getState().items[0].quantity).toBe(50)
  })

  it('수량을 0 이하로 변경하면 아이템이 삭제된다', () => {
    useCartStore.getState().addItem(mockItem)
    useCartStore.getState().updateQuantity(1, 0)
    expect(useCartStore.getState().items).toHaveLength(0)
  })

  it('아이템을 삭제할 수 있다', () => {
    useCartStore.getState().addItem(mockItem)
    useCartStore.getState().addItem(mockItem2)
    useCartStore.getState().removeItem(1)
    expect(useCartStore.getState().items).toHaveLength(1)
    expect(useCartStore.getState().items[0].menuItem.id).toBe(2)
  })

  it('장바구니를 비울 수 있다', () => {
    useCartStore.getState().addItem(mockItem)
    useCartStore.getState().addItem(mockItem2)
    useCartStore.getState().clearCart()
    expect(useCartStore.getState().items).toHaveLength(0)
  })

  it('총액을 올바르게 계산한다', () => {
    useCartStore.getState().addItem(mockItem)
    useCartStore.getState().addItem(mockItem2)
    useCartStore.getState().updateQuantity(1, 2)
    expect(useCartStore.getState().totalAmount()).toBe(12000 * 2 + 15000)
  })

  it('총 수량을 올바르게 계산한다', () => {
    useCartStore.getState().addItem(mockItem)
    useCartStore.getState().addItem(mockItem2)
    useCartStore.getState().updateQuantity(1, 3)
    expect(useCartStore.getState().totalCount()).toBe(4)
  })

  it('빈 장바구니를 올바르게 감지한다', () => {
    expect(useCartStore.getState().isEmpty()).toBe(true)
    useCartStore.getState().addItem(mockItem)
    expect(useCartStore.getState().isEmpty()).toBe(false)
  })
})
