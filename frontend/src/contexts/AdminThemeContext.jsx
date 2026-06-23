import React, { createContext, useContext, useEffect, useState } from 'react';

export const ADMIN_THEMES = [
  { id: 'light', name: 'Light', icon: 'sun' },
  { id: 'dark', name: 'Dark', icon: 'moon' },
  { id: 'cyber', name: 'Cyber Purple', icon: 'sparkles' },
  { id: 'mint', name: 'Mint', icon: 'leaf' },
];

const AdminThemeContext = createContext(null);

export const useAdminTheme = () => useContext(AdminThemeContext);

export const AdminThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState(() => localStorage.getItem('adminTheme') || 'light');

  useEffect(() => {
    document.documentElement.setAttribute('data-admin-theme', theme);
    localStorage.setItem('adminTheme', theme);
    return () => {
      document.documentElement.removeAttribute('data-admin-theme');
    };
  }, [theme]);

  return (
    <AdminThemeContext.Provider value={{ theme, setTheme, themes: ADMIN_THEMES }}>
      {children}
    </AdminThemeContext.Provider>
  );
};
