import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from '../Navbar/Navbar';

function AuthenticatedLayout() {
  return (
    <div>
      <Navbar />
      <Outlet /> {/* This renders nested routes */}
    </div>
  );
}

export default AuthenticatedLayout;
