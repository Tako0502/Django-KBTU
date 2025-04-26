import React, { useEffect, useState } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { CircularProgress, Box } from '@mui/material';
import api from '../services/api';

const PublicRoute = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(null);
  const location = useLocation();

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        setIsAuthenticated(false);
        return;
      }

      try {
        await api.auth.getCurrentUser();
        setIsAuthenticated(true);
      } catch (error) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        setIsAuthenticated(false);
      }
    };

    checkAuth();
  }, []);

  if (isAuthenticated === null) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
      </Box>
    );
  }

  if (isAuthenticated) {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    if (user.role === 'job_seeker') {
      return <Navigate to="/job-search" replace />;
    } else if (user.role === 'recruiter') {
      return <Navigate to="/recruiter-dashboard" replace />;
    }
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

export default PublicRoute; 