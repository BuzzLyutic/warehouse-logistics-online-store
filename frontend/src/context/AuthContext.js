// src/context/AuthContext.js

import React, { createContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../utils/api';
import { jwtDecode } from 'jwt-decode';
export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true); // Initial auth check
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuth = async () => {
      setIsLoading(true);
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const decoded = jwtDecode(token);
          // Simple expiry check (you might want a more robust solution)
          if (decoded.exp * 1000 < Date.now()) {
            throw new Error('Token expired');
          }
          api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
          const { data } = await api.get('/auth/user/me/');
          setUser({ ...data, role: decoded.role, permissions: decoded.permissions });
        } catch (error) {
          console.error('Authentication failed', error);
          localStorage.clear();
          setUser(null);
        }
      }
      setIsLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (credentials) => {
    try {
      const { data } = await api.post('/auth/login/', credentials);
      localStorage.setItem('token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      const decoded = jwtDecode(data.access);
      api.defaults.headers.common['Authorization'] = `Bearer ${data.access}`;
      setUser({ ...data.user, role: decoded.role, permissions: decoded.permissions });
      navigate('/home');
    } catch (error) {
      throw error;
    }
  };

  const logout = async () => {
    try {
      await api.post('/auth/logout/', {
        refresh: localStorage.getItem('refresh_token'),
      });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.clear();
      setUser(null);
      api.defaults.headers.common['Authorization'] = null;
      navigate('/login');
    }
  };

  if (isLoading) {
    return <div>Loading...</div>; // Or a more elaborate loading spinner
  }

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
