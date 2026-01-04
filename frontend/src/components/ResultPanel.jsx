import React from 'react';
import api from '../services/api';
import './ResultPanel.css';

function ResultPanel({ result, onReset }) {
  if (!result) return null;

  return (
    <div className="result-panel">
      <div className="result-header">
        <h2>✅ QCM généré avec succès !</h2>
      </div>

      <div className="result-content">
        <div className="result-info">
          <h3>📄 Informations</h3>
          <p className="success-message">
            {result.message || 'Le PDF a été téléchargé automatiquement dans votre dossier de téléchargements.'}
          </p>
          {result.filename && (
            <p><strong>Fichier :</strong> {result.filename}</p>
          )}
        </div>
      </div>

      <div className="result-actions">
        <button className="reset-btn" onClick={onReset}>
          🔄 Créer un nouveau QCM
        </button>
      </div>
    </div>
  );
}

export default ResultPanel;
