// src/components/Inventory/InventoryCreate.js
import React, { useState } from 'react';
import { createInventory } from '../../services/inventoryService';
import { useNavigate } from 'react-router-dom';
import '../../styles/InventoryForm.css';

const InventoryCreate = () => {
  const navigate = useNavigate();
  const [inventoryData, setInventoryData] = useState({
    name: '',
    quantity: 0,
    warehouse_id: 1,
    goods_id: 1,
  });
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setInventoryData({ ...inventoryData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await createInventory(inventoryData);
      setMessage('Inventory created successfully!');
      setInventoryData({
        name: '',
        quantity: 0,
        warehouse_id: 1,
        goods_id: 1,
      });
      navigate('/inventory')
    } catch (error) {
      setMessage('Failed to create inventory.');
      console.error('Error creating inventory:', error);
    }
  };

  return (
    <div className="inventory-form">
      <h2>Создать инвентарь</h2>
      {message && <p>{message}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Название:</label>
          <input type="text" id="name" name="name" value={inventoryData.name} onChange={handleChange} required />
        </div>
        <div>
          <label htmlFor="quantity">Количество:</label>
          <input type="number" id="quantity" name="quantity" value={inventoryData.quantity} onChange={handleChange} required />
        </div>
        <div>
          <label htmlFor="warehouse_id">Идентификатор склада:</label>
          <input type="number" id="warehouse_id" name="warehouse_id" value={inventoryData.warehouse_id} onChange={handleChange} required />
        </div>
        <div>
          <label htmlFor="goods_id">Идентификатор товара:</label>
          <input type="number" id="goods_id" name="goods_id" value={inventoryData.goods_id} onChange={handleChange} required />
        </div>
        <button type="submit">Создать</button>
      </form>
    </div>
  );
};

export default InventoryCreate;