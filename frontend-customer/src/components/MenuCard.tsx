import type { MenuItem } from '../types'

interface MenuCardProps {
  menuItem: MenuItem
  onClick: () => void
}

const PLACEHOLDER_IMAGE = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjE1MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMjAwIiBoZWlnaHQ9IjE1MCIgZmlsbD0iI2VlZSIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBkb21pbmFudC1iYXNlbGluZT0ibWlkZGxlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjOTk5IiBmb250LXNpemU9IjE0Ij7snbTrr7jsp4Ag7JeG7J2MPC90ZXh0Pjwvc3ZnPg=='

function formatPrice(price: number): string {
  return price.toLocaleString('ko-KR') + '원'
}

export default function MenuCard({ menuItem, onClick }: MenuCardProps) {
  return (
    <div
      style={styles.card}
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => { if (e.key === 'Enter') onClick() }}
      data-testid={`menu-card-${menuItem.id}`}
    >
      <img
        src={menuItem.image_url || PLACEHOLDER_IMAGE}
        alt={menuItem.name}
        style={styles.image}
        onError={(e) => {
          (e.target as HTMLImageElement).src = PLACEHOLDER_IMAGE
        }}
      />
      <div style={styles.info}>
        <h3 style={styles.name}>{menuItem.name}</h3>
        <p style={styles.price}>{formatPrice(menuItem.price)}</p>
      </div>
    </div>
  )
}

const styles: Record<string, React.CSSProperties> = {
  card: {
    backgroundColor: '#fff',
    borderRadius: '12px',
    overflow: 'hidden',
    boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
    cursor: 'pointer',
    transition: 'transform 0.2s',
  },
  image: {
    width: '100%',
    height: '150px',
    objectFit: 'cover',
  },
  info: {
    padding: '12px',
  },
  name: {
    margin: 0,
    fontSize: '16px',
    fontWeight: 600,
  },
  price: {
    margin: '4px 0 0',
    fontSize: '15px',
    color: '#1976d2',
    fontWeight: 700,
  },
}
