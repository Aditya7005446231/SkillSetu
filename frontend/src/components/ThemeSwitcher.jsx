/*
From Uiverse.io by dalbrechtmartin - https://uiverse.io/dalbrechtmartin/brave-donkey-91
MIT License, Copyright (c) dalbrechtmartin (Danaé A.M.)
*/
import { useEffect, useState } from 'react'
import '../styles/theme-toggle.css'

export function ThemeSwitcher() {
  const [isDark, setIsDark] = useState(() => {
    return localStorage.getItem('skillsetu-theme') === 'dark'
  })

  useEffect(() => {
    if (isDark) {
      document.body.classList.add('dark-mode')
      localStorage.setItem('skillsetu-theme', 'dark')
    } else {
      document.body.classList.remove('dark-mode')
      localStorage.setItem('skillsetu-theme', 'light')
    }
  }, [isDark])

  return (
    <label className="grim-toggle" title="Toggle Light / Dark Theme">
      <span className="grim-toggle__text" style={{ fontSize: '0.78rem' }}>Theme</span>
      <input
        className="grim-toggle__input"
        type="checkbox"
        role="switch"
        checked={isDark}
        onChange={(e) => setIsDark(e.target.checked)}
      />
      <span className="grim-toggle__track" aria-hidden="true">
        <span className="grim-toggle__stars">✦✦</span>
        <span className="grim-toggle__thumb">
          <svg className="grim-toggle__icon grim-toggle__sun" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="4"></circle>
            <path
              d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"
            ></path>
          </svg>
          <svg className="grim-toggle__icon grim-toggle__moon" viewBox="0 0 24 24">
            <path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"></path>
          </svg>
        </span>
      </span>
      <span className="grim-toggle__state" aria-hidden="true"></span>
    </label>
  )
}

export default ThemeSwitcher
