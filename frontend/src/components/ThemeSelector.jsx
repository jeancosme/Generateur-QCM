import React, { useState, useEffect } from 'react';
import api from '../services/api';
import './ThemeSelector.css';

function ThemeSelector({ selectedLevel, selectedThemes, onThemesChange }) {
  const [themes, setThemes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (selectedLevel) {
      loadThemes();
    } else {
      setThemes([]);
    }
  }, [selectedLevel]);

  const loadThemes = async () => {
    try {
      setLoading(true);
      const data = await api.getThemes(selectedLevel);
      setThemes(data);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Erreur chargement thèmes:', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleTheme = (theme) => {
    if (selectedThemes.includes(theme)) {
      onThemesChange(selectedThemes.filter(t => t !== theme));
    } else {
      onThemesChange([...selectedThemes, theme]);
    }
  };

  const selectAll = () => {
    onThemesChange(themes);
  };

  const clearAll = () => {
    onThemesChange([]);
  };

  if (!selectedLevel) {
    return (
      <div className="theme-selector">
        <p className="info-message">👆 Veuillez d'abord sélectionner un niveau</p>
      </div>
    );
  }

  if (loading) {
    return <div className="theme-selector loading">Chargement des thèmes...</div>;
  }

  if (error) {
    return (
      <div className="theme-selector error">
        <p>❌ {error}</p>
        <button onClick={loadThemes}>Réessayer</button>
      </div>
    );
  }

  return (
    <div className="theme-selector">
      <div className="theme-header">
        <h2>🎯 Sélectionnez les thèmes</h2>
        <div className="theme-actions">
          <button className="action-btn" onClick={selectAll}>
            Tout sélectionner
          </button>
          <button className="action-btn" onClick={clearAll}>
            Tout désélectionner
          </button>
        </div>
      </div>
      
      <div className="selected-count">
        {selectedThemes.length} thème(s) sélectionné(s)
      </div>

      <div className="theme-grid">
        {themes.map((theme) => (
          <div
            key={theme}
            className={`theme-card ${selectedThemes.includes(theme) ? 'selected' : ''}`}
            onClick={() => toggleTheme(theme)}
          >
            <span className="theme-icon">
              {selectedThemes.includes(theme) ? '✅' : '⚪'}
            </span>
            <span className="theme-name">{theme}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ThemeSelector;
