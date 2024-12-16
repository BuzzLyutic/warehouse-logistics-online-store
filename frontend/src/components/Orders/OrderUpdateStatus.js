import React, { useState } from 'react';
import { updateOrderStatus } from '../../services/orderService';

const OrderUpdateStatus = ({ orderId }) => {
  const [newStatus, setNewStatus] = useState('');
  const [message, setMessage] = useState('');

  const handleStatusChange = (e) => {
    setNewStatus(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await updateOrderStatus(orderId, newStatus);
      setMessage('Order status updated successfully!');
      setNewStatus(''); // Reset form
    } catch (error) {
      setMessage('Failed to update order status.');
      console.error(`Error updating status for order ${orderId}:`, error);
    }
  };

  return (
    <div>
      <h3>Update Order Status</h3>
      {message && <p>{message}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="newStatus">New Status:</label>
          <select id="newStatus" name="newStatus" value={newStatus} onChange={handleStatusChange} required>
            <option value="">Select Status</option>
            <option value="Pending">Pending</option>
            <option value="Processing">Processing</option>
            <option value="Shipped">Shipped</option>
            <option value="Delivered">Delivered</option>
            <option value="Cancelled">Cancelled</option>
          </select>
        </div>
        <button type="submit">Update Status</button>
      </form>
    </div>
  );
};

export default OrderUpdateStatus;