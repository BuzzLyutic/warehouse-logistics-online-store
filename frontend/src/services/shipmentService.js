// src/services/shipmentService.js
import api from '../utils/api';

export const createShipment = async (shipmentData) => {
  try {
    const response = await api.post('/shipments/shipments/', shipmentData);
    return response.data;
  } catch (error) {
    console.error('Error creating shipment:', error);
    throw error;
  }
};

export const getShipmentTracking = async (shipmentId) => {
  try {
    const response = await api.get(`/shipments/shipments/${shipmentId}/tracking/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching tracking for shipment ID ${shipmentId}:`, error);
    throw error;
  }
};