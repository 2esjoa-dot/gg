import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Suspense, lazy } from 'react'
import AuthGuard from './components/AuthGuard'
import Loading from './components/Loading'

const MenuPage = lazy(() => import('./pages/MenuPage'))
const CartPage = lazy(() => import('./pages/CartPage'))
const OrderConfirmPage = lazy(() => import('./pages/OrderConfirmPage'))
const OrderHistoryPage = lazy(() => import('./pages/OrderHistoryPage'))
const SetupPage = lazy(() => import('./pages/SetupPage'))

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<Loading size="lg" />}>
        <Routes>
          <Route path="/setup" element={<SetupPage />} />
          <Route
            path="/"
            element={
              <AuthGuard>
                <MenuPage />
              </AuthGuard>
            }
          />
          <Route
            path="/cart"
            element={
              <AuthGuard>
                <CartPage />
              </AuthGuard>
            }
          />
          <Route
            path="/order/confirm"
            element={
              <AuthGuard>
                <OrderConfirmPage />
              </AuthGuard>
            }
          />
          <Route
            path="/orders"
            element={
              <AuthGuard>
                <OrderHistoryPage />
              </AuthGuard>
            }
          />
        </Routes>
      </Suspense>
    </BrowserRouter>
  )
}

export default App
