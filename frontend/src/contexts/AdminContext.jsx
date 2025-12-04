import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AdminContext = createContext();

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

export const AdminProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [admin, setAdmin] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if admin is already logged in
    const token = localStorage.getItem('adminToken');
    const username = localStorage.getItem('adminUsername');
    
    if (token && username) {
      setIsAuthenticated(true);
      setAdmin({ username, token });
    }
    setLoading(false);
  }, []);

  const login = async (username, password) => {
    try {
      const response = await axios.post(`${BACKEND_URL}/api/admin/login`, {
        username,
        password
      });

      const { access_token, username: adminUsername } = response.data;
      
      localStorage.setItem('adminToken', access_token);
      localStorage.setItem('adminUsername', adminUsername);
      
      setIsAuthenticated(true);
      setAdmin({ username: adminUsername, token: access_token });
      
      return { success: true };
    } catch (error) {
      console.error('Login error:', error);
      return { 
        success: false, 
        message: error.response?.data?.detail || 'Login failed. Please check your credentials.' 
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('adminToken');
    localStorage.removeItem('adminUsername');
    setIsAuthenticated(false);
    setAdmin(null);
  };

  const getAuthHeaders = () => {
    const token = localStorage.getItem('adminToken');
    return {
      Authorization: `Bearer ${token}`
    };
  };

  return (
    <AdminContext.Provider value={{ 
      isAuthenticated, 
      admin, 
      login, 
      logout, 
      loading,
      getAuthHeaders 
    }}>
      {children}
    </AdminContext.Provider>
  );
};

export const useAdmin = () => {
  const context = useContext(AdminContext);
  if (!context) {
    throw new Error('useAdmin must be used within AdminProvider');
  }
  return context;
};
