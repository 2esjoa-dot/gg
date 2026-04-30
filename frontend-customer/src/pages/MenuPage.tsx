import { useState, useEffect, memo } from 'react'
import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAuthStore } from '../store/authStore'
import { useCartStore } from '../store/cartStore'
import { getMenuByStore } from '../api/menu'
import { formatCurrency } from '../utils/format'
import type { Category, MenuItem } from '../types'
import Loading from '../components/Loading'
import ErrorMessage from '../components/ErrorMessage'
import Modal from '../components/Modal'
import Button from '../components/Button'

const MenuCard = memo(function MenuCard({
  item,
  onAdd,
  onDetail,
}: {
  item: MenuItem
  onAdd: (item: MenuItem) => void
  onDetail: (item: MenuItem) => void
}) {
  return (
    <div
      className="bg-white rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow cursor-pointer"
      onClick={() => onDetail(item)}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === 'Enter' && onDetail(item)}
      data-testid={`menu-card-${item.id}`}
    >
      <div className="aspect-[4/3] bg-gray-100 flex items-center justify-center">
        {item.image_url ? (
          <img src={item.image_url} alt={item.name} className="w-full h-full object-cover" loading="lazy" />
        ) : (
          <span className="text-4xl">🍽️</span>
        )}
      </div>
      <div className="p-3">
        <p className="font-medium text-gray-900 truncate">{item.name}</p>
        <div className="flex items-center justify-between mt-2">
          <span className="font-semibold text-primary-600">{formatCurrency(item.price)}</span>
          <button
            onClick={(e) => {
              e.stopPropagation()
              onAdd(item)
            }}
            className="px-3 py-1.5 bg-primary-600 text-white text-sm rounded-lg hover:bg-primary-700 min-h-touch"
            data-testid={`menu-add-${item.id}`}
          >
            담기
          </button>
        </div>
      </div>
    </div>
  )
})

export default function MenuPage() {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const storeId = useAuthStore((s) => s.storeId)
  const addItem = useCartStore((s) => s.addItem)
  const cartCount = useCartStore((s) => s.totalCount())

  const [categories, setCategories] = useState<Category[]>([])
  const [items, setItems] = useState<MenuItem[]>([])
  const [activeCategory, setActiveCategory] = useState<number | null>(null)
  const [selectedItem, setSelectedItem] = useState<MenuItem | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!storeId) return
    setIsLoading(true)
    getMenuByStore(storeId)
      .then((data) => {
        setCategories(data.categories)
        setItems(data.items.filter((i) => i.is_active))
        if (data.categories.length > 0) setActiveCategory(data.categories[0].id)
      })
      .catch(() => setError(t('error.server')))
      .finally(() => setIsLoading(false))
  }, [storeId, t])

  const filteredItems = activeCategory
    ? items.filter((i) => i.category_id === activeCategory)
    : items

  if (isLoading) return <Loading size="lg" />
  if (error) return <ErrorMessage message={error} onRetry={() => window.location.reload()} />

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between">
        <h1 className="text-lg font-semibold text-gray-900">{t('menu.title')}</h1>
        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate('/orders')}
            className="text-sm text-gray-500 hover:text-gray-700 min-h-touch px-2"
            data-testid="menu-orders-button"
          >
            {t('order.historyTitle')}
          </button>
          <button
            onClick={() => navigate('/cart')}
            className="relative min-h-touch min-w-touch flex items-center justify-center"
            aria-label={`장바구니 ${cartCount}개`}
            data-testid="menu-cart-button"
          >
            🛒
            {cartCount > 0 && (
              <span className="absolute -top-1 -right-1 bg-primary-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                {cartCount}
              </span>
            )}
          </button>
        </div>
      </header>

      <div className="overflow-x-auto border-b border-gray-200 bg-white" role="tablist">
        <div className="flex px-4 gap-1">
          {categories.map((cat) => (
            <button
              key={cat.id}
              role="tab"
              aria-selected={activeCategory === cat.id}
              onClick={() => setActiveCategory(cat.id)}
              className={`px-4 py-3 text-sm font-medium whitespace-nowrap border-b-2 transition-colors min-h-touch ${
                activeCategory === cat.id
                  ? 'border-primary-600 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
              data-testid={`category-tab-${cat.id}`}
            >
              {cat.name}
            </button>
          ))}
        </div>
      </div>

      <div className="p-4 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {filteredItems.map((item) => (
          <MenuCard
            key={item.id}
            item={item}
            onAdd={addItem}
            onDetail={setSelectedItem}
          />
        ))}
      </div>

      <Modal isOpen={!!selectedItem} onClose={() => setSelectedItem(null)} title={selectedItem?.name}>
        {selectedItem && (
          <div className="space-y-4">
            <div className="aspect-video bg-gray-100 rounded-lg flex items-center justify-center">
              {selectedItem.image_url ? (
                <img src={selectedItem.image_url} alt={selectedItem.name} className="w-full h-full object-cover rounded-lg" />
              ) : (
                <span className="text-6xl">🍽️</span>
              )}
            </div>
            {selectedItem.description && (
              <p className="text-gray-600">{selectedItem.description}</p>
            )}
            <p className="text-xl font-bold text-primary-600">{formatCurrency(selectedItem.price)}</p>
            <Button
              onClick={() => {
                addItem(selectedItem)
                setSelectedItem(null)
              }}
              className="w-full"
              size="lg"
              data-testid="menu-detail-add"
            >
              {t('menu.addToCartFull')}
            </Button>
          </div>
        )}
      </Modal>
    </div>
  )
}
