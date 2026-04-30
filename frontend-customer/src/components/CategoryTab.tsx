import type { Category } from '../types'

interface CategoryTabProps {
  categories: Category[]
  selectedId: number | null
  onSelect: (id: number) => void
}

export default function CategoryTab({ categories, selectedId, onSelect }: CategoryTabProps) {
  return (
    <div style={styles.container} data-testid="category-tab">
      {categories.map((cat) => (
        <button
          key={cat.id}
          onClick={() => onSelect(cat.id)}
          style={{
            ...styles.tab,
            ...(cat.id === selectedId ? styles.activeTab : {}),
          }}
          data-testid={`category-tab-${cat.id}`}
          aria-pressed={cat.id === selectedId}
        >
          {cat.name}
        </button>
      ))}
    </div>
  )
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    display: 'flex',
    overflowX: 'auto',
    gap: '8px',
    padding: '12px 16px',
    backgroundColor: '#fff',
    borderBottom: '1px solid #e0e0e0',
  },
  tab: {
    padding: '8px 20px',
    border: '1px solid #ddd',
    borderRadius: '20px',
    backgroundColor: '#fff',
    cursor: 'pointer',
    whiteSpace: 'nowrap',
    fontSize: '14px',
    fontWeight: 500,
  },
  activeTab: {
    backgroundColor: '#1976d2',
    color: '#fff',
    borderColor: '#1976d2',
  },
}
