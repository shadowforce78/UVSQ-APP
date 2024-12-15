window.addEventListener('DOMContentLoaded', () => {
    const userData = localStorage.getItem('userData');
    const data = JSON.parse(userData);
    const absences = data['absences'];
    const mainDiv = document.querySelector('.main');

    // Ensure absences is not null/undefined
    if (!absences) {
        const noData = document.createElement('p');
        noData.textContent = 'Aucune absence trouvée';
        mainDiv.appendChild(noData);
        return;
    }

    // Convert object entries to array and sort by date
    const sortedDates = Object.entries(absences).sort(([dateA], [dateB]) => {
        return new Date(dateB) - new Date(dateA);
    });

    sortedDates.forEach(([date, absencesList]) => {
        const dateHeader = document.createElement('h2');
        dateHeader.textContent = `Date: ${date}`;
        mainDiv.appendChild(dateHeader);

        // Check if absencesList is an array before using forEach
        if (Array.isArray(absencesList)) {
            absencesList.forEach((absence) => {
                const absenceDiv = document.createElement('div');
                absenceDiv.classList.add('absence');

                const matiere = document.createElement('p');
                matiere.textContent = `Matière: ${absence.matiereComplet}`;
                absenceDiv.appendChild(matiere);

                const enseignant = document.createElement('p');
                enseignant.textContent = `Enseignant: ${absence.enseignant}`;
                absenceDiv.appendChild(enseignant);

                const time = document.createElement('p');
                time.textContent = `Heure: ${absence.debut} - ${absence.fin}`;
                absenceDiv.appendChild(time);

                const statut = document.createElement('p');
                statut.textContent = `Statut: ${absence.statut}`;
                absenceDiv.appendChild(statut);

                mainDiv.appendChild(absenceDiv);
            });
        }
    });
});