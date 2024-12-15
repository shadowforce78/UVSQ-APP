window.addEventListener('DOMContentLoaded', () => {

    const userData = localStorage.getItem('userData');
    const releve = JSON.parse(userData);
    const ues = releve["relevé"]["ues"]
    const ressources = releve["relevé"]["ressources"]
    const saes = releve["relevé"]["saes"]

    // Gestion du thème
    function setTheme(isDark) {
        document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    }

    // Initialisation du thème
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme === 'dark');
    document.getElementById('themeToggle').checked = savedTheme === 'dark';

    // Event listener pour le toggle
    document.getElementById('themeToggle').addEventListener('change', (e) => {
        setTheme(e.target.checked);
    });

    const modal = document.getElementById('detailModal');
    const modalContent = document.getElementById('modalContent');
    const closeBtn = document.getElementsByClassName('close')[0];

    const evaluationModal = document.getElementById('evaluationModal');
    const evaluationModalContent = document.getElementById('evaluationModalContent');
    const evaluationCloseBtn = document.getElementsByClassName('evaluation-close')[0];

    function showEvaluationDetails(evaluation) {
        const noteStats = evaluation.note || { value: 'Non notée', min: 'N/A', max: 'N/A', moy: 'N/A' };
        
        evaluationModalContent.innerHTML = `
            <h2>Détails de l'évaluation</h2>
            <div class="evaluation-details">
                <p><strong>ID:</strong> ${evaluation.id}</p>
                <p><strong>Coefficient:</strong> ${evaluation.coef}</p>
                <p><strong>Date:</strong> ${new Date(evaluation.date_debut).toLocaleDateString()}</p>
                <div class="note-stats">
                    <p><strong>Note:</strong> ${noteStats.value}</p>
                    <p><strong>Minimum:</strong> ${noteStats.min}</p>
                    <p><strong>Maximum:</strong> ${noteStats.max}</p>
                    <p><strong>Moyenne:</strong> ${noteStats.moy}</p>
                </div>
                ${evaluation.remarque ? `<p><strong>Remarque:</strong> ${evaluation.remarque}</p>` : ''}
                ${evaluation.description ? `<p><strong>Description:</strong> ${evaluation.description}</p>` : ''}
            </div>
        `;
        evaluationModal.style.display = 'block';
    }

    function showDetails(type, code) {
        const details = type === 'ressource' ? ressources[code] : saes[code];
        if (!details) return;

        let evaluationsHTML = '';
        
        if (details.evaluations && details.evaluations.length > 0) {
            evaluationsHTML = details.evaluations.map((evaluation, index) => `
                <div class="detail-item evaluation-clickable" data-evaluation-index="${index}">
                    <h3>Évaluation ${index + 1}</h3>
                    <p><strong>ID:</strong> ${evaluation.id}</p>
                    <p><strong>Note:</strong> ${evaluation.note?.value || 'Non notée'}</p>
                    ${evaluation.description ? `<p><strong>Description:</strong> ${evaluation.description}</p>` : ''}
                </div>
            `).join('');
        } else {
            evaluationsHTML = '<div class="detail-item">Aucune évaluation disponible</div>';
        }
        
        modalContent.innerHTML = `
            <h2>${code} - ${details.titre || 'Sans titre'}</h2>
            <p><strong>Code Apogée:</strong> ${details.code_apogee || 'Non spécifié'}</p>
            <div class="detail-grid">
                ${evaluationsHTML}
            </div>
        `;
        modal.style.display = 'block';

        // Ajouter les écouteurs d'événements pour les évaluations
        document.querySelectorAll('.evaluation-clickable').forEach(item => {
            item.addEventListener('click', () => {
                const index = item.dataset.evaluationIndex;
                showEvaluationDetails(details.evaluations[index]);
            });
        });
    }

    closeBtn.onclick = () => modal.style.display = 'none';
    window.onclick = (e) => {
        if (e.target === modal) modal.style.display = 'none';
        if (e.target === evaluationModal) evaluationModal.style.display = 'none';
    }

    evaluationCloseBtn.onclick = () => evaluationModal.style.display = 'none';
    window.onclick = (e) => {
        if (e.target === modal) modal.style.display = 'none';
        if (e.target === evaluationModal) evaluationModal.style.display = 'none';
    };

    function displayGrades() {
        const container = document.getElementById('grades-container');
        
        Object.entries(ues).forEach(([ueKey, ueData]) => {
            const ueElement = document.createElement('div');
            ueElement.className = 'ue-card';
            
            ueElement.innerHTML = `
                <div class="ue-header">
                    <span class="ue-title">${ueData.titre}</span>
                    <span class="ue-average">Moyenne: ${ueData.moyenne.value}</span>
                </div>
                <div class="resources-container">
                    <h3>Ressources</h3>
                    ${Object.entries(ueData.ressources).map(([key, resource]) => `
                        <div class="grade-item" data-type="ressource" data-code="${key}">
                            <span>${key}</span>
                            <span>${resource.moyenne !== '~' ? resource.moyenne : 'Non notée'}</span>
                        </div>
                    `).join('')}
                </div>
                ${ueData.saes ? `
                    <div class="saes-container">
                        <h3>SAÉs</h3>
                        ${Object.entries(ueData.saes).map(([key, sae]) => `
                            <div class="grade-item" data-type="sae" data-code="${key}">
                                <span>${key}</span>
                                <span>${sae.moyenne !== '~' ? sae.moyenne : 'Non notée'}</span>
                            </div>
                        `).join('')}
                    </div>
                ` : ''}
            `;
            container.appendChild(ueElement);
        });

        // Ajouter les écouteurs d'événements après avoir créé les éléments
        document.querySelectorAll('.grade-item').forEach(item => {
            item.addEventListener('click', () => {
                const type = item.dataset.type;
                const code = item.dataset.code;
                showDetails(type, code);
            });
        });
    }

    displayGrades();

    // Ajout de la navigation
    document.getElementById('backButton').addEventListener('click', () => {
        window.location.href = 'home.html';
    });
});