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

    function showDetails(type, code) {
        const details = type === 'ressource' ? ressources[code] : saes[code];
        if (!details) return;

        // Création d'un tableau des évaluations disponibles
        const evaluations = details.evaluations.map(evaluation => ({
            id: evaluation.id,
            coef: evaluation.coef,
            date_debut: new Date(evaluation.date_debut).toLocaleDateString(),
            note: evaluation.note || 'Non notée'
        }));
        
        modalContent.innerHTML = `
            <h2>${code} - ${details.titre || 'Sans titre'}</h2>
            <div class="detail-grid">
                ${evaluations.length > 0 ? 
                    evaluations.map(evaluation => `
                        <div class="detail-item">
                            <strong>Évaluation ${evaluation.id}:</strong> ${evaluation.note}<br>
                            <strong>Coefficient:</strong> ${evaluation.coef}<br>
                            <strong>Date:</strong> ${evaluation.date_debut}
                        </div>
                    `).join('')
                    : '<div class="detail-item">Aucune note disponible</div>'
                }
            </div>
        `;
        modal.style.display = 'block';
    }

    closeBtn.onclick = () => modal.style.display = 'none';
    window.onclick = (e) => {
        if (e.target === modal) modal.style.display = 'none';
    }

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
});