import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useCartStore } from '../store/cartStore'
import { useAuthStore } from '../store/authStore'
import { createOrder } from '../api/order'
import { formatCurrency } from '../utils/format'
import Button from '../components/Button'

export default function OrderConfirmPage() {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const { items, totalAmount, clearCart, isEmpty } = useCartStore()
  const { storeId, tableId, sessionId, setSessionId } = useAuthStore()

  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [orderResult, setOrderResult] = useState<{ orderNumber: string } | null>(null)
  const [countdown, setCountdown] = useState(5)
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null)

  useEffect(() => {
    if (isEmpty()) {
      navigate('/cart', { replace: true })
    }
  }, [isEmpty, navigate])

  useEffect(() => {
    if (!orderResult) return
    timerRef.current = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          if (timerRef.current) clearInterval(timerRef.current)
          navigate('/', { replace: true })
          return 0
        }
        return prev - 1
      })
    }, 1000)
    return () => {
      if (timerRef.current) clearInterval(timerRef.current)
    }
  }, [orderResult, navigate])

  const handleConfirm = async () => {
    if (!storeId || !tableId) return
    setIsSubmitting(true)
    setError(null)
    try {
      const response = await createOrder({
        store_id: storeId,
        table_id: tableId,
        session_id: sessionId ?? undefined,
        items: items.map((i) => ({
          menu_item_id: i.menuItem.id,
          quantity: i.quantity,
        })),
      })
      if (response.session_id) {
        setSessionId(response.session_id)
      }
      clearCart()
      setOrderResult({ orderNumber: response.order_number })
    } catch {
      setError(t('error.server'))
      setIsSubmitting(false)
    }
  }

  if (orderResult) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-white px-4" data-testid="order-success">
        <div className="text-center space-y-4">
          <div className="text-6xl">✅</div>
          <h2 className="text-2xl font-bold text-gray-900">{t('order.successTitle')}</h2>
          <p className="text-gray-500">
            {t('order.orderNumber')}: <span className="font-semibold">{orderResult.orderNumber}</span>
          </p>
          <p className="text-sm text-gray-400">
            {t('order.successRedirect', { seconds: countdown })}
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 px-4 py-4 flex items-center gap-3">
        <button
          onClick={() => navigate('/cart')}
          className="min-h-touch min-w-touch flex items-center justify-center text-gray-600"
          aria-label={t('common.back')}
          data-testid="order-confirm-back"
        >
          ←
        </button>
        <h1 className="text-lg font-semibold text-gray-900">{t('order.confirmTitle')}</h1>
      </header>

      <div className="px-4 py-4 space-y-3">
        {items.map((item) => (
          <div key={item.menuItem.id} className="bg-white rounded-xl p-4 flex justify-between items-center">
            <div>
              <p className="font-medium text-gray-900">{item.menuItem.name}</p>
              <p className="text-sm text-gray-500">
                {formatCurrency(item.menuItem.price)} × {item.quantity}
              </p>
            </div>
            <p className="font-semibold">{formatCurrency(item.menuItem.price * item.quantity)}</p>
          </div>
        ))}

        <div className="bg-white rounded-xl p-4 flex justify-between items-center">
          <span className="font-semibold text-gray-900">{t('cart.total')}</span>
          <span className="text-xl font-bold text-primary-600">{formatCurrency(totalAmount())}</span>
        </div>

        {error && (
          <div className="text-center text-sm text-red-600" role="alert">{error}</div>
        )}

        <Button
          onClick={handleConfirm}
          loading={isSubmitting}
          className="w-full"
          size="lg"
          data-testid="order-confirm-button"
        >
          {t('order.confirmButton')}
        </Button>
      </div>
    </div>
  )
}
