import React from 'react';
import api from '../services/api';
import './ResultPanel.css';

function ResultPanel({ result, onReset }) {
  if (!result) return null;

  const handleDownload = async () => {
    try {
      if (result.output_format === 'pdf') {
        await api.downloadPDF(result.pdf_filename);
      } else if (result.output_format === 'html') {
        await api.downloadHTML(result.html_filename);
      }
    } catch (error) {
      console.error('Erreur téléchargement:', error);
      alert('Erreur lors du téléchargement: ' + error.message);
    }
  };

  return (
    <div className="result-panel">
      <div className="result-header">
        <h2>✅ QCM généré avec succès !</h2>
      </div>

      <div className="result-content">
        <div className="result-info">
          <h3>📄 Informations</h3>
          <ul>
            <li><strong>Niveau :</strong> {result.level}</li>
            <li><strong>Thèmes :</strong> {result.themes.join(', ')}</li>
            <li><strong>Nombre de questions :</strong> {result.n_questions}</li>
            <li><strong>Format :</strong> {result.output_format.toUpperCase()}</li>
            {result.pdf_filename && (
              <li><strong>Fichier PDF :</strong> {result.pdf_filename}</li>
            )}
            {result.html_filename && (
              <li><strong>Fichier HTML :</strong> {result.html_filename}</li>
            )}
          </ul>
        </div>

        {result.questions && result.questions.length > 0 && (
          <div className="result-questions">
            <h3>📝 Questions générées</h3>
            <div className="questions-summary">
              {result.questions.map((q, index) => (
                <div key={index} className="question-summary-item">
                  <span className="q-number">{index + 1}.</span>
                  <span className="q-theme">{q.theme}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="result-actions">
        <button className="download-btn" onClick={handleDownload}>
          📥 Télécharger le QCM
        </button>
        <button className="reset-btn" onClick={onReset}>
          🔄 Créer un nouveau QCM
        </button>
      </div>
    </div>
  );
}

export default ResultPanel;
