import { useState, useEffect } from 'react'
import { fetchMenu } from '../api/menu'
import CategoryTab from '../components/CategoryTab'
import MenuCard from '../components/MenuCard'
import MenuDetail from '../components/MenuDetail'
import type { Category, MenuItem } from '../types'

interface CategoryWithItems {
  category: Category
  items: MenuItem[]
}

export default function MenuPage() {
  const [menuData, setMenuData] = useState<CategoryWithItems[]>([])
  const [selectedCategoryId, setSelectedCategoryId] = useState<number | null>(null)
  const [selectedItem, setSelectedItem] = useState<MenuItem | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadMenu()
  }, [])

  async function loadMenu() {
    try {
      setLoading(true)
      setError(null)
      const data = await fetchMenu()
      setMenuData(data)
      if (data.length > 0) {
        setSelectedCategoryId(data[0].category.id)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : '메뉴를 불러오는데 실패했습니다')
    } finally {
      setLoading(false)
    }
  }

  const categories = menuData.map((d) => d.category)
  const currentItems =
    menuData.find((d) => d.category.id === selectedCategoryId)?.items ?? []

  if (loading) {
    return (
      <div style={styles.center} data-testid="menu-loading">
        <p>메뉴를 불러오는 중...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div style={styles.center} data-testid="menu-error">
        <p>{error}</p>
        <button onClick={loadMenu} data-testid="menu-retry-button">
          다시 시도
        </button>
      </div>
    )
  }

  if (menuData.length === 0) {
    return (
      <div style={styles.center} data-testid="menu-empty">
        <p>등록된 메뉴가 없습니다</p>
      </div>
    )
  }

  return (
    <div style={styles.container} data-testid="menu-page">
      <CategoryTab
        categories={categories}
        selectedId={selectedCategoryId}
        onSelect={setSelectedCategoryId}
      />
      <div style={styles.grid} data-testid="menu-grid">
        {currentItems.map((item) => (
          <MenuCard
            key={item.id}
            menuItem={item}
            onClick={() => setSelectedItem(item)}
          />
        ))}
      </div>
      {selectedItem && (
        <MenuDetail
          menuItem={selectedItem}
          isOpen={true}
          onClose={() => setSelectedItem(null)}
        />
      )}
    </div>
  )
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    height: '100vh',
    backgroundColor: '#f5f5f5',
  },
  center: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    gap: '12px',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
    gap: '16px',
    padding: '16px',
    flex: 1,
    overflowY: 'auto',
  },
}
