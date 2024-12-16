// src/components/Auth/Register.js

import React, { useState, useEffect } from 'react';
import { register } from '../../services/authService';
import { useNavigate } from 'react-router-dom';
import api from '../../utils/api';
import '../../styles/Register.css';

const Register = () => {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('');
  const [roles, setRoles] = useState([]);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);
    try {
      const registrationResult = await register({
        first_name: firstName,
        last_name: lastName,
        email,
        password,
        role,
      });

      if (registrationResult) {
        setSuccess(true);
        setFirstName('');
        setLastName('');
        setEmail('');
        setPassword('');
        setRole('');
        setTimeout(() => {
          navigate('/login');
        }, 8000)
      }
    } catch (err) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError('Registration failed. Please check your connection or try again later.');
      }
    }
  };

  if (success) {
    return <div>Registration successful! You can now log in (Redirecting in 5 seconds...).</div>;
  }

  return (
    <div className="register-container">
      <h2>Регистрация</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="firstName">Имя:</label>
          <input
            type="text"
            id="firstName"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="lastName">Фамилия:</label>
          <input
            type="text"
            id="lastName"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="email">Эл.почта:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="password">Пароль:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="role">Должность:</label>
          <select id="role" value={role} onChange={(e) => setRole(e.target.value)} required>
            <option value="">Выберете должность</option>
            <option value="admin">Администратор</option>
            <option value="staff">Сотрудник</option>
            <option value="order_manager">Менеджер по заказам</option>
          </select>
        </div>
        <button type="submit">Зарегистрироваться</button>
      </form>
    </div>
  );
};

export default Register;