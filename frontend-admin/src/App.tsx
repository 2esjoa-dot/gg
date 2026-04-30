import { BrowserRouter, Routes, Route } from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import TableManagePage from './pages/TableManagePage'
import MenuManagePage from './pages/MenuManagePage'
import AccountPage from './pages/AccountPage'
import HQStorePage from './pages/HQStorePage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/" element={<DashboardPage />} />
        <Route path="/tables" element={<TableManagePage />} />
        <Route path="/menu" element={<MenuManagePage />} />
        <Route path="/accounts" element={<AccountPage />} />
        <Route path="/stores" element={<HQStorePage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
