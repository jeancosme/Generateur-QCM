import React, { useState } from 'react';
import './ConfigPanel.css';

function ConfigPanel({ selectedLevel, selectedThemes, onGenerate }) {
  const [numQuestions, setNumQuestions] = useState(10);
  const [difficulty, setDifficulty] = useState('all');
  const [outputFormat, setOutputFormat] = useState('pdf');
  const [includeAnswers, setIncludeAnswers] = useState(true);
  const [generating, setGenerating] = useState(false);

  const canGenerate = selectedLevel && selectedThemes.length > 0 && numQuestions > 0;

  const handleGenerate = async () => {
    if (!canGenerate) return;

    const config = {
      level: selectedLevel,
      themes: selectedThemes,
      n_questions: numQuestions,
      difficulty: difficulty === 'all' ? null : difficulty,
      output_format: outputFormat,
      include_answers: includeAnswers,
    };

    setGenerating(true);
    try {
      await onGenerate(config);
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="config-panel">
      <h2>⚙️ Configuration du QCM</h2>

      <div className="config-grid">
        <div className="config-item">
          <label htmlFor="numQuestions">
            Nombre de questions
          </label>
          <input
            id="numQuestions"
            type="number"
            min="1"
            max="100"
            value={numQuestions}
            onChange={(e) => setNumQuestions(parseInt(e.target.value) || 1)}
            className="config-input"
          />
        </div>

        <div className="config-item">
          <label htmlFor="difficulty">
            Difficulté
          </label>
          <select
            id="difficulty"
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
            className="config-select"
          >
            <option value="all">Toutes</option>
            <option value="facile">Facile</option>
            <option value="moyen">Moyen</option>
            <option value="difficile">Difficile</option>
          </select>
        </div>

        <div className="config-item">
          <label htmlFor="outputFormat">
            Format de sortie
          </label>
          <select
            id="outputFormat"
            value={outputFormat}
            onChange={(e) => setOutputFormat(e.target.value)}
            className="config-select"
          >
            <option value="pdf">PDF</option>
            <option value="html">HTML</option>
          </select>
        </div>

        <div className="config-item checkbox-item">
          <label>
            <input
              type="checkbox"
              checked={includeAnswers}
              onChange={(e) => setIncludeAnswers(e.target.checked)}
            />
            <span>Inclure les réponses</span>
          </label>
        </div>
      </div>

      <div className="config-summary">
        <h3>📋 Résumé</h3>
        <ul>
          <li><strong>Niveau :</strong> {selectedLevel || 'Non sélectionné'}</li>
          <li><strong>Thèmes :</strong> {selectedThemes.length > 0 ? selectedThemes.join(', ') : 'Aucun'}</li>
          <li><strong>Questions :</strong> {numQuestions}</li>
          <li><strong>Difficulté :</strong> {difficulty === 'all' ? 'Toutes' : difficulty}</li>
        </ul>
      </div>

      <button
        className={`generate-btn ${!canGenerate || generating ? 'disabled' : ''}`}
        onClick={handleGenerate}
        disabled={!canGenerate || generating}
      >
        {generating ? '⏳ Génération en cours...' : '🚀 Générer le QCM'}
      </button>

      {!canGenerate && (
        <p className="warning-message">
          ⚠️ Veuillez sélectionner un niveau et au moins un thème
        </p>
      )}
    </div>
  );
}

export default ConfigPanel;
