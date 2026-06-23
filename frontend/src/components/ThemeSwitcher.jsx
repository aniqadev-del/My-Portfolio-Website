import React, { useState, useRef, useEffect } from 'react';
import { Sun, Moon, Sparkles, Leaf, Palette, Check, ChevronDown } from 'lucide-react';
import { useAdminTheme } from '../contexts/AdminThemeContext';

const ICONS = {
  sun: Sun,
  moon: Moon,
  sparkles: Sparkles,
  leaf: Leaf,
};

export const ThemeSwitcher = () => {
  const { theme, setTheme, themes } = useAdminTheme();
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    const handler = (e) => {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const current = themes.find((t) => t.id === theme) || themes[0];
  const CurrentIcon = ICONS[current.icon] || Palette;

  return (
    <div className="relative" ref={ref}>
      <button
        type="button"
        data-testid="theme-switcher-trigger"
        onClick={() => setOpen((o) => !o)}
        className="flex items-center space-x-2 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors border border-gray-200"
        title="Change theme"
      >
        <CurrentIcon className="w-5 h-5" />
        <span className="hidden sm:inline text-sm font-medium">{current.name}</span>
        <ChevronDown className={`w-4 h-4 transition-transform ${open ? 'rotate-180' : ''}`} />
      </button>

      {open && (
        <div
          data-testid="theme-switcher-menu"
          className="absolute right-0 mt-2 w-48 bg-white border border-gray-200 rounded-xl shadow-lg p-1.5 z-50"
        >
          {themes.map((t) => {
            const Icon = ICONS[t.icon] || Palette;
            const active = t.id === theme;
            return (
              <button
                key={t.id}
                type="button"
                data-testid={`theme-option-${t.id}`}
                onClick={() => {
                  setTheme(t.id);
                  setOpen(false);
                }}
                className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm transition-colors ${
                  active ? 'bg-blue-50 text-blue-600 font-medium' : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                <span className="flex items-center space-x-2">
                  <Icon className="w-4 h-4" />
                  <span>{t.name}</span>
                </span>
                {active && <Check className="w-4 h-4" />}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default ThemeSwitcher;
