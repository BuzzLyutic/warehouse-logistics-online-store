import React, { useState } from 'react';
import { createShipment } from '../../services/shipmentService';

const ShipmentCreate = () => {
  const [shipmentData, setShipmentData] = useState({
    order_id: '',
    carrier: '',
    tracking_number: ''
  });
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setShipmentData({ ...shipmentData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await createShipment(shipmentData);
      setMessage('Shipment created successfully!');
      setShipmentData({
        order_id: '',
        carrier: '',
        tracking_number: ''
      }); // Reset form
    } catch (error) {
      setMessage('Failed to create shipment.');
      console.error('Error creating shipment:', error);
    }
  };

  return (
    <div>
      <h2>Create Shipment</h2>
      {message && <p>{message}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="order_id">Order ID:</label>
          <input type="text" id="order_id" name="order_id" value={shipmentData.order_id} onChange={handleChange} required />
        </div>
        <div>
          <label htmlFor="carrier">Carrier:</label>
          <input type="text" id="carrier" name="carrier" value={shipmentData.carrier} onChange={handleChange} required />
        </div>
        <div>
          <label htmlFor="tracking_number">Tracking Number:</label>
          <input type="text" id="tracking_number" name="tracking_number" value={shipmentData.tracking_number} onChange={handleChange} required />
        </div>
        <button type="submit">Create Shipment</button>
      </form>
    </div>
  );
};

export default ShipmentCreate;