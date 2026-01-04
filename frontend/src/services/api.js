/**
 * Service API pour communiquer avec le backend
 */

// Utiliser une URL relative en production (via nginx proxy) ou localhost:8000 en dev
const API_BASE_URL = import.meta.env.PROD ? '/api' : 'http://localhost:8000';

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
      const error = await response.text();
      throw new Error(error || 'Erreur lors de la génération du QCM');
    }
    
    // Télécharger directement le PDF
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    
    // Extraire le nom du fichier depuis les headers ou utiliser un nom par défaut
    const contentDisposition = response.headers.get('content-disposition');
    let filename = 'qcm.pdf';
    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
      if (filenameMatch) filename = filenameMatch[1];
    }
    
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    
    // Retourner un objet de succès pour le frontend
    return {
      success: true,
      filename: filename,
      message: 'QCM généré et téléchargé avec succès'
    };
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
