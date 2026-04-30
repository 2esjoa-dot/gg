import { http, HttpResponse } from 'msw'

const mockCategories = [
  { id: 1, store_id: 1, name: '인기 메뉴', display_order: 1 },
  { id: 2, store_id: 1, name: '메인', display_order: 2 },
  { id: 3, store_id: 1, name: '사이드', display_order: 3 },
  { id: 4, store_id: 1, name: '음료', display_order: 4 },
]

const mockMenuItems = [
  { id: 1, store_id: 1, category_id: 1, name: '시그니처 버거', price: 12000, description: '특제 소스와 신선한 재료', image_url: null, display_order: 1, is_active: true },
  { id: 2, store_id: 1, category_id: 1, name: '치즈 피자', price: 15000, description: '모짜렐라 치즈 듬뿍', image_url: null, display_order: 2, is_active: true },
  { id: 3, store_id: 1, category_id: 2, name: '스테이크', price: 25000, description: '프리미엄 안심 스테이크', image_url: null, display_order: 1, is_active: true },
  { id: 4, store_id: 1, category_id: 3, name: '감자튀김', price: 5000, description: '바삭한 감자튀김', image_url: null, display_order: 1, is_active: true },
  { id: 5, store_id: 1, category_id: 4, name: '콜라', price: 2000, description: null, image_url: null, display_order: 1, is_active: true },
]

let orderIdCounter = 100
const mockOrders: Record<string, unknown[]> = {}

export const handlers = [
  http.post('/api/customer/auth/login', async ({ request }) => {
    const body = await request.json() as Record<string, unknown>
    if (body.password === 'wrong') {
      return HttpResponse.json({ detail: '인증 정보가 올바르지 않습니다' }, { status: 401 })
    }
    return HttpResponse.json({
      token: 'mock-jwt-token',
      store_id: 1,
      table_id: Number(body.table_number) || 1,
      session_id: 1,
    })
  }),

  http.get('/api/customer/menu/:storeId', () => {
    return HttpResponse.json({ categories: mockCategories, items: mockMenuItems })
  }),

  http.post('/api/customer/orders', async ({ request }) => {
    const body = await request.json() as Record<string, unknown>
    orderIdCounter++
    const orderNumber = `ORD-${Date.now()}-${orderIdCounter}`
    const sessionId = (body.session_id as number) || 1
    const key = String(sessionId)
    if (!mockOrders[key]) mockOrders[key] = []
    mockOrders[key].push({
      id: orderIdCounter,
      order_number: orderNumber,
      status: 'pending',
      total_amount: 0,
      items: [],
      created_at: new Date().toISOString(),
    })
    return HttpResponse.json({ id: orderIdCounter, order_number: orderNumber, session_id: sessionId, total_amount: 0 })
  }),

  http.get('/api/customer/orders/session/:sessionId', () => {
    return HttpResponse.json([
      {
        id: 1,
        order_number: 'ORD-MOCK-001',
        status: 'preparing',
        total_amount: 27000,
        items: [
          { id: 1, menu_item_id: 1, menu_name: '시그니처 버거', quantity: 1, unit_price: 12000, subtotal: 12000 },
          { id: 2, menu_item_id: 2, menu_name: '치즈 피자', quantity: 1, unit_price: 15000, subtotal: 15000 },
        ],
        created_at: new Date(Date.now() - 600000).toISOString(),
      },
    ])
  }),
]
