import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import theme from './theme';

// Components
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import PublicRoute from './components/PublicRoute';

// Pages
import Login from './pages/Login';
import Register from './pages/Register';
import JobSearch from './pages/JobSearch';
import RecruiterDashboard from './pages/RecruiterDashboard';
import Dashboard from './pages/Dashboard';
import Unauthorized from './pages/Unauthorized';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Navbar />
        <Routes>
          {/* Public Routes */}
          <Route
            path="/login"
            element={
              <PublicRoute>
                <Login />
              </PublicRoute>
            }
          />
          <Route
            path="/register"
            element={
              <PublicRoute>
                <Register />
              </PublicRoute>
            }
          />

          {/* Protected Routes */}
          <Route
            path="/job-search"
            element={
              <ProtectedRoute allowedRoles={['job_seeker']}>
                <JobSearch />
              </ProtectedRoute>
            }
          />
          <Route
            path="/recruiter-dashboard"
            element={
              <ProtectedRoute allowedRoles={['recruiter']}>
                <RecruiterDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />

          {/* Other Routes */}
          <Route path="/unauthorized" element={<Unauthorized />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App; 