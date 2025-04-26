import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { useAuth } from './contexts/AuthContext';

// Components
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Register from './pages/Register';
import JobSeekerDashboard from './pages/JobSeekerDashboard';
import RecruiterDashboard from './pages/RecruiterDashboard';
import JobSearch from './pages/JobSearch';
import CandidateSearch from './pages/CandidateSearch';
import Profile from './pages/Profile';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

const PrivateRoute = ({ children, allowedRoles }) => {
  const { user, isAuthenticated } = useAuth();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }
  
  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to="/" />;
  }
  
  return children;
};

const App = () => {
  const { user, isAuthenticated } = useAuth();

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Navbar />
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={
            isAuthenticated ? <Navigate to="/" /> : <Login />
          } />
          <Route path="/register" element={
            isAuthenticated ? <Navigate to="/" /> : <Register />
          } />

          {/* Private Routes */}
          <Route path="/" element={
            <PrivateRoute>
              {user?.role === 'recruiter' ? <RecruiterDashboard /> : <JobSeekerDashboard />}
            </PrivateRoute>
          } />

          {/* Job Seeker Routes */}
          <Route path="/job-search" element={
            <PrivateRoute allowedRoles={['job_seeker']}>
              <JobSearch />
            </PrivateRoute>
          } />

          {/* Recruiter Routes */}
          <Route path="/candidate-search" element={
            <PrivateRoute allowedRoles={['recruiter']}>
              <CandidateSearch />
            </PrivateRoute>
          } />

          {/* Common Routes */}
          <Route path="/profile" element={
            <PrivateRoute>
              <Profile />
            </PrivateRoute>
          } />
        </Routes>
      </Router>
    </ThemeProvider>
  );
};

export default App; 