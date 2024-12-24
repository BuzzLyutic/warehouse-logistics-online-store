import React, { useState, useEffect } from 'react';
import { getOrders } from '../../services/orderService';
import '../../styles/Orders.css'; // Import the CSS file
import { Link } from 'react-router-dom';


const OrderList = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchOrders = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await getOrders();
        setOrders(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, []);

  if (loading) {
    return <div>Loading orders...</div>;
  }

  if (error) {
    return <div>Error loading orders: {error}</div>;
  }

  return (
    <div className="order-list-container">
      <h1>Orders</h1>
      {orders.length === 0 ? (
        <p>No orders available.</p>
      ) : (
        <table className="order-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Customer Name</th>
              <th>Customer Email</th>
              <th>Total Price</th>
              <th>Status</th>
              <th>Created At</th>
            </tr>
          </thead>
          <tbody>
            {orders.map(order => (
              <tr key={order.id}>
                <td>{order.id}</td>
                <td>{order.customer_name}</td>
                <td>{order.customer_email}</td>
                <td>${order.total_price}</td>
                <td>{order.status}</td>
                <td>{new Date(order.created_at).toLocaleString()}</td>
                <td>
                <Link to={`/orders/${order.id}`} className="update-button">Подробнее</Link> {/* Update button with query param */}
              </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default OrderList;