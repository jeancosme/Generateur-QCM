// Script principal pour l'application Olympiades de Mathématiques
// Gère l'authentification et l'affichage des résultats

// Variables globales
let currentEstablishment = null;
let currentUAI = null;
let allResults = []; // Stocke tous les résultats de l'établissement

// Attendre que le DOM soit chargé
document.addEventListener('DOMContentLoaded', function() {
    console.log('Application Olympiades chargée');
    console.log(`${ESTABLISHMENTS_CREDENTIALS.length} établissements configurés`);
    console.log(`${RESULTS_DATA.length} résultats disponibles`);
    
    // Gérer la soumission du formulaire d'authentification
    const authForm = document.getElementById('auth-form');
    if (authForm) {
        authForm.addEventListener('submit', handleAuthentication);
    }
    
    // Bouton de déconnexion
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }
    
    // Moteur de recherche
    const searchInput = document.getElementById('student-search');
    if (searchInput) {
        searchInput.addEventListener('input', handleSearch);
    }
    
    // Boutons d'export
    const exportPdfBtn = document.getElementById('export-pdf-btn');
    const exportExcelBtn = document.getElementById('export-excel-btn');
    const exportCsvBtn = document.getElementById('export-csv-btn');
    const exportOdtBtn = document.getElementById('export-odt-btn');
    
    if (exportPdfBtn) exportPdfBtn.addEventListener('click', exportToPDF);
    if (exportExcelBtn) exportExcelBtn.addEventListener('click', exportToExcel);
    if (exportCsvBtn) exportCsvBtn.addEventListener('click', exportToCSV);
    if (exportOdtBtn) exportOdtBtn.addEventListener('click', exportToODT);
    
    // Vérifier si déjà authentifié (session)
    checkExistingAuth();
});

/**
 * Vérifie si l'utilisateur est déjà authentifié
 */
function checkExistingAuth() {
    const savedUAI = sessionStorage.getItem('authenticated_uai');
    const savedName = sessionStorage.getItem('establishment_name');
    
    if (savedUAI && savedName) {
        // Vérifier que les identifiants sont toujours valides
        const establishment = ESTABLISHMENTS_CREDENTIALS.find(e => e.uai.toUpperCase() === savedUAI.toUpperCase());
        if (establishment) {
            currentEstablishment = savedName;
            currentUAI = savedUAI;
            showResults(savedUAI, savedName);
        } else {
            // Session invalide, nettoyer
            sessionStorage.clear();
        }
    }
}

/**
 * Gère l'authentification de l'établissement
 */
function handleAuthentication(event) {
    event.preventDefault();
    
    const uaiInput = document.getElementById('uai');
    const passwordInput = document.getElementById('password');
    
    const uai = uaiInput.value.trim().toUpperCase();
    const password = passwordInput.value.trim();
    
    // Rechercher l'établissement
    const establishment = ESTABLISHMENTS_CREDENTIALS.find(e => 
        e.uai.toUpperCase() === uai
    );
    
    if (!establishment) {
        showError('Code UAI non trouvé. Vérifiez votre code UAI.');
        return;
    }
    
    // Vérifier le mot de passe
    if (establishment.password !== password) {
        showError('Mot de passe incorrect. Vérifiez votre mot de passe.');
        return;
    }
    
    // Authentification réussie
    console.log('Authentification réussie pour:', establishment.name);
    
    // Sauvegarder dans la session
    sessionStorage.setItem('authenticated_uai', establishment.uai);
    sessionStorage.setItem('establishment_name', establishment.name);
    
    currentEstablishment = establishment.name;
    currentUAI = establishment.uai;
    
    // Afficher les résultats
    showResults(establishment.uai, establishment.name);
}

/**
 * Affiche un message d'erreur
 */
function showError(message) {
    // Supprimer l'ancien message d'erreur s'il existe
    const oldError = document.querySelector('.error-message');
    if (oldError) {
        oldError.remove();
    }
    
    const authForm = document.getElementById('auth-form');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.style.cssText = 'background: #fee2e2; border: 1px solid #ef4444; color: #dc2626; padding: 12px; border-radius: 8px; margin-top: 16px; font-size: 14px;';
    errorDiv.textContent = '❌ ' + message;
    
    authForm.appendChild(errorDiv);
    
    // Retirer le message après 5 secondes
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

/**
 * Affiche les résultats pour un établissement
 */
function showResults(uai, establishmentName) {
    console.log(`Affichage des résultats pour ${establishmentName} (${uai})`);
    
    // Cacher la section d'authentification
    const authSection = document.getElementById('auth-section');
    authSection.style.display = 'none';
    
    // Afficher la section des résultats
    const resultsSection = document.getElementById('results-section');
    resultsSection.style.display = 'block';
    
    // Mettre à jour le nom de l'établissement
    const establishmentNameElement = document.getElementById('establishment-name');
    if (establishmentNameElement) {
        establishmentNameElement.textContent = establishmentName;
    }
    
    // Filtrer les résultats pour cet établissement
    allResults = RESULTS_DATA.filter(result => 
        result.uai && result.uai.toUpperCase() === uai.toUpperCase()
    );
    
    console.log(`${allResults.length} résultats trouvés`);
    
    // Afficher les résultats
    displayResults(allResults);
    
    // Réinitialiser la recherche
    const searchInput = document.getElementById('student-search');
    if (searchInput) {
        searchInput.value = '';
    }
    
    // Scroll vers le haut
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Gère la recherche d'élève
 */
function handleSearch(event) {
    const searchTerm = event.target.value.toLowerCase().trim();
    
    if (!searchTerm) {
        // Si pas de recherche, afficher tous les résultats
        displayResults(allResults);
        return;
    }
    
    // Filtrer les résultats
    const filteredResults = allResults.filter(result => {
        const studentName = (result.studentName || '').toLowerCase();
        return studentName.includes(searchTerm);
    });
    
    displayResults(filteredResults);
}

/**
 * Affiche les résultats dans le tableau
 */
function displayResults(results) {
    const tbody = document.querySelector('#results-table tbody');
    
    if (!tbody) {
        console.error('Tableau des résultats non trouvé');
        return;
    }
    
    // Vider le tableau
    tbody.innerHTML = '';
    
    // Mettre à jour le compteur
    const studentCount = document.getElementById('student-count');
    if (studentCount) {
        studentCount.textContent = `${results.length} élève${results.length > 1 ? 's' : ''}`;
    }
    
    if (results.length === 0) {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td colspan="6" style="text-align: center; padding: 40px; color: #64748b;">
                Aucun résultat trouvé.
            </td>
        `;
        tbody.appendChild(tr);
        return;
    }
    
    // Trier par nom d'élève
    results.sort((a, b) => {
        const nameA = a.studentName || '';
        const nameB = b.studentName || '';
        return nameA.localeCompare(nameB, 'fr');
    });
    
    // Ajouter chaque résultat
    results.forEach(result => {
        const tr = document.createElement('tr');
        
        // Nom de l'élève
        const tdName = document.createElement('td');
        tdName.textContent = result.studentName || '-';
        tr.appendChild(tdName);
        
        // Date de naissance
        const tdBirth = document.createElement('td');
        if (result.birthDate) {
            const date = new Date(result.birthDate);
            tdBirth.textContent = date.toLocaleDateString('fr-FR');
        } else {
            tdBirth.textContent = '-';
        }
        tr.appendChild(tdBirth);
        
        // Niveau
        const tdLevel = document.createElement('td');
        tdLevel.textContent = result.level || '-';
        tr.appendChild(tdLevel);
        
        // Résultat individuel
        const tdIndividual = document.createElement('td');
        tdIndividual.innerHTML = formatResult(result.individualResult, result.individualRank);
        tr.appendChild(tdIndividual);
        
        // Résultat équipe
        const tdTeam = document.createElement('td');
        tdTeam.innerHTML = formatResult(result.teamResult, result.teamRank);
        tr.appendChild(tdTeam);
        
        // Membres de l'équipe
        const tdMembers = document.createElement('td');
        if (result.teamMembers && result.teamMembers.length > 0) {
            tdMembers.innerHTML = result.teamMembers.join('<br>');
        } else {
            tdMembers.textContent = '-';
        }
        tr.appendChild(tdMembers);
        
        tbody.appendChild(tr);
    });
}

/**
 * Formate un résultat avec son classement
 */
function formatResult(result, rank) {
    if (!result && !rank) {
        return '-';
    }
    
    let html = '';
    
    if (result) {
        html += `<div style="font-weight: 500;">${result}</div>`;
    }
    
    if (rank) {
        html += `<div style="font-size: 0.9em; color: #64748b; margin-top: 4px;">Classement : ${rank}</div>`;
    }
    
    return html || '-';
}

/**
 * Gère la déconnexion
 */
function handleLogout() {
    // Nettoyer la session
    sessionStorage.clear();
    
    currentEstablishment = null;
    currentUAI = null;
    
    // Réinitialiser le formulaire
    const authForm = document.getElementById('auth-form');
    if (authForm) {
        authForm.reset();
    }
    
    // Cacher les résultats
    const resultsSection = document.getElementById('results-section');
    resultsSection.style.display = 'none';
    
    // Afficher l'authentification
    const authSection = document.getElementById('auth-section');
    authSection.style.display = 'block';
    
    // Scroll vers le haut
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    console.log('Déconnexion effectuée');
}

/**
 * Exporte les résultats en PDF
 */
function exportToPDF() {
    if (!window.jspdf) {
        alert('Erreur : bibliothèque PDF non chargée');
        return;
    }
    
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF('l', 'mm', 'a4'); // Format paysage
    
    // Titre
    doc.setFontSize(16);
    doc.text(`Résultats Olympiades de Mathématiques - ${currentEstablishment}`, 14, 15);
    
    // Date
    doc.setFontSize(10);
    doc.text(`Généré le ${new Date().toLocaleDateString('fr-FR')}`, 14, 22);
    
    // Préparer les données pour le tableau
    const tableData = allResults.map(result => [
        result.studentName || '-',
        result.birthDate ? new Date(result.birthDate).toLocaleDateString('fr-FR') : '-',
        result.level || '-',
        result.individualResult || '-',
        result.teamResult || '-',
        result.teamMembers && result.teamMembers.length > 0 ? result.teamMembers.join(', ') : '-'
    ]);
    
    // Créer le tableau
    doc.autoTable({
        startY: 28,
        head: [['Nom Prénom', 'Date de naissance', 'Niveau', 'Résultat Individuel', 'Résultat Équipe', 'Membres Équipe']],
        body: tableData,
        styles: { fontSize: 8, cellPadding: 2 },
        headStyles: { fillColor: [37, 99, 235], textColor: 255 },
        alternateRowStyles: { fillColor: [248, 250, 252] },
        margin: { top: 28 }
    });
    
    // Sauvegarder
    const filename = `resultats_olympiades_${currentEstablishment.replace(/[^a-z0-9]/gi, '_')}_${new Date().toISOString().split('T')[0]}.pdf`;
    doc.save(filename);
}

/**
 * Exporte les résultats en Excel
 */
function exportToExcel() {
    if (!window.XLSX) {
        alert('Erreur : bibliothèque Excel non chargée');
        return;
    }
    
    // Préparer les données
    const data = allResults.map(result => ({
        'Nom Prénom': result.studentName || '-',
        'Date de naissance': result.birthDate ? new Date(result.birthDate).toLocaleDateString('fr-FR') : '-',
        'Niveau': result.level || '-',
        'Résultat Individuel': result.individualResult || '-',
        'Classement Individuel': result.individualRank || '-',
        'Résultat Équipe': result.teamResult || '-',
        'Classement Équipe': result.teamRank || '-',
        'Membres Équipe': result.teamMembers && result.teamMembers.length > 0 ? result.teamMembers.join(', ') : '-'
    }));
    
    // Créer le classeur
    const ws = XLSX.utils.json_to_sheet(data);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Résultats');
    
    // Sauvegarder
    const filename = `resultats_olympiades_${currentEstablishment.replace(/[^a-z0-9]/gi, '_')}_${new Date().toISOString().split('T')[0]}.xlsx`;
    XLSX.writeFile(wb, filename);
}

/**
 * Exporte les résultats en CSV
 */
function exportToCSV() {
    // Préparer les en-têtes
    const headers = ['Nom Prénom', 'Date de naissance', 'Niveau', 'Résultat Individuel', 'Classement Individuel', 'Résultat Équipe', 'Classement Équipe', 'Membres Équipe'];
    
    // Préparer les données
    const rows = allResults.map(result => [
        result.studentName || '-',
        result.birthDate ? new Date(result.birthDate).toLocaleDateString('fr-FR') : '-',
        result.level || '-',
        result.individualResult || '-',
        result.individualRank || '-',
        result.teamResult || '-',
        result.teamRank || '-',
        result.teamMembers && result.teamMembers.length > 0 ? result.teamMembers.join(', ') : '-'
    ]);
    
    // Créer le contenu CSV
    let csvContent = '\uFEFF'; // BOM pour UTF-8
    csvContent += headers.join(';') + '\n';
    rows.forEach(row => {
        csvContent += row.map(cell => `"${cell}"`).join(';') + '\n';
    });
    
    // Télécharger
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const filename = `resultats_olympiades_${currentEstablishment.replace(/[^a-z0-9]/gi, '_')}_${new Date().toISOString().split('T')[0]}.csv`;
    
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
    URL.revokeObjectURL(link.href);
}

/**
 * Exporte les résultats en ODT (format OpenDocument)
 */
function exportToODT() {
    if (!window.XLSX) {
        alert('Erreur : bibliothèque Excel non chargée');
        return;
    }
    
    // Préparer les données
    const data = allResults.map(result => ({
        'Nom Prénom': result.studentName || '-',
        'Date de naissance': result.birthDate ? new Date(result.birthDate).toLocaleDateString('fr-FR') : '-',
        'Niveau': result.level || '-',
        'Résultat Individuel': result.individualResult || '-',
        'Classement Individuel': result.individualRank || '-',
        'Résultat Équipe': result.teamResult || '-',
        'Classement Équipe': result.teamRank || '-',
        'Membres Équipe': result.teamMembers && result.teamMembers.length > 0 ? result.teamMembers.join(', ') : '-'
    }));
    
    // Créer le classeur
    const ws = XLSX.utils.json_to_sheet(data);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Résultats');
    
    // Sauvegarder au format ODS (OpenDocument Spreadsheet - compatible LibreOffice)
    const filename = `resultats_olympiades_${currentEstablishment.replace(/[^a-z0-9]/gi, '_')}_${new Date().toISOString().split('T')[0]}.ods`;
    XLSX.writeFile(wb, filename, { bookType: 'ods' });
}
