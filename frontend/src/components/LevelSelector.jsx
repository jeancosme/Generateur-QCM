import React, { useState, useEffect } from 'react';
import api from '../services/api';
import './LevelSelector.css';

function LevelSelector({ selectedLevel, onLevelChange }) {
  const [levels, setLevels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadLevels();
  }, []);

  const loadLevels = async () => {
    try {
      setLoading(true);
      const data = await api.getLevels();
      setLevels(data);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Erreur chargement niveaux:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="level-selector loading">Chargement des niveaux...</div>;
  }

  if (error) {
    return (
      <div className="level-selector error">
        <p>❌ {error}</p>
        <button onClick={loadLevels}>Réessayer</button>
      </div>
    );
  }

  return (
    <div className="level-selector">
      <h2>📚 Sélectionnez un niveau</h2>
      <div className="level-buttons">
        {levels.map((level) => (
          <button
            key={level}
            className={`level-btn ${selectedLevel === level ? 'active' : ''}`}
            onClick={() => onLevelChange(level)}
          >
            {level}
          </button>
        ))}
      </div>
    </div>
  );
}

export default LevelSelector;
