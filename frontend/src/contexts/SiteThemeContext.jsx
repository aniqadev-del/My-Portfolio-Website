import React, { createContext, useContext, useEffect, useState } from 'react';

const SiteThemeContext = createContext(null);

export const useSiteTheme = () => useContext(SiteThemeContext);

export const SiteThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState(() => localStorage.getItem('siteTheme') || 'light');

  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.setAttribute('data-site-theme', 'dark');
    } else {
      document.documentElement.removeAttribute('data-site-theme');
    }
    localStorage.setItem('siteTheme', theme);
    return () => document.documentElement.removeAttribute('data-site-theme');
  }, [theme]);

  const toggle = () => setTheme((t) => (t === 'dark' ? 'light' : 'dark'));

  return (
    <SiteThemeContext.Provider value={{ theme, toggle, setTheme }}>
      {children}
    </SiteThemeContext.Provider>
  );
};
