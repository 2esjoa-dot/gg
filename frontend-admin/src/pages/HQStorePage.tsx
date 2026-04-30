import { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { getStores, createStore } from '../api/store'
import { formatDate } from '../utils/format'
import type { Store } from '../types'
import { ApiError } from '../api/client'

export default function HQStorePage() {
  const { t } = useTranslation()
  const [stores, setStores] = useState<Store[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [search, setSearch] = useState('')
  const [formData, setFormData] = useState({ name: '', code: '', address: '' })
  const [error, setError] = useState<string | null>(null)

  const loadStores = async () => {
    try {
      const data = await getStores()
      setStores(data)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => { loadStores() }, [])

  const handleCreate = async () => {
    setError(null)
    if (!formData.name || !formData.code) return
    try {
      await createStore(formData)
      setShowModal(false)
      setFormData({ name: '', code: '', address: '' })
      loadStores()
    } catch (err) {
      if (err instanceof ApiError && err.statusCode === 409) {
        setError(t('store.duplicateError'))
      }
    }
  }

  const filteredStores = stores.filter(
    (s) => s.name.includes(search) || s.code.includes(search)
  )

  if (isLoading) return <div className="flex justify-center py-12"><div className="animate-spin h-8 w-8 border-4 border-primary-600 border-t-transparent rounded-full" /></div>

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-900">{t('store.title')}</h2>
        <button onClick={() => setShowModal(true)} className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 text-sm font-medium" data-testid="add-store-button">
          {t('store.addStore')}
        </button>
      </div>

      <div className="mb-4">
        <input
          type="text"
          placeholder={t('common.search')}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full max-w-xs px-4 py-2.5 border border-gray-300 rounded-xl"
          data-testid="store-search"
        />
      </div>

      <div className="bg-white rounded-xl overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">{t('store.storeName')}</th>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">{t('store.storeCode')}</th>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">{t('store.address')}</th>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">{t('store.createdAt')}</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {filteredStores.map((store) => (
              <tr key={store.id} data-testid={`store-row-${store.id}`}>
                <td className="px-4 py-3 font-medium">{store.name}</td>
                <td className="px-4 py-3 text-sm text-gray-500">{store.code}</td>
                <td className="px-4 py-3 text-sm text-gray-500">{store.address || '-'}</td>
                <td className="px-4 py-3 text-sm text-gray-500">{formatDate(store.created_at)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" role="dialog" aria-modal="true">
          <div className="bg-white rounded-2xl p-6 w-full max-w-sm mx-4">
            <h3 className="text-lg font-semibold mb-4">{t('store.addStore')}</h3>
            <div className="space-y-3">
              <input placeholder={t('store.storeName') + ' *'} value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} className="w-full px-4 py-2.5 border border-gray-300 rounded-xl" data-testid="store-form-name" />
              <input placeholder={t('store.storeCode') + ' *'} value={formData.code} onChange={(e) => setFormData({ ...formData, code: e.target.value })} className="w-full px-4 py-2.5 border border-gray-300 rounded-xl" data-testid="store-form-code" />
              <input placeholder={t('store.address')} value={formData.address} onChange={(e) => setFormData({ ...formData, address: e.target.value })} className="w-full px-4 py-2.5 border border-gray-300 rounded-xl" data-testid="store-form-address" />
              {error && <p className="text-sm text-red-600">{error}</p>}
            </div>
            <div className="flex gap-3 mt-4">
              <button onClick={() => setShowModal(false)} className="flex-1 py-2.5 border border-gray-300 rounded-xl text-gray-700">{t('common.cancel')}</button>
              <button onClick={handleCreate} className="flex-1 py-2.5 bg-primary-600 text-white rounded-xl hover:bg-primary-700" data-testid="store-form-submit">{t('common.save')}</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
