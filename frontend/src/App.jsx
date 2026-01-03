import { useState } from 'react'
import './App.css'
import Header from './components/Header'
import LevelSelector from './components/LevelSelector'
import ThemeSelector from './components/ThemeSelector'
import ConfigPanel from './components/ConfigPanel'
import QuestionPreview from './components/QuestionPreview'
import ResultPanel from './components/ResultPanel'
import api from './services/api'

function App() {
  const [selectedLevel, setSelectedLevel] = useState(null)
  const [selectedThemes, setSelectedThemes] = useState([])
  const [generationResult, setGenerationResult] = useState(null)
  const [error, setError] = useState(null)

  const handleLevelChange = (level) => {
    setSelectedLevel(level)
    setSelectedThemes([])
    setGenerationResult(null)
    setError(null)
  }

  const handleThemesChange = (themes) => {
    setSelectedThemes(themes)
    setGenerationResult(null)
    setError(null)
  }

  const handleGenerate = async (config) => {
    try {
      setError(null)
      const result = await api.generateQCM(config)
      setGenerationResult(result)
    } catch (err) {
      setError(err.message)
      console.error('Erreur génération:', err)
      alert('Erreur lors de la génération: ' + err.message)
    }
  }

  const handleReset = () => {
    setGenerationResult(null)
    setError(null)
  }

  return (
    <div className="app">
      <Header />
      
      <main className="app-container">
        {generationResult ? (
          <ResultPanel 
            result={generationResult} 
            onReset={handleReset}
          />
        ) : (
          <>
            <LevelSelector
              selectedLevel={selectedLevel}
              onLevelChange={handleLevelChange}
            />

            <ThemeSelector
              selectedLevel={selectedLevel}
              selectedThemes={selectedThemes}
              onThemesChange={handleThemesChange}
            />

            {selectedLevel && selectedThemes.length > 0 && (
              <>
                <QuestionPreview
                  selectedLevel={selectedLevel}
                  selectedThemes={selectedThemes}
                />

                <ConfigPanel
                  selectedLevel={selectedLevel}
                  selectedThemes={selectedThemes}
                  onGenerate={handleGenerate}
                />
              </>
            )}
          </>
        )}

        {error && (
          <div className="error-banner">
            ❌ {error}
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>© 2026 Générateur de QCM - Fait avec ❤️</p>
      </footer>
    </div>
  )
}

export default App
