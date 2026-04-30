import { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { getMenuItems, getCategories, createMenuItem, updateMenuItem, deleteMenuItem, uploadMenuImage } from '../api/menu'
import { formatCurrency } from '../utils/format'
import type { MenuItem, Category } from '../types'

const menuSchema = z.object({
  name: z.string().min(1, 'menu.nameRequired').max(100),
  price: z.coerce.number().int().positive('menu.pricePositive'),
  description: z.string().max(500).optional(),
  category_id: z.coerce.number().positive('menu.categoryRequired'),
  is_active: z.boolean().optional(),
})

type MenuFormData = z.infer<typeof menuSchema>

export default function MenuManagePage() {
  const { t } = useTranslation()
  const [items, setItems] = useState<MenuItem[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingItem, setEditingItem] = useState<MenuItem | null>(null)
  const [deleteId, setDeleteId] = useState<number | null>(null)
  const [imageFile, setImageFile] = useState<File | null>(null)

  const { register, handleSubmit, reset, formState: { errors } } = useForm<MenuFormData>({
    resolver: zodResolver(menuSchema),
  })

  const loadData = async () => {
    try {
      const [menuData, catData] = await Promise.all([getMenuItems(), getCategories()])
      setItems(menuData)
      setCategories(catData)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => { loadData() }, [])

  const openCreate = () => {
    setEditingItem(null)
    reset({ name: '', price: 0, description: '', category_id: 0, is_active: true })
    setImageFile(null)
    setShowForm(true)
  }

  const openEdit = (item: MenuItem) => {
    setEditingItem(item)
    reset({ name: item.name, price: item.price, description: item.description || '', category_id: item.category_id, is_active: item.is_active })
    setImageFile(null)
    setShowForm(true)
  }

  const onSubmit = async (data: MenuFormData) => {
    let imageUrl: string | undefined
    if (imageFile) {
      const result = await uploadMenuImage(imageFile)
      imageUrl = result.image_url
    }

    if (editingItem) {
      await updateMenuItem(editingItem.id, { ...data, image_url: imageUrl })
    } else {
      await createMenuItem({ ...data, image_url: imageUrl })
    }
    setShowForm(false)
    loadData()
  }

  const handleDelete = async () => {
    if (!deleteId) return
    await deleteMenuItem(deleteId)
    setDeleteId(null)
    loadData()
  }

  if (isLoading) return <div className="flex justify-center py-12"><div className="animate-spin h-8 w-8 border-4 border-primary-600 border-t-transparent rounded-full" /></div>

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-900">{t('menu.title')}</h2>
        <button onClick={openCreate} className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 text-sm font-medium" data-testid="add-menu-button">
          {t('menu.addMenu')}
        </button>
      </div>

      <div className="bg-white rounded-xl overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">{t('menu.menuName')}</th>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">{t('menu.category')}</th>
              <th className="px-4 py-3 text-right text-sm font-medium text-gray-500">{t('menu.price')}</th>
              <th className="px-4 py-3 text-center text-sm font-medium text-gray-500">상태</th>
              <th className="px-4 py-3 text-right text-sm font-medium text-gray-500">작업</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {items.map((item) => (
              <tr key={item.id} data-testid={`menu-row-${item.id}`}>
                <td className="px-4 py-3 font-medium">{item.name}</td>
                <td className="px-4 py-3 text-sm text-gray-500">{categories.find((c) => c.id === item.category_id)?.name}</td>
                <td className="px-4 py-3 text-right">{formatCurrency(item.price)}</td>
                <td className="px-4 py-3 text-center">
                  <span className={`text-xs font-medium ${item.is_active ? 'text-green-600' : 'text-gray-400'}`}>
                    {item.is_active ? t('menu.active') : t('menu.inactive')}
                  </span>
                </td>
                <td className="px-4 py-3 text-right space-x-2">
                  <button onClick={() => openEdit(item)} className="text-sm text-primary-600 hover:text-primary-700" data-testid={`edit-menu-${item.id}`}>{t('common.edit')}</button>
                  <button onClick={() => setDeleteId(item.id)} className="text-sm text-red-600 hover:text-red-700" data-testid={`delete-menu-${item.id}`}>{t('common.delete')}</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showForm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" role="dialog" aria-modal="true">
          <div className="bg-white rounded-2xl p-6 w-full max-w-md mx-4">
            <h3 className="text-lg font-semibold mb-4">{editingItem ? t('menu.editMenu') : t('menu.addMenu')}</h3>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-3" data-testid="menu-form">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">{t('menu.menuName')} *</label>
                <input {...register('name')} className="w-full px-4 py-2.5 border border-gray-300 rounded-xl" data-testid="menu-form-name" />
                {errors.name && <p className="mt-1 text-sm text-red-600">{t(errors.name.message!)}</p>}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">{t('menu.price')} *</label>
                <input type="number" {...register('price')} className="w-full px-4 py-2.5 border border-gray-300 rounded-xl" data-testid="menu-form-price" />
                {errors.price && <p className="mt-1 text-sm text-red-600">{t(errors.price.message!)}</p>}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">{t('menu.category')} *</label>
                <select {...register('category_id')} className="w-full px-4 py-2.5 border border-gray-300 rounded-xl" data-testid="menu-form-category">
                  <option value="">{t('menu.categoryRequired')}</option>
                  {categories.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
                </select>
                {errors.category_id && <p className="mt-1 text-sm text-red-600">{t(errors.category_id.message!)}</p>}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">{t('menu.description')}</label>
                <textarea {...register('description')} rows={3} className="w-full px-4 py-2.5 border border-gray-300 rounded-xl" data-testid="menu-form-description" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">{t('menu.image')}</label>
                <input type="file" accept="image/jpeg,image/png,image/webp" onChange={(e) => setImageFile(e.target.files?.[0] || null)} className="w-full text-sm" data-testid="menu-form-image" />
              </div>
              <div className="flex gap-3 pt-2">
                <button type="button" onClick={() => setShowForm(false)} className="flex-1 py-2.5 border border-gray-300 rounded-xl text-gray-700">{t('common.cancel')}</button>
                <button type="submit" className="flex-1 py-2.5 bg-primary-600 text-white rounded-xl hover:bg-primary-700" data-testid="menu-form-submit">{t('common.save')}</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {deleteId && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" role="dialog" aria-modal="true">
          <div className="bg-white rounded-2xl p-6 w-full max-w-sm mx-4 text-center">
            <p className="text-gray-900 mb-4">{t('menu.deleteConfirm')}</p>
            <div className="flex gap-3">
              <button onClick={() => setDeleteId(null)} className="flex-1 py-2.5 border border-gray-300 rounded-xl">{t('common.cancel')}</button>
              <button onClick={handleDelete} className="flex-1 py-2.5 bg-red-600 text-white rounded-xl hover:bg-red-700" data-testid="confirm-delete-menu">{t('common.confirm')}</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
