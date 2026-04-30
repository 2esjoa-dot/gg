import { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { getTables, createTable, completeTable, getTableHistory } from '../api/table'
import { formatCurrency, formatDateTime } from '../utils/format'
import type { Table as TableType, HistoryOrder } from '../types'
import { ApiError } from '../api/client'

export default function TableManagePage() {
  const { t } = useTranslation()
  const [tables, setTables] = useState<TableType[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [showAddModal, setShowAddModal] = useState(false)
  const [confirmTableId, setConfirmTableId] = useState<number | null>(null)
  const [historyTableId, setHistoryTableId] = useState<number | null>(null)
  const [historyOrders, setHistoryOrders] = useState<HistoryOrder[]>([])
  const [addError, setAddError] = useState<string | null>(null)
  const [tableNumber, setTableNumber] = useState('')
  const [password, setPassword] = useState('')

  const loadTables = async () => {
    try {
      const data = await getTables()
      setTables(data)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => { loadTables() }, [])

  const handleAdd = async () => {
    setAddError(null)
    if (!tableNumber || !password || password.length < 4) {
      setAddError(t('table.passwordMin'))
      return
    }
    try {
      await createTable({ table_number: Number(tableNumber), password })
      setShowAddModal(false)
      setTableNumber('')
      setPassword('')
      loadTables()
    } catch (err) {
      if (err instanceof ApiError && err.statusCode === 409) {
        setAddError(t('table.duplicateError'))
      }
    }
  }

  const handleComplete = async (tableId: number) => {
    await completeTable(tableId)
    setConfirmTableId(null)
    loadTables()
  }

  const handleShowHistory = async (tableId: number) => {
    setHistoryTableId(tableId)
    const data = await getTableHistory(tableId)
    setHistoryOrders(data)
  }

  if (isLoading) return <div className="flex justify-center py-12"><div className="animate-spin h-8 w-8 border-4 border-primary-600 border-t-transparent rounded-full" /></div>

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-900">{t('table.title')}</h2>
        <button
          onClick={() => setShowAddModal(true)}
          className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 text-sm font-medium"
          data-testid="add-table-button"
        >
          {t('table.addTable')}
        </button>
      </div>

      <div className="bg-white rounded-xl overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">{t('table.tableNumber')}</th>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">상태</th>
              <th className="px-4 py-3 text-right text-sm font-medium text-gray-500">주문 총액</th>
              <th className="px-4 py-3 text-right text-sm font-medium text-gray-500">작업</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {tables.map((table) => (
              <tr key={table.id} data-testid={`table-row-${table.id}`}>
                <td className="px-4 py-3 font-medium">{table.table_number}번</td>
                <td className="px-4 py-3">
                  <span className={`inline-flex px-2 py-0.5 rounded-full text-xs font-medium ${table.session_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'}`}>
                    {table.session_active ? t('table.sessionActive') : t('table.sessionInactive')}
                  </span>
                </td>
                <td className="px-4 py-3 text-right">{formatCurrency(table.current_total)}</td>
                <td className="px-4 py-3 text-right space-x-2">
                  {table.session_active && (
                    <button
                      onClick={() => setConfirmTableId(table.id)}
                      className="text-sm text-red-600 hover:text-red-700"
                      data-testid={`complete-table-${table.id}`}
                    >
                      {t('table.complete')}
                    </button>
                  )}
                  <button
                    onClick={() => handleShowHistory(table.id)}
                    className="text-sm text-primary-600 hover:text-primary-700"
                    data-testid={`history-table-${table.id}`}
                  >
                    {t('table.history')}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" role="dialog" aria-modal="true">
          <div className="bg-white rounded-2xl p-6 w-full max-w-sm mx-4">
            <h3 className="text-lg font-semibold mb-4">{t('table.addTable')}</h3>
            <div className="space-y-3">
              <input type="number" placeholder={t('table.tableNumber')} value={tableNumber} onChange={(e) => setTableNumber(e.target.value)} className="w-full px-4 py-3 border border-gray-300 rounded-xl" data-testid="add-table-number" />
              <input type="password" placeholder={t('table.password')} value={password} onChange={(e) => setPassword(e.target.value)} className="w-full px-4 py-3 border border-gray-300 rounded-xl" data-testid="add-table-password" />
              {addError && <p className="text-sm text-red-600">{addError}</p>}
            </div>
            <div className="flex gap-3 mt-4">
              <button onClick={() => setShowAddModal(false)} className="flex-1 py-2.5 border border-gray-300 rounded-xl text-gray-700">{t('common.cancel')}</button>
              <button onClick={handleAdd} className="flex-1 py-2.5 bg-primary-600 text-white rounded-xl hover:bg-primary-700" data-testid="add-table-submit">{t('common.save')}</button>
            </div>
          </div>
        </div>
      )}

      {confirmTableId && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" role="dialog" aria-modal="true">
          <div className="bg-white rounded-2xl p-6 w-full max-w-sm mx-4 text-center">
            <p className="text-gray-900 mb-4">{t('table.completeConfirm')}</p>
            <div className="flex gap-3">
              <button onClick={() => setConfirmTableId(null)} className="flex-1 py-2.5 border border-gray-300 rounded-xl">{t('common.cancel')}</button>
              <button onClick={() => handleComplete(confirmTableId)} className="flex-1 py-2.5 bg-red-600 text-white rounded-xl hover:bg-red-700" data-testid="confirm-complete">{t('common.confirm')}</button>
            </div>
          </div>
        </div>
      )}

      {historyTableId !== null && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" role="dialog" aria-modal="true">
          <div className="bg-white rounded-2xl p-6 w-full max-w-lg mx-4 max-h-[80vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold">{t('table.history')}</h3>
              <button onClick={() => setHistoryTableId(null)} className="text-gray-400 hover:text-gray-600">{t('common.close')}</button>
            </div>
            {historyOrders.length === 0 ? (
              <p className="text-center text-gray-500 py-8">{t('table.noHistory')}</p>
            ) : (
              <div className="space-y-3">
                {historyOrders.map((order) => (
                  <div key={order.id} className="border border-gray-200 rounded-lg p-3">
                    <div className="flex justify-between text-sm">
                      <span className="font-medium">{order.order_number}</span>
                      <span className="text-gray-500">{formatDateTime(order.created_at)}</span>
                    </div>
                    <p className="text-right font-semibold mt-1">{formatCurrency(order.total_amount)}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
