// src/services/inventoryService.js
import api from '../utils/api';

export const getInventoryList = async () => {
  try {
    const response = await api.get('/inventory/inventory/');
    return response.data;
  } catch (error) {
    console.error('Error fetching inventory:', error);
    throw error;
  }
};

export const createInventory = async (inventoryData) => {
    try {
        const response = await api.post('/inventory/inventory/create/', inventoryData);
        return response.data;
    } catch (error) {
        console.error('Error creating inventory:', error);
        throw error;
    }
};

export const updateInventory = async (inventoryData) => {
    try {
        const response = await api.post('/inventory/inventory/update/', inventoryData);
        return response.data;
    } catch (error) {
        console.error('Error updating inventory:', error);
        throw error;
    }
};