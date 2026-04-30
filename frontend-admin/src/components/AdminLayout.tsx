import { ReactNode } from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAdminAuthStore } from '../store/authStore'

const navItems = [
  { path: '/', labelKey: 'nav.dashboard', roles: ['store_admin', 'hq_admin'] },
  { path: '/tables', labelKey: 'nav.tables', roles: ['store_admin'] },
  { path: '/menu', labelKey: 'nav.menu', roles: ['store_admin'] },
  { path: '/accounts', labelKey: 'nav.accounts', roles: ['store_admin'] },
  { path: '/stores', labelKey: 'nav.stores', roles: ['hq_admin'] },
]

export default function AdminLayout({ children }: { children: ReactNode }) {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const { role, username, logout } = useAdminAuthStore()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const visibleItems = navItems.filter((item) => role && item.roles.includes(role))

  return (
    <div className="flex h-screen bg-gray-50">
      <aside className="w-60 bg-white border-r border-gray-200 flex flex-col">
        <div className="px-6 py-5 border-b border-gray-100">
          <h1 className="text-lg font-bold text-primary-600">Table Order</h1>
          <p className="text-xs text-gray-400 mt-1">{username}</p>
        </div>
        <nav className="flex-1 px-3 py-4 space-y-1">
          {visibleItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === '/'}
              className={({ isActive }) =>
                `block px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-primary-50 text-primary-700'
                    : 'text-gray-600 hover:bg-gray-100'
                }`
              }
              data-testid={`nav-${item.path.replace('/', '') || 'dashboard'}`}
            >
              {t(item.labelKey)}
            </NavLink>
          ))}
        </nav>
        <div className="px-3 py-4 border-t border-gray-100">
          <button
            onClick={handleLogout}
            className="w-full px-3 py-2.5 text-sm text-gray-600 hover:bg-gray-100 rounded-lg text-left"
            data-testid="logout-button"
          >
            {t('auth.logout')}
          </button>
        </div>
      </aside>
      <main className="flex-1 overflow-y-auto p-6">{children}</main>
    </div>
  )
}
