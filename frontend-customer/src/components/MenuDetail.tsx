import type { MenuItem } from '../types'

interface MenuDetailProps {
  menuItem: MenuItem
  isOpen: boolean
  onClose: () => void
}

const PLACEHOLDER_IMAGE = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjE1MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMjAwIiBoZWlnaHQ9IjE1MCIgZmlsbD0iI2VlZSIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBkb21pbmFudC1iYXNlbGluZT0ibWlkZGxlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjOTk5IiBmb250LXNpemU9IjE0Ij7snbTrr7jsp4Ag7JeG7J2MPC90ZXh0Pjwvc3ZnPg=='

function formatPrice(price: number): string {
  return price.toLocaleString('ko-KR') + '원'
}

export default function MenuDetail({ menuItem, isOpen, onClose }: MenuDetailProps) {
  if (!isOpen) return null

  return (
    <div
      style={styles.overlay}
      onClick={onClose}
      data-testid="menu-detail-overlay"
      role="dialog"
      aria-modal="true"
      aria-label={`${menuItem.name} 상세 정보`}
    >
      <div
        style={styles.modal}
        onClick={(e) => e.stopPropagation()}
        data-testid="menu-detail-modal"
      >
        <button
          style={styles.closeButton}
          onClick={onClose}
          data-testid="menu-detail-close"
          aria-label="닫기"
        >
          ✕
        </button>
        <img
          src={menuItem.image_url || PLACEHOLDER_IMAGE}
          alt={menuItem.name}
          style={styles.image}
          onError={(e) => {
            (e.target as HTMLImageElement).src = PLACEHOLDER_IMAGE
          }}
        />
        <div style={styles.content}>
          <h2 style={styles.name}>{menuItem.name}</h2>
          <p style={styles.price}>{formatPrice(menuItem.price)}</p>
          {menuItem.description && (
            <p style={styles.description}>{menuItem.description}</p>
          )}
        </div>
      </div>
    </div>
  )
}

const styles: Record<string, React.CSSProperties> = {
  overlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0,0,0,0.5)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 1000,
  },
  modal: {
    backgroundColor: '#fff',
    borderRadius: '16px',
    overflow: 'hidden',
    maxWidth: '400px',
    width: '90%',
    maxHeight: '80vh',
    position: 'relative',
  },
  closeButton: {
    position: 'absolute',
    top: '12px',
    right: '12px',
    background: 'rgba(0,0,0,0.5)',
    color: '#fff',
    border: 'none',
    borderRadius: '50%',
    width: '32px',
    height: '32px',
    cursor: 'pointer',
    fontSize: '16px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 1,
  },
  image: {
    width: '100%',
    height: '250px',
    objectFit: 'cover',
  },
  content: {
    padding: '20px',
  },
  name: {
    margin: 0,
    fontSize: '20px',
    fontWeight: 700,
  },
  price: {
    margin: '8px 0',
    fontSize: '18px',
    color: '#1976d2',
    fontWeight: 700,
  },
  description: {
    margin: '12px 0 0',
    fontSize: '14px',
    color: '#666',
    lineHeight: 1.6,
  },
}
