import React, { useState, useEffect } from 'react';
import api from '../services/api';
import './QuestionPreview.css';

function QuestionPreview({ selectedLevel, selectedThemes }) {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [totalCount, setTotalCount] = useState(0);

  useEffect(() => {
    if (selectedLevel && selectedThemes.length > 0) {
      loadQuestions();
    } else {
      setQuestions([]);
      setTotalCount(0);
    }
  }, [selectedLevel, selectedThemes]);

  const loadQuestions = async () => {
    try {
      setLoading(true);
      const data = await api.searchQuestions({
        level: selectedLevel,
        themes: selectedThemes,
        limit: 5, // Afficher seulement 5 questions en prévisualisation
      });
      setQuestions(data.questions || []);
      setTotalCount(data.total || 0);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Erreur chargement questions:', err);
    } finally {
      setLoading(false);
    }
  };

  if (!selectedLevel || selectedThemes.length === 0) {
    return null;
  }

  if (loading) {
    return (
      <div className="question-preview">
        <h2>👁️ Aperçu des questions</h2>
        <div className="loading-message">Chargement des questions...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="question-preview">
        <h2>👁️ Aperçu des questions</h2>
        <div className="error-message">
          <p>❌ {error}</p>
          <button onClick={loadQuestions}>Réessayer</button>
        </div>
      </div>
    );
  }

  return (
    <div className="question-preview">
      <h2>👁️ Aperçu des questions</h2>
      
      <div className="preview-info">
        <p className="total-count">
          📊 <strong>{totalCount}</strong> question(s) disponible(s) avec ces critères
        </p>
        {questions.length > 0 && (
          <p className="preview-note">
            Voici un aperçu de {questions.length} question(s) :
          </p>
        )}
      </div>

      {questions.length === 0 ? (
        <div className="no-questions">
          ⚠️ Aucune question trouvée avec ces critères
        </div>
      ) : (
        <div className="questions-list">
          {questions.map((question, index) => (
            <div key={index} className="question-card">
              <div className="question-header">
                <span className="question-number">Question {index + 1}</span>
                <span className="question-theme">{question.theme}</span>
              </div>
              <div className="question-content">
                <p className="question-text">{question.enonce}</p>
                {question.choices && question.choices.length > 0 && (
                  <ul className="choices-list">
                    {question.choices.map((choice, i) => (
                      <li key={i} className={question.correct_answer === i ? 'correct' : ''}>
                        {String.fromCharCode(65 + i)}. {choice}
                      </li>
                    ))}
                  </ul>
                )}
              </div>
              {question.difficulty && (
                <div className="question-footer">
                  <span className={`difficulty ${question.difficulty}`}>
                    {question.difficulty}
                  </span>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default QuestionPreview;
