import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useCartStore } from '../store/cartStore'
import { formatCurrency } from '../utils/format'
import Button from '../components/Button'
import EmptyState from '../components/EmptyState'
import BottomBar from '../components/BottomBar'

export default function CartPage() {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const { items, updateQuantity, clearCart, totalAmount, totalCount, isEmpty } =
    useCartStore()

  return (
    <div className="min-h-screen bg-gray-50 pb-24">
      <header className="bg-white border-b border-gray-200 px-4 py-4 flex items-center gap-3">
        <button
          onClick={() => navigate('/')}
          className="min-h-touch min-w-touch flex items-center justify-center text-gray-600"
          aria-label={t('common.back')}
          data-testid="cart-back-button"
        >
          ←
        </button>
        <h1 className="text-lg font-semibold text-gray-900">{t('cart.title')}</h1>
      </header>

      {isEmpty() ? (
        <EmptyState title={t('cart.empty')} description={t('cart.emptyDescription')} />
      ) : (
        <div className="px-4 py-4 space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-500">{t('cart.totalCount', { count: totalCount() })}</span>
            <button
              onClick={clearCart}
              className="text-sm text-red-500 hover:text-red-600 min-h-touch"
              data-testid="cart-clear-button"
            >
              {t('cart.clear')}
            </button>
          </div>

          {items.map((item) => (
            <div
              key={item.menuItem.id}
              className="bg-white rounded-xl p-4 flex items-center gap-4"
              data-testid={`cart-item-${item.menuItem.id}`}
            >
              <div className="flex-1 min-w-0">
                <p className="font-medium text-gray-900 truncate">{item.menuItem.name}</p>
                <p className="text-sm text-gray-500">{formatCurrency(item.menuItem.price)}</p>
              </div>

              <div className="flex items-center gap-2" role="group" aria-label={`${item.menuItem.name} 수량`}>
                <button
                  onClick={() => updateQuantity(item.menuItem.id, item.quantity - 1)}
                  className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-gray-600 hover:bg-gray-200"
                  aria-label="수량 감소"
                  data-testid={`cart-decrease-${item.menuItem.id}`}
                >
                  −
                </button>
                <span className="w-8 text-center font-medium" aria-label={`수량 ${item.quantity}`}>
                  {item.quantity}
                </span>
                <button
                  onClick={() => updateQuantity(item.menuItem.id, item.quantity + 1)}
                  disabled={item.quantity >= 50}
                  className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-gray-600 hover:bg-gray-200 disabled:opacity-40"
                  aria-label="수량 증가"
                  data-testid={`cart-increase-${item.menuItem.id}`}
                >
                  +
                </button>
              </div>

              <p className="font-semibold text-gray-900 w-20 text-right">
                {formatCurrency(item.menuItem.price * item.quantity)}
              </p>
            </div>
          ))}
        </div>
      )}

      <BottomBar>
        <div className="flex items-center justify-between mb-2">
          <span className="text-gray-600">{t('cart.total')}</span>
          <span className="text-xl font-bold text-gray-900">{formatCurrency(totalAmount())}</span>
        </div>
        <Button
          onClick={() => navigate('/order/confirm')}
          disabled={isEmpty()}
          className="w-full"
          size="lg"
          data-testid="cart-order-button"
        >
          {t('cart.order')}
        </Button>
      </BottomBar>
    </div>
  )
}
