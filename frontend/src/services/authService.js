import api from '../utils/api';

export const login = async (credentials) => {
  try {
    const response = await api.post('/auth/login/', credentials);
    localStorage.setItem('token', response.data.access);
    return response.data;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
};

export const register = async (userData) => {
  try {
    const response = await api.post('/auth/register/', userData);
    return response.data;
  } catch (error) {
    console.error('Registration error:', error);
    throw error;
  }
};

export const logout = async () => {
  try {
    await api.post('/auth/logout/', {
      refresh: localStorage.getItem('refresh_token'),
    });
    localStorage.clear();
  } catch (error) {
    console.error('Logout error:', error);
  }};