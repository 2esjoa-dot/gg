import { useState, useEffect } from 'react'
import { CartItem, MenuItem } from '../types'

const CART_KEY = 'table-order-cart'

export function useCart() {
  const [items, setItems] = useState<CartItem[]>(() => {
    const saved = localStorage.getItem(CART_KEY)
    return saved ? JSON.parse(saved) : []
  })

  useEffect(() => {
    localStorage.setItem(CART_KEY, JSON.stringify(items))
  }, [items])

  const addItem = (menuItem: MenuItem) => {
    setItems(prev => {
      const existing = prev.find(i => i.menuItem.id === menuItem.id)
      if (existing) {
        return prev.map(i =>
          i.menuItem.id === menuItem.id ? { ...i, quantity: i.quantity + 1 } : i
        )
      }
      return [...prev, { menuItem, quantity: 1 }]
    })
  }

  const removeItem = (menuItemId: number) => {
    setItems(prev => prev.filter(i => i.menuItem.id !== menuItemId))
  }

  const updateQuantity = (menuItemId: number, quantity: number) => {
    if (quantity <= 0) {
      removeItem(menuItemId)
      return
    }
    setItems(prev =>
      prev.map(i => (i.menuItem.id === menuItemId ? { ...i, quantity } : i))
    )
  }

  const clearCart = () => setItems([])

  const totalAmount = items.reduce(
    (sum, item) => sum + item.menuItem.price * item.quantity, 0
  )

  const totalCount = items.reduce((sum, item) => sum + item.quantity, 0)

  return { items, addItem, removeItem, updateQuantity, clearCart, totalAmount, totalCount }
}
