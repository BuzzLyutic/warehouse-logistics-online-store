// src/services/orderService.js
import api from '../utils/api';

export const getOrders = async () => {
  try {
    const response = await api.get('/orders/orders/');
    return response.data;
  } catch (error) {
    console.error('Error fetching orders:', error);
    throw error;
  }
};

export const getOrderById = async (orderId) => {
  try {
    const response = await api.get(`/orders/orders/${orderId}/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching order with ID ${orderId}:`, error);
    throw error;
  }
};

export const updateOrderStatus = async (orderId, newStatus) => {
    try {
      const response = await api.patch(`/orders/orders/${orderId}/update_status/`, { status: newStatus });
      return response.data;
    } catch (error) {
      console.error(`Error updating status for order with ID ${orderId}:`, error);
      throw error;
    }
  };