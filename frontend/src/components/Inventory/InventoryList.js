// src/components/Inventory/InventoryList.js
import React, { useState, useEffect } from 'react';
import { getInventoryList } from '../../services/inventoryService';
import { Link } from 'react-router-dom';
import '../../styles/InventoryList.css';


const InventoryList = () => {
  const [inventory, setInventory] = useState([]);

  useEffect(() => {
    const fetchInventory = async () => {
      try {
        const data = await getInventoryList();
        setInventory(data);
      } catch (error) {
        console.error('Failed to fetch inventory:', error);
      }
    };

    fetchInventory();
  }, []);

  return (
    <div className="inventory-list">
      <h2>Список инвентарей</h2>
      <Link to="/inventory/create" className="add-inventory-button">Добавить инвентарь</Link>
      <table>
        <thead>
          <tr>
            <th>Идентификатор</th>
            <th>Название</th>
            <th>Количество</th>
            <th>Склад</th>
            <th>Товары</th>
            <th>Действия</th> {/* New column for actions */}
          </tr>
        </thead>
        <tbody>
          {inventory.map((item) => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.goods.name}</td>
              <td>{item.quantity}</td>
              <td>{item.warehouse.name}</td>
              <td>{item.goods.name}</td>
              <td>
                <Link to={`/inventory/update?id=${item.id}`} className="update-button">Обновить</Link> {/* Update button with query param */}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default InventoryList;