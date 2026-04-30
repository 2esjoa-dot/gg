import { http, HttpResponse } from 'msw'

const mockTables = [
  { id: 1, store_id: 1, table_number: 1, session_active: true, current_total: 27000 },
  { id: 2, store_id: 1, table_number: 2, session_active: false, current_total: 0 },
  { id: 3, store_id: 1, table_number: 3, session_active: true, current_total: 15000 },
]

const mockMenuItems = [
  { id: 1, store_id: 1, category_id: 1, name: '시그니처 버거', price: 12000, description: '특제 소스', image_url: null, display_order: 1, is_active: true },
  { id: 2, store_id: 1, category_id: 1, name: '치즈 피자', price: 15000, description: '모짜렐라', image_url: null, display_order: 2, is_active: true },
]

const mockCategories = [
  { id: 1, store_id: 1, name: '인기 메뉴', display_order: 1 },
  { id: 2, store_id: 1, name: '메인', display_order: 2 },
]

const mockStores = [
  { id: 1, name: '강남점', code: 'gangnam', address: '서울시 강남구', created_at: '2026-01-15T00:00:00Z' },
  { id: 2, name: '홍대점', code: 'hongdae', address: '서울시 마포구', created_at: '2026-02-20T00:00:00Z' },
]

export const handlers = [
  http.post('/api/admin/auth/login', async ({ request }) => {
    const body = await request.json() as Record<string, unknown>
    if (body.password === 'wrong') {
      return HttpResponse.json({ detail: '인증 정보가 올바르지 않습니다' }, { status: 401 })
    }
    return HttpResponse.json({
      token: 'mock-admin-jwt',
      role: body.username === 'hqadmin' ? 'hq_admin' : 'store_admin',
      store_id: 1,
      username: body.username,
    })
  }),

  http.post('/api/admin/auth/register', async ({ request }) => {
    const body = await request.json() as Record<string, unknown>
    if (body.username === 'existing') {
      return HttpResponse.json({ detail: '이미 존재하는 사용자명입니다' }, { status: 409 })
    }
    return HttpResponse.json({ id: 10, username: body.username })
  }),

  http.get('/api/admin/tables', () => HttpResponse.json(mockTables)),
  http.post('/api/admin/tables', async ({ request }) => {
    const body = await request.json() as Record<string, unknown>
    return HttpResponse.json({ id: 10, store_id: 1, table_number: body.table_number, session_active: false, current_total: 0 })
  }),
  http.post('/api/admin/tables/:tableId/complete', () => HttpResponse.json(null, { status: 200 })),
  http.get('/api/admin/tables/:tableId/history', () => HttpResponse.json([])),

  http.get('/api/admin/menu', () => HttpResponse.json(mockMenuItems)),
  http.get('/api/admin/menu/categories', () => HttpResponse.json(mockCategories)),
  http.post('/api/admin/menu', async ({ request }) => {
    const body = await request.json() as Record<string, unknown>
    return HttpResponse.json({ id: 10, store_id: 1, ...body, display_order: 99, is_active: true })
  }),
  http.put('/api/admin/menu/:itemId', async ({ request, params }) => {
    const body = await request.json() as Record<string, unknown>
    return HttpResponse.json({ id: Number(params.itemId), store_id: 1, ...body })
  }),
  http.delete('/api/admin/menu/:itemId', () => HttpResponse.json(null, { status: 200 })),
  http.patch('/api/admin/menu/order', () => HttpResponse.json(null, { status: 200 })),
  http.post('/api/admin/menu/upload-image', () => HttpResponse.json({ image_url: '/uploads/mock-image.jpg' })),

  http.get('/api/hq/stores', () => HttpResponse.json(mockStores)),
  http.post('/api/hq/stores', async ({ request }) => {
    const body = await request.json() as Record<string, unknown>
    return HttpResponse.json({ id: 10, ...body, created_at: new Date().toISOString() })
  }),
]
