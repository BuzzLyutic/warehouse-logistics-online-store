// src/components/Home.js
import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Home.css';

const Home = () => {
  return (
    <div className="home-container">
      <header className="home-header">
        <h1>Управление складом и логистикой</h1>
        <p>Оптимизация работы Вашего Интернет-Магазина</p>
        <Link to="/logout" className="logout">Выйти</Link>
      </header>

      <section className="navigation-section">
        <Link to="/inventory" className="nav-link">
          <div className="nav-icon">
            <i className="fas fa-boxes"></i> {/* Example icon - see Font Awesome */}
          </div>
          <h2>Инвентарь</h2>
          <p>Управление складами и товарами</p>
        </Link>

        <Link to="/orders" className="nav-link">
          <div className="nav-icon">
            <i className="fas fa-clipboard-list"></i> {/* Example icon */}
          </div>
          <h2>Заказы</h2>
          <p>Просмотр и обработка заказов</p>
        </Link>

        <Link to="/shipment" className="nav-link">
          <div className="nav-icon">
            <i className="fas fa-clipboard-list"></i> {/* Example icon */}
          </div>
          <h2>Транспортировки</h2>
          <p>Отслеживание перевозки грузов</p>
        </Link>

        {/* Add more links as your application grows */}
      </section>

      <footer className="home-footer">
        <p>&copy; {new Date().getFullYear()} ... РТУ МИРЭА</p>
      </footer>
    </div>
  );
};

export default Home;