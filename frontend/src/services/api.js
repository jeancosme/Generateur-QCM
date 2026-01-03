/**
 * Service API pour communiquer avec le backend
 */

const API_BASE_URL = 'http://localhost:8000';

class ApiService {
  /**
   * Récupérer tous les niveaux disponibles
   */
  async getLevels() {
    const response = await fetch(`${API_BASE_URL}/levels`);
    if (!response.ok) throw new Error('Erreur lors de la récupération des niveaux');
    return response.json();
  }

  /**
   * Récupérer les thèmes pour un niveau donné
   */
  async getThemes(level) {
    const url = level 
      ? `${API_BASE_URL}/themes?level=${level}`
      : `${API_BASE_URL}/themes`;
    const response = await fetch(url);
    if (!response.ok) throw new Error('Erreur lors de la récupération des thèmes');
    return response.json();
  }

  /**
   * Récupérer toute la taxonomie
   */
  async getTaxonomy() {
    const response = await fetch(`${API_BASE_URL}/taxonomy`);
    if (!response.ok) throw new Error('Erreur lors de la récupération de la taxonomie');
    return response.json();
  }

  /**
   * Chercher des questions avec des filtres
   */
  async searchQuestions(filters = {}) {
    const params = new URLSearchParams();
    if (filters.level) params.append('level', filters.level);
    if (filters.themes && filters.themes.length > 0) {
      filters.themes.forEach(theme => params.append('themes', theme));
    }
    if (filters.difficulty) params.append('difficulty', filters.difficulty);
    if (filters.skip !== undefined) params.append('skip', filters.skip);
    if (filters.limit !== undefined) params.append('limit', filters.limit);

    const response = await fetch(`${API_BASE_URL}/questions/search?${params}`);
    if (!response.ok) throw new Error('Erreur lors de la recherche de questions');
    return response.json();
  }

  /**
   * Générer un QCM
   */
  async generateQCM(config) {
    const response = await fetch(`${API_BASE_URL}/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(config),
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Erreur lors de la génération du QCM');
    }
    return response.json();
  }

  /**
   * Télécharger un fichier PDF
   */
  async downloadPDF(filename) {
    const response = await fetch(`${API_BASE_URL}/download/pdf/${filename}`);
    if (!response.ok) throw new Error('Erreur lors du téléchargement du PDF');
    
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  }

  /**
   * Télécharger un fichier HTML
   */
  async downloadHTML(filename) {
    const response = await fetch(`${API_BASE_URL}/download/html/${filename}`);
    if (!response.ok) throw new Error('Erreur lors du téléchargement du HTML');
    
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  }

  /**
   * Obtenir les statistiques
   */
  async getStats() {
    const response = await fetch(`${API_BASE_URL}/stats`);
    if (!response.ok) throw new Error('Erreur lors de la récupération des statistiques');
    return response.json();
  }
}

export default new ApiService();
