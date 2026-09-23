import './App.css'

import {
  Navigate,
  Route,
  Routes,
} from 'react-router-dom'

import Navbar from './components/Navbar'
import Hero from './components/Hero'
import Features from './components/Features'
import WhyStockPilot from './components/WhyStockPilot'
import HowItWorks from './components/HowItWorks'
import Pricing from './components/Pricing'
import FAQ from './components/FAQ'
import ContactCTA from './components/ContactCTA'
import Footer from './components/Footer'

import AppLayout from './components/layout/AppLayout'
import Login from './pages/auth/Login'
import Dashboard from './pages/dashboard/Dashboard'
import Inventory from './pages/inventory/Inventory'
import Products from './pages/products/Products'
import Sales from './pages/sales/Sales'
import Purchases from './pages/purchases/Purchases'
import Suppliers from './pages/suppliers/Suppliers'
import Deliveries from './pages/deliveries/Deliveries'
import Reports from './pages/reports/Reports'
import Settings from './pages/settings/Settings'

function LandingPage() {
  return (
    <div className="site-shell">
      <Navbar />

      <main>
        <Hero />
        <Features />
        <WhyStockPilot />
        <HowItWorks />
        <Pricing />
        <FAQ />
        <ContactCTA />
      </main>

      <Footer />
    </div>
  )
}

function App() {
  return (
    <Routes>
      <Route
        path="/"
        element={<LandingPage />}
      />

      <Route
        path="/login"
        element={<Login />}
      />

      <Route element={<AppLayout />}>
        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        <Route
          path="/inventory"
          element={<Inventory />}
        />

        <Route
          path="/products"
          element={<Products />}
        />

        <Route
          path="/sales"
          element={<Sales />}
        />

        <Route
          path="/purchases"
          element={<Purchases />}
        />

        <Route
          path="/suppliers"
          element={<Suppliers />}
        />

        <Route
          path="/deliveries"
          element={<Deliveries />}
        />

        <Route
          path="/reports"
          element={<Reports />}
        />

        <Route
          path="/settings"
          element={<Settings />}
        />
      </Route>

      <Route
        path="*"
        element={
          <Navigate
            to="/"
            replace
          />
        }
      />
    </Routes>
  )
}

export default App
