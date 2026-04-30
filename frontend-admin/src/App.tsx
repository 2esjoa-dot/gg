import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Suspense, lazy } from 'react'
import AdminAuthGuard, { RoleGuard } from './components/AdminAuthGuard'
import AdminLayout from './components/AdminLayout'

const LoginPage = lazy(() => import('./pages/LoginPage'))
const DashboardPage = lazy(() => import('./pages/DashboardPage'))
const TableManagePage = lazy(() => import('./pages/TableManagePage'))
const MenuManagePage = lazy(() => import('./pages/MenuManagePage'))
const AccountPage = lazy(() => import('./pages/AccountPage'))
const HQStorePage = lazy(() => import('./pages/HQStorePage'))

function Loading() {
  return (
    <div className="flex items-center justify-center h-screen">
      <div className="animate-spin h-8 w-8 border-4 border-primary-600 border-t-transparent rounded-full" />
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<Loading />}>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/"
            element={
              <AdminAuthGuard>
                <AdminLayout>
                  <DashboardPage />
                </AdminLayout>
              </AdminAuthGuard>
            }
          />
          <Route
            path="/tables"
            element={
              <AdminAuthGuard>
                <AdminLayout>
                  <TableManagePage />
                </AdminLayout>
              </AdminAuthGuard>
            }
          />
          <Route
            path="/menu"
            element={
              <AdminAuthGuard>
                <AdminLayout>
                  <MenuManagePage />
                </AdminLayout>
              </AdminAuthGuard>
            }
          />
          <Route
            path="/accounts"
            element={
              <AdminAuthGuard>
                <AdminLayout>
                  <AccountPage />
                </AdminLayout>
              </AdminAuthGuard>
            }
          />
          <Route
            path="/stores"
            element={
              <AdminAuthGuard>
                <AdminLayout>
                  <RoleGuard role="hq_admin">
                    <HQStorePage />
                  </RoleGuard>
                </AdminLayout>
              </AdminAuthGuard>
            }
          />
        </Routes>
      </Suspense>
    </BrowserRouter>
  )
}

export default App
