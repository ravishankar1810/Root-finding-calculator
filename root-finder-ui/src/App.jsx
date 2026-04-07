import { BrowserRouter as Router, Routes, Route, NavLink, Navigate } from 'react-router-dom';
import BisectionPage from './pages/BisectionPage';
import NewtonPage from './pages/NewtonPage';
import SecantPage from './pages/SecantPage';
import RegulaFalsiPage from './pages/RegulaFalsiPage';
import ComparePage from './pages/ComparePage';

export default function App() {
  return (
    <Router>
      <div className="app-container" style={{ backgroundColor: '#0D1117', minHeight: '100vh', color: '#E6EDF3' }}>
        {/* Navigation Bar */}
        <nav style={{ padding: '20px', backgroundColor: '#161B22', display: 'flex', gap: '15px' }}>
          <NavLink to="/bisection" style={{ color: '#58A6FF', textDecoration: 'none' }}>Bisection</NavLink>
          <NavLink to="/newton" style={{ color: '#58A6FF', textDecoration: 'none' }}>Newton-Raphson</NavLink>
          <NavLink to="/secant" style={{ color: '#58A6FF', textDecoration: 'none' }}>Secant</NavLink>
          <NavLink to="/regula-falsi" style={{ color: '#58A6FF', textDecoration: 'none' }}>Regula Falsi</NavLink>
          <NavLink to="/compare" style={{ color: '#D2A8FF', textDecoration: 'none' }}>Compare All</NavLink>
        </nav>

        {/* Page Content */}
        <div style={{ padding: '20px' }}>
          <Routes>
            {/* Redirect the blank home page to Bisection automatically */}
            <Route path="/" element={<Navigate to="/bisection" replace />} />
            
            <Route path="/bisection" element={<BisectionPage />} />
            <Route path="/newton" element={<NewtonPage />} />
            <Route path="/secant" element={<SecantPage />} />
            <Route path="/regula-falsi" element={<RegulaFalsiPage />} />
            <Route path="/compare" element={<ComparePage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}