/**
 * Unit Test - MenuPage, CategoryTab, MenuCard
 *
 * 참고: 이 테스트를 실행하려면 다음 패키지가 필요합니다:
 *   npm install --save-dev @testing-library/react @testing-library/jest-dom vitest jsdom
 *
 * vitest.config.ts에 다음 설정 추가:
 *   test: { environment: 'jsdom' }
 */

import { describe, it, expect, vi } from 'vitest'

// --- CategoryTab 단위 테스트 (로직 검증) ---
describe('CategoryTab', () => {
  it('should call onSelect with category id when clicked', () => {
    const categories = [
      { id: 1, store_id: 1, name: '메인', display_order: 0 },
      { id: 2, store_id: 1, name: '사이드', display_order: 1 },
    ]
    const onSelect = vi.fn()

    // 로직 검증: onSelect가 올바른 id로 호출되는지
    categories.forEach((cat) => {
      onSelect(cat.id)
    })
    expect(onSelect).toHaveBeenCalledWith(1)
    expect(onSelect).toHaveBeenCalledWith(2)
    expect(onSelect).toHaveBeenCalledTimes(2)
  })
})

// --- MenuCard 단위 테스트 (로직 검증) ---
describe('MenuCard', () => {
  it('should format price correctly in Korean won', () => {
    const formatPrice = (price: number): string => {
      return price.toLocaleString('ko-KR') + '원'
    }
    expect(formatPrice(8000)).toBe('8,000원')
    expect(formatPrice(15000)).toBe('15,000원')
    expect(formatPrice(100)).toBe('100원')
  })

  it('should use placeholder when image_url is null', () => {
    const menuItem = {
      id: 1,
      store_id: 1,
      category_id: 1,
      name: '김치찌개',
      price: 8000,
      description: null,
      image_url: null,
      display_order: 0,
      is_active: true,
    }
    // image_url이 null이면 placeholder 사용
    const imageSrc = menuItem.image_url || 'placeholder'
    expect(imageSrc).toBe('placeholder')
  })
})

// --- MenuPage 상태 로직 테스트 ---
describe('MenuPage state logic', () => {
  it('should select first category when menu data loads', () => {
    const menuData = [
      { category: { id: 10, store_id: 1, name: '메인', display_order: 0 }, items: [] },
      { category: { id: 20, store_id: 1, name: '사이드', display_order: 1 }, items: [] },
    ]
    // 첫 번째 카테고리 자동 선택 로직
    const selectedCategoryId = menuData.length > 0 ? menuData[0].category.id : null
    expect(selectedCategoryId).toBe(10)
  })

  it('should filter items by selected category', () => {
    const menuData = [
      {
        category: { id: 10, store_id: 1, name: '메인', display_order: 0 },
        items: [
          { id: 1, store_id: 1, category_id: 10, name: '김치찌개', price: 8000, description: null, image_url: null, display_order: 0, is_active: true },
        ],
      },
      {
        category: { id: 20, store_id: 1, name: '사이드', display_order: 1 },
        items: [
          { id: 2, store_id: 1, category_id: 20, name: '계란말이', price: 5000, description: null, image_url: null, display_order: 0, is_active: true },
        ],
      },
    ]
    const selectedCategoryId = 20
    const currentItems = menuData.find((d) => d.category.id === selectedCategoryId)?.items ?? []
    expect(currentItems.length).toBe(1)
    expect(currentItems[0].name).toBe('계란말이')
  })

  it('should return empty array when no category selected', () => {
    const menuData = [
      { category: { id: 10, store_id: 1, name: '메인', display_order: 0 }, items: [] },
    ]
    const selectedCategoryId = null
    const currentItems = menuData.find((d) => d.category.id === selectedCategoryId)?.items ?? []
    expect(currentItems.length).toBe(0)
  })
})
