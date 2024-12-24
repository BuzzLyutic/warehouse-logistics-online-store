import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getOrderById, updateOrderStatus } from '../../services/orderService';
import '../../styles/Orders.css';

const OrderDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [order, setOrder] = useState(null);
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchOrder = async () => {
      try {
        const data = await getOrderById(id);
        setOrder(data);
        setStatus(data.status);
      } catch (err) {
        setError('Failed to fetch order details.');
      } finally {
        setLoading(false);
      }
    };
    fetchOrder();
  }, [id]);

  const handleStatusUpdate = async () => {
    try {
      await updateOrderStatus(id, status);
      alert('Order status updated successfully!');
      navigate('/orders');
    } catch (err) {
      alert('Failed to update order status.');
    }
  };

  if (loading) return <div>Loading order details...</div>;
  if (error) return <div>{error}</div>;
  if (!order) return <div>Order not found.</div>;

  return (
    <div className="order-details-container">
      <h1>Order Details</h1>
      <ul>
        <li><strong>ID:</strong> {order.id}</li>
        <li><strong>Customer:</strong> {order.customer_name}</li>
        <li><strong>Email:</strong> {order.customer_email}</li>
        <li><strong>Total Price:</strong> ${order.total_price}</li>
        <li><strong>Status:</strong>
          <select value={status} onChange={(e) => setStatus(e.target.value)} className="status-select">
            <option value="pending">Pending</option>
            <option value="processing">Processing</option>
            <option value="shipping">Shipping</option>
            <option value="fulfilled">Fulfilled</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </li>
      </ul>
      <button onClick={handleStatusUpdate} className="update-button">Update Status</button>
      <button onClick={() => navigate('/orders')} className="back-button">Back to Orders</button>
    </div>
  );
};

export default OrderDetails;