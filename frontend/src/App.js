// App.js
import React from 'react';
import {
  createBrowserRouter,
  RouterProvider,
  createRoutesFromElements,
  Route,
  Navigate,
  Outlet, // Import Outlet to render child routes
} from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import InventoryList from './components/Inventory/InventoryList';
import InventoryCreate from './components/Inventory/InventoryCreate';
import InventoryUpdate from './components/Inventory/InventoryUpdate';
import Home from './components/Home';
import OrderList from './components/Orders/OrderList';
import OrderDetails from './components/Orders/OrderDetails';
import ShipmentList from './components/Shipments/ShipmentList';

import './styles/App.css';

const AppLayout = () => {
  return (
    <AuthProvider>
      <Outlet /> {/* This renders the child routes */}
    </AuthProvider>
  );
};

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route element={<AppLayout />}>
      <Route path="/" element={<Navigate replace to="/login" />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route
        path="/home"
        element={
          <ProtectedRoute>
            <Home />
          </ProtectedRoute>
        }
      />
      <Route path="/inventory"
        element={
            <ProtectedRoute>
                <Outlet />
            </ProtectedRoute>
        }>
          <Route index element={<InventoryList />} />
          <Route path="create" element={<InventoryCreate />} />
          <Route path="update" element={<InventoryUpdate />} />
        </Route>
      <Route path="/orders" element={<ProtectedRoute><Outlet /></ProtectedRoute>}>
      <Route index element={<OrderList />} />
      <Route path=":id" element={<OrderDetails />} />
    </Route>
    <Route path="/shipment" element={<ProtectedRoute><ShipmentList /></ProtectedRoute>} />
  </Route>
  )
);

const App = () => {
  return <RouterProvider router={router} />;
};

export default App;

