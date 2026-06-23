import React, { useState, useRef, useEffect } from 'react';
import { ChevronDown, Check } from 'lucide-react';

const EMOJI_GROUPS = {
  'Tech & AI': ['🤖', '⚙️', '💻', '🖥️', '📱', '🧠', '🔌', '🛰️', '🔬', '🧪', '📡', '🖲️'],
  'Automation & Tools': ['🔧', '🛠️', '🔩', '🧰', '⚡', '🔄', '⏱️', '⏰', '🔔', '🪄', '🎛️', '🧲'],
  'Data & Analytics': ['📊', '📈', '📉', '🗂️', '🗃️', '📋', '📑', '🧮', '🔢', '💾', '🗄️', '📁'],
  'Business & Growth': ['💼', '💡', '🚀', '🎯', '🏆', '📌', '💰', '🤝', '📣', '🌐', '🏢', '🔑'],
  'Communication': ['✉️', '📧', '💬', '📞', '☎️', '📨', '📥', '📤', '🗨️', '📢', '🔖', '🪧'],
  'General': ['✅', '⭐', '✨', '🔥', '❤️', '🛡️', '🧩', '🎨', '📦', '🌟', '⚖️', '🧭'],
};

export const EmojiPicker = ({ value, onChange }) => {
  const [open, setOpen] = useState(false);
  const [custom, setCustom] = useState('');
  const ref = useRef(null);

  useEffect(() => {
    const handler = (e) => {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const select = (emoji) => {
    onChange(emoji);
    setOpen(false);
  };

  const applyCustom = () => {
    const v = custom.trim();
    if (v) {
      onChange(v);
      setCustom('');
      setOpen(false);
    }
  };

  return (
    <div className="relative" ref={ref}>
      <button
        type="button"
        data-testid="emoji-picker-trigger"
        onClick={() => setOpen((o) => !o)}
        className="w-full flex items-center justify-between px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent hover:bg-gray-50 transition-colors"
      >
        <span className="flex items-center space-x-2">
          <span className="text-2xl leading-none">{value || '🙂'}</span>
          <span className="text-sm text-gray-600">
            {value ? 'Selected icon' : 'Choose an icon'}
          </span>
        </span>
        <ChevronDown className={`w-4 h-4 text-gray-500 transition-transform ${open ? 'rotate-180' : ''}`} />
      </button>

      {open && (
        <div
          data-testid="emoji-picker-panel"
          className="absolute z-50 mt-2 w-full bg-white border border-gray-200 rounded-xl shadow-lg p-3 max-h-72 overflow-y-auto"
        >
          {Object.entries(EMOJI_GROUPS).map(([group, emojis]) => (
            <div key={group} className="mb-3">
              <p className="text-xs font-semibold text-gray-500 mb-1.5 uppercase tracking-wide">{group}</p>
              <div className="grid grid-cols-8 gap-1">
                {emojis.map((emoji) => (
                  <button
                    key={emoji}
                    type="button"
                    data-testid={`emoji-option-${emoji}`}
                    onClick={() => select(emoji)}
                    className={`text-xl p-1.5 rounded-lg hover:bg-blue-100 transition-colors ${
                      value === emoji ? 'bg-blue-100 ring-2 ring-blue-500' : ''
                    }`}
                  >
                    {emoji}
                  </button>
                ))}
              </div>
            </div>
          ))}

          <div className="border-t border-gray-100 pt-3">
            <p className="text-xs font-semibold text-gray-500 mb-1.5 uppercase tracking-wide">
              Add a custom emoji / icon
            </p>
            <div className="flex space-x-2">
              <input
                type="text"
                data-testid="emoji-custom-input"
                value={custom}
                onChange={(e) => setCustom(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), applyCustom())}
                placeholder="Paste any emoji e.g. 🦾"
                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button
                type="button"
                data-testid="emoji-custom-apply"
                onClick={applyCustom}
                className="flex items-center space-x-1 px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm"
              >
                <Check className="w-4 h-4" />
                <span>Use</span>
              </button>
            </div>
            <p className="text-xs text-gray-400 mt-1">
              Tip: press Win + . (Windows) or Ctrl + Cmd + Space (Mac) to open the emoji keyboard.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default EmojiPicker;
