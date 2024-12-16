// src/utils/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: '/api', // Nginx will proxy this to the Django backend
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const registerUser = (userData) => api.post('/auth/register/', userData);
export const loginUser = (userData) => api.post('/auth/login/', userData);
export const logoutUser = () => api.post('/auth/logout/', { refresh: localStorage.getItem('refreshToken') });
export const getCurrentUser = () => api.get('/auth/user/me/');

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      console.error('API Error:', error.response.data);
      if (error.response.status === 401 || error.response.status === 403) {
      }
    } else {
      console.error('Network or Request Error:', error.message);
    }
    return Promise.reject(error);
  }
);

export default api;