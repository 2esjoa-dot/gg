import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { CartItem, MenuItem } from '../types'

const MAX_ITEM_QUANTITY = 50

interface CartStore {
  items: CartItem[]
  addItem: (menuItem: MenuItem) => void
  removeItem: (menuItemId: number) => void
  updateQuantity: (menuItemId: number, quantity: number) => void
  clearCart: () => void
  totalAmount: () => number
  totalCount: () => number
  isEmpty: () => boolean
}

export const useCartStore = create<CartStore>()(
  persist(
    (set, get) => ({
      items: [],

      addItem: (menuItem: MenuItem) => {
        set((state) => {
          const existing = state.items.find((i) => i.menuItem.id === menuItem.id)
          if (existing) {
            if (existing.quantity >= MAX_ITEM_QUANTITY) return state
            return {
              items: state.items.map((i) =>
                i.menuItem.id === menuItem.id
                  ? { ...i, quantity: i.quantity + 1 }
                  : i
              ),
            }
          }
          return { items: [...state.items, { menuItem, quantity: 1 }] }
        })
      },

      removeItem: (menuItemId: number) => {
        set((state) => ({
          items: state.items.filter((i) => i.menuItem.id !== menuItemId),
        }))
      },

      updateQuantity: (menuItemId: number, quantity: number) => {
        if (quantity <= 0) {
          get().removeItem(menuItemId)
          return
        }
        if (quantity > MAX_ITEM_QUANTITY) return
        set((state) => ({
          items: state.items.map((i) =>
            i.menuItem.id === menuItemId ? { ...i, quantity } : i
          ),
        }))
      },

      clearCart: () => set({ items: [] }),

      totalAmount: () =>
        get().items.reduce((sum, item) => sum + item.menuItem.price * item.quantity, 0),

      totalCount: () =>
        get().items.reduce((sum, item) => sum + item.quantity, 0),

      isEmpty: () => get().items.length === 0,
    }),
    {
      name: 'table-order-cart',
    }
  )
)
