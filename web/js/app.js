// Configuration de l'API
const API_URL = 'http://localhost:8000';

// État de l'application
let currentQuestions = [];
let availableTopics = [];

// ========================================
// INITIALISATION
// ========================================
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    checkAPIStatus();
    loadTopics();
    loadStats();
    initEventListeners();
});

// ========================================
// GESTION DES ONGLETS
// ========================================
function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.dataset.tab;
            
            // Désactiver tous les onglets
            tabButtons.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // Activer l'onglet sélectionné
            btn.classList.add('active');
            document.getElementById(`${targetTab}-tab`).classList.add('active');
            
            // Charger les données si nécessaire
            if (targetTab === 'stats') loadStats();
        });
    });
}

// ========================================
// VÉRIFICATION DE L'API
// ========================================
async function checkAPIStatus() {
    const statusBadge = document.getElementById('api-status');
    try {
        const response = await fetch(`${API_URL}/`);
        if (response.ok) {
            statusBadge.textContent = '✅ En ligne';
            statusBadge.className = 'status-badge online';
        } else {
            throw new Error('API non disponible');
        }
    } catch (error) {
        statusBadge.textContent = '❌ Hors ligne';
        statusBadge.className = 'status-badge offline';
        console.error('Erreur API:', error);
    }
}

// ========================================
// CHARGEMENT DES THÈMES
// ========================================
async function loadTopics() {
    try {
        const response = await fetch(`${API_URL}/api/topics`);
        availableTopics = await response.json();
        
        // Mettre à jour les selects de thèmes
        const topicSelects = ['topic', 'filter-topic'];
        topicSelects.forEach(selectId => {
            const select = document.getElementById(selectId);
            if (select) {
                select.innerHTML = availableTopics.map(topic => 
                    `<option value="${topic}">${topic}</option>`
                ).join('');
            }
        });
    } catch (error) {
        console.error('Erreur de chargement des thèmes:', error);
    }
}

// ========================================
// GÉNÉRATION DE PDF
// ========================================
function initEventListeners() {
    // Formulaire de génération
    document.getElementById('generate-form').addEventListener('submit', handleGenerate);
    
    // Bouton de prévisualisation
    document.getElementById('preview-btn').addEventListener('click', handlePreview);
    
    // Chargement des questions
    document.getElementById('load-questions-btn').addEventListener('click', loadQuestions);
    
    // Formulaire de création de question
    document.getElementById('question-form').addEventListener('submit', handleCreateQuestion);
    
    // Effacer le formulaire
    document.getElementById('clear-form-btn').addEventListener('click', clearQuestionForm);
}

async function handleGenerate(e) {
    e.preventDefault();
    
    const btn = e.target.querySelector('button[type="submit"]');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<span class="loading"></span> Génération...';
    btn.disabled = true;
    
    try {
        const formData = getGenerateFormData();
        
        const response = await fetch(`${API_URL}/api/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            throw new Error('Erreur de génération');
        }
        
        // Télécharger le PDF
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `qcm_${Date.now()}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        showMessage('✅ PDF généré avec succès !', 'success');
    } catch (error) {
        console.error('Erreur:', error);
        showMessage('❌ Erreur lors de la génération du PDF', 'error');
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

function getGenerateFormData() {
    const levelSelect = document.getElementById('level');
    const topicSelect = document.getElementById('topic');
    
    return {
        title: document.getElementById('title').value,
        n: parseInt(document.getElementById('num-questions').value),
        mode: document.getElementById('mode').value,
        seed: Math.floor(Math.random() * 10000),
        with_answers: true,
        filters: {
            level: Array.from(levelSelect.selectedOptions).map(opt => opt.value),
            topic: Array.from(topicSelect.selectedOptions).map(opt => opt.value),
            max_difficulty: document.getElementById('difficulty').value ? 
                parseInt(document.getElementById('difficulty').value) : null
        }
    };
}

// ========================================
// PRÉVISUALISATION
// ========================================
async function handlePreview() {
    const previewArea = document.getElementById('preview-area');
    const previewContent = document.getElementById('preview-content');
    
    previewContent.innerHTML = '<p class="placeholder">Chargement...</p>';
    previewArea.style.display = 'block';
    
    try {
        const formData = getGenerateFormData();
        const params = new URLSearchParams();
        
        if (formData.filters.level && formData.filters.level.length > 0) {
            formData.filters.level.forEach(l => params.append('level', l));
        }
        if (formData.filters.topic && formData.filters.topic.length > 0) {
            formData.filters.topic.forEach(t => params.append('topic', t));
        }
        if (formData.filters.max_difficulty) {
            params.append('max_difficulty', formData.filters.max_difficulty);
        }
        params.append('limit', formData.n);
        
        const response = await fetch(`${API_URL}/api/questions?${params}`);
        const questions = await response.json();
        
        if (questions.length === 0) {
            previewContent.innerHTML = '<p class="placeholder">Aucune question trouvée avec ces critères.</p>';
            return;
        }
        
        currentQuestions = questions;
        previewContent.innerHTML = questions.map((q, i) => renderQuestion(q, i + 1)).join('');
        
        // Rendre les mathématiques
        if (window.MathJax) {
            MathJax.typesetPromise([previewContent]);
        }
    } catch (error) {
        console.error('Erreur:', error);
        previewContent.innerHTML = '<p class="placeholder">Erreur de chargement</p>';
    }
}

// ========================================
// PARCOURIR LES QUESTIONS
// ========================================
async function loadQuestions() {
    const questionsList = document.getElementById('questions-list');
    const filterLevel = document.getElementById('filter-level').value;
    const filterTopic = document.getElementById('filter-topic').value;
    const searchTerm = document.getElementById('search').value;
    
    questionsList.innerHTML = '<p class="placeholder">Chargement...</p>';
    
    try {
        const params = new URLSearchParams();
        if (filterLevel) params.append('level', filterLevel);
        if (filterTopic) params.append('topic', filterTopic);
        params.append('limit', 50);
        
        const response = await fetch(`${API_URL}/api/questions?${params}`);
        const questions = await response.json();
        
        // Filtrer par recherche si nécessaire
        let filteredQuestions = questions;
        if (searchTerm) {
            const term = searchTerm.toLowerCase();
            filteredQuestions = questions.filter(q => 
                q.stem_tex.toLowerCase().includes(term) ||
                q.topic.toLowerCase().includes(term) ||
                q.uid.toLowerCase().includes(term)
            );
        }
        
        if (filteredQuestions.length === 0) {
            questionsList.innerHTML = '<p class="placeholder">Aucune question trouvée</p>';
            return;
        }
        
        questionsList.innerHTML = filteredQuestions.map((q, i) => renderQuestion(q, i + 1, true)).join('');
        
        // Rendre les mathématiques
        if (window.MathJax) {
            MathJax.typesetPromise([questionsList]);
        }
    } catch (error) {
        console.error('Erreur:', error);
        questionsList.innerHTML = '<p class="placeholder">Erreur de chargement</p>';
    }
}

function renderQuestion(q, index, withActions = false) {
    const difficultyStars = '⭐'.repeat(q.difficulty);
    
    return `
        <div class="question-item">
            <div class="question-header">
                <span style="font-weight: 700; color: var(--primary);">Question ${index}</span>
                <div class="question-meta">
                    <span class="badge badge-level">${q.level}</span>
                    <span class="badge badge-topic">${q.topic}</span>
                    <span class="badge badge-difficulty">${difficultyStars}</span>
                </div>
            </div>
            <div class="question-content">
                <p><strong>Énoncé :</strong> ${q.stem_tex}</p>
            </div>
            <div class="question-answer">
                <p><strong>Réponse :</strong> ${q.answer_tex}</p>
                ${q.distractors_tex ? `<p><strong>Distracteurs :</strong> ${q.distractors_tex}</p>` : ''}
            </div>
            ${withActions ? `
                <div style="margin-top: 10px; display: flex; gap: 10px;">
                    <button class="btn btn-secondary" onclick="editQuestion('${q.uid}')" style="font-size: 0.85rem; padding: 6px 12px;">
                        ✏️ Modifier
                    </button>
                    <button class="btn" onclick="deleteQuestion('${q.uid}')" style="font-size: 0.85rem; padding: 6px 12px; background: var(--danger); color: white;">
                        🗑️ Supprimer
                    </button>
                </div>
            ` : ''}
        </div>
    `;
}

// ========================================
// CRÉATION DE QUESTION
// ========================================
async function handleCreateQuestion(e) {
    e.preventDefault();
    
    const btn = e.target.querySelector('button[type="submit"]');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<span class="loading"></span> Enregistrement...';
    btn.disabled = true;
    
    try {
        const questionData = {
            uid: document.getElementById('q-uid').value,
            level: document.getElementById('q-level').value,
            topic: document.getElementById('q-topic').value,
            subtopic: document.getElementById('q-subtopic').value || '',
            skill: document.getElementById('q-skill').value || '',
            format: document.getElementById('q-format').value,
            difficulty: parseInt(document.getElementById('q-difficulty').value),
            time_s: parseInt(document.getElementById('q-time').value),
            stem_tex: document.getElementById('q-stem').value,
            answer_tex: document.getElementById('q-answer').value,
            distractors_tex: document.getElementById('q-distractors').value || '',
            figure_url: '',
            tags: document.getElementById('q-tags').value || '',
            status: document.getElementById('q-status').value,
            language: 'fr'
        };
        
        const response = await fetch(`${API_URL}/api/questions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(questionData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erreur de création');
        }
        
        showFormMessage('✅ Question créée avec succès !', 'success');
        clearQuestionForm();
        loadTopics(); // Recharger les thèmes
    } catch (error) {
        console.error('Erreur:', error);
        showFormMessage(`❌ ${error.message}`, 'error');
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

function clearQuestionForm() {
    document.getElementById('question-form').reset();
}

// ========================================
// MODIFICATION/SUPPRESSION
// ========================================
async function editQuestion(uid) {
    try {
        const response = await fetch(`${API_URL}/api/questions/${uid}`);
        const question = await response.json();
        
        // Remplir le formulaire
        document.getElementById('q-uid').value = question.uid;
        document.getElementById('q-level').value = question.level;
        document.getElementById('q-topic').value = question.topic;
        document.getElementById('q-subtopic').value = question.subtopic;
        document.getElementById('q-skill').value = question.skill;
        document.getElementById('q-format').value = question.format;
        document.getElementById('q-difficulty').value = question.difficulty;
        document.getElementById('q-time').value = question.time_s;
        document.getElementById('q-stem').value = question.stem_tex;
        document.getElementById('q-answer').value = question.answer_tex;
        document.getElementById('q-distractors').value = question.distractors_tex;
        document.getElementById('q-tags').value = question.tags;
        document.getElementById('q-status').value = question.status;
        
        // Changer d'onglet
        document.querySelector('[data-tab="create"]').click();
        
        showFormMessage('📝 Modification de la question. Changez l\'UID pour créer une copie.', 'info');
    } catch (error) {
        console.error('Erreur:', error);
        alert('Erreur de chargement de la question');
    }
}

async function deleteQuestion(uid) {
    if (!confirm(`Êtes-vous sûr de vouloir supprimer la question ${uid} ?`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/api/questions/${uid}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Erreur de suppression');
        }
        
        alert('✅ Question supprimée avec succès');
        loadQuestions(); // Recharger la liste
    } catch (error) {
        console.error('Erreur:', error);
        alert('❌ Erreur de suppression');
    }
}

// ========================================
// STATISTIQUES
// ========================================
async function loadStats() {
    const statsContent = document.getElementById('stats-content');
    statsContent.innerHTML = '<p class="placeholder">Chargement...</p>';
    
    try {
        const response = await fetch(`${API_URL}/api/stats`);
        const stats = await response.json();
        
        statsContent.innerHTML = `
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">${stats.total_questions}</div>
                    <div class="stat-label">Questions totales</div>
                </div>
            </div>
            
            <div class="stats-grid" style="margin-top: 30px;">
                <div class="stat-card">
                    <h3 style="margin-bottom: 15px;">Par niveau</h3>
                    <div class="stat-list">
                        ${Object.entries(stats.by_level).map(([level, count]) => `
                            <div class="stat-list-item">
                                <span>${level}</span>
                                <strong>${count}</strong>
                            </div>
                        `).join('')}
                    </div>
                </div>
                
                <div class="stat-card">
                    <h3 style="margin-bottom: 15px;">Par difficulté</h3>
                    <div class="stat-list">
                        ${Object.entries(stats.by_difficulty).map(([diff, count]) => `
                            <div class="stat-list-item">
                                <span>${'⭐'.repeat(parseInt(diff))}</span>
                                <strong>${count}</strong>
                            </div>
                        `).join('')}
                    </div>
                </div>
                
                <div class="stat-card">
                    <h3 style="margin-bottom: 15px;">Top thèmes</h3>
                    <div class="stat-list">
                        ${Object.entries(stats.by_topic).slice(0, 5).map(([topic, count]) => `
                            <div class="stat-list-item">
                                <span>${topic}</span>
                                <strong>${count}</strong>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    } catch (error) {
        console.error('Erreur:', error);
        statsContent.innerHTML = '<p class="placeholder">Erreur de chargement</p>';
    }
}

// ========================================
// UTILITAIRES
// ========================================
function showMessage(text, type) {
    // Créer un message temporaire en haut de la page
    const message = document.createElement('div');
    message.className = `message ${type}`;
    message.textContent = text;
    message.style.position = 'fixed';
    message.style.top = '20px';
    message.style.right = '20px';
    message.style.zIndex = '9999';
    message.style.maxWidth = '400px';
    
    document.body.appendChild(message);
    
    setTimeout(() => {
        message.style.transition = 'opacity 0.3s';
        message.style.opacity = '0';
        setTimeout(() => document.body.removeChild(message), 300);
    }, 3000);
}

function showFormMessage(text, type) {
    const messageDiv = document.getElementById('form-message');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = text;
    messageDiv.style.display = 'block';
    
    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 5000);
}
