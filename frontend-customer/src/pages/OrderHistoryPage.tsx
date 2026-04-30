import { useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAuthStore } from '../store/authStore'
import { getOrdersBySession } from '../api/order'
import { usePolling } from '../hooks/usePolling'
import { formatCurrency, formatDateTime } from '../utils/format'
import { StatusBadge } from '../components/Badge'
import Loading from '../components/Loading'
import EmptyState from '../components/EmptyState'

export default function OrderHistoryPage() {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const sessionId = useAuthStore((s) => s.sessionId)

  const fetcher = useCallback(() => {
    if (!sessionId) return Promise.resolve([])
    return getOrdersBySession(sessionId)
  }, [sessionId])

  const { data: orders, isLoading } = usePolling(fetcher, {
    interval: 30000,
    enabled: !!sessionId,
  })

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 px-4 py-4 flex items-center gap-3">
        <button
          onClick={() => navigate('/')}
          className="min-h-touch min-w-touch flex items-center justify-center text-gray-600"
          aria-label={t('common.back')}
          data-testid="order-history-back"
        >
          ←
        </button>
        <h1 className="text-lg font-semibold text-gray-900">{t('order.historyTitle')}</h1>
      </header>

      {isLoading ? (
        <Loading />
      ) : !orders || orders.length === 0 ? (
        <EmptyState title={t('order.noOrders')} />
      ) : (
        <div className="px-4 py-4 space-y-4">
          {orders.map((order) => (
            <div
              key={order.id}
              className="bg-white rounded-xl p-4 space-y-3"
              data-testid={`order-card-${order.id}`}
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">{order.order_number}</p>
                  <p className="text-xs text-gray-400">{formatDateTime(order.created_at)}</p>
                </div>
                <StatusBadge status={order.status} />
              </div>

              <div className="border-t border-gray-100 pt-3 space-y-1">
                {order.items.map((item) => (
                  <div key={item.id} className="flex justify-between text-sm">
                    <span className="text-gray-600">
                      {item.menu_name} × {item.quantity}
                    </span>
                    <span className="text-gray-900">{formatCurrency(item.subtotal)}</span>
                  </div>
                ))}
              </div>

              <div className="border-t border-gray-100 pt-3 flex justify-between">
                <span className="font-medium text-gray-600">{t('cart.total')}</span>
                <span className="font-bold text-gray-900">{formatCurrency(order.total_amount)}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
