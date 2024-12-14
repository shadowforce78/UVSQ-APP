import { edt } from './API.js';

// Date handling
function adjustForWeekend(date) {
    const day = date.getDay();
    if (day === 0) { // Dimanche
        date.setDate(date.getDate() + 1); // Aller au lundi suivant
    } else if (day === 6) { // Samedi
        date.setDate(date.getDate() + 2); // Aller au lundi suivant
    }
    return date;
}

let currentDate = adjustForWeekend(new Date());

function getWeekDates(date) {
    const first = date.getDate() - date.getDay() + 1;
    const last = first + 4;
    const firstDay = new Date(date.setDate(first));
    const lastDay = new Date(date.setDate(last));
    return {
        start: formatDate(firstDay),
        end: formatDate(lastDay)
    };
}

function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// Schedule display
async function displaySchedule() {
    const weekDates = getWeekDates(currentDate);
    const classe = document.querySelector('.dropbtn').textContent;
    const scheduleData = await edt(classe, weekDates.start, weekDates.end);

    const content = document.querySelector('.content');
    content.innerHTML = '';

    // Create weekly grid
    const grid = document.createElement('div');
    grid.className = 'schedule-grid';

    // Add time header (empty cell for the corner)
    const timeHeader = document.createElement('div');
    timeHeader.className = 'time-header';
    grid.appendChild(timeHeader);

    // Add headers for days
    const days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi'];
    days.forEach(day => {
        const dayHeader = document.createElement('div');
        dayHeader.className = 'day-header';
        dayHeader.textContent = day;
        grid.appendChild(dayHeader);
    });

    // Add time slots - only full hours
    for (let hour = 8; hour <= 18; hour++) {
        const timeSlot = document.createElement('div');
        timeSlot.className = 'time-slot';
        timeSlot.textContent = `${String(hour).padStart(2, '0')}:00`;
        grid.appendChild(timeSlot);

        // Add empty cells for each day
        for (let i = 0; i < 5; i++) {
            const dayCell = document.createElement('div');
            dayCell.className = 'time-cell';
            grid.appendChild(dayCell);
        }
    }

    // Process and display events in a container
    const eventsContainer = document.createElement('div');
    eventsContainer.className = 'events-container';
    scheduleData.forEach(event => {
        const eventDiv = createEventElement(event);
        eventsContainer.appendChild(eventDiv);
    });

    grid.appendChild(eventsContainer);
    content.appendChild(grid);
}

function parseEventTime(timeString) {
    // Format: "16/12/2024 13:00-17:00"
    const [date, time] = timeString.split(' ');
    const [start, end] = time.split('-');
    const [startHour, startMinute] = start.split(':').map(Number);
    const [endHour, endMinute] = end.split(':').map(Number);
    const day = new Date(date.split('/').reverse().join('-')).getDay();

    return {
        day: day === 0 ? 6 : day - 1, // Convertir dimanche(0) en 6 et décaler les autres jours
        startTime: startHour + startMinute / 60,
        endTime: endHour + endMinute / 60
    };
}

function calculateEventPosition(timeInfo) {
    const hourHeight = 60; // hauteur d'une heure en pixels
    const startHour = timeInfo.startTime - 8; // commence à 8h
    const duration = timeInfo.endTime - timeInfo.startTime;

    const top = startHour * hourHeight;
    const height = duration * hourHeight - 2; // -2px pour l'espacement vertical
    const left = (timeInfo.day) * (100 / 5) + 0.5; // +0.5% pour la marge gauche
    const width = (100 / 5) - 1; // -1% pour éviter le chevauchement

    return { top, height, left, width };
}

function createEventElement(event) {
    const div = document.createElement('div');
    div.className = 'event';

    const getElementContent = (label) => {
        if (!event || !event.elements) {
            console.warn('Event or elements is undefined');
            return 'Non spécifié';
        }

        // Normalisation pour la recherche insensible aux accents
        const normalizedLabel = label.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
        const element = event.elements.find(e => {
            if (!e || !e.label) return false;
            return e.label.normalize('NFD').replace(/[\u0300-\u036f]/g, '') === normalizedLabel;
        });

        return element ? element.content : 'Non spécifié';
    };

    const timeData = getElementContent("Heure");
    const subject = getElementContent("Matiere");
    const group = getElementContent("Groupe");
    let category = getElementContent('Catégorie d’événement')


    category = category.trim();
    const categoryLower = category.toLowerCase();

    console.log('Catégorie après trim:', category);
    console.log('Catégorie en minuscules:', categoryLower);
    console.log('Contient TD:', categoryLower.includes('td'));
    console.log('Contient CM:', categoryLower.includes('cm'));
    console.log('Contient TP:', categoryLower.includes('tp'));

    // Ajouter la classe CSS selon le type de cours
    let appliedClass = 'other';
    if (categoryLower.includes('td')) {
        div.classList.add('td');
        appliedClass = 'td';
    } else if (categoryLower.includes('cm')) {
        div.classList.add('cm');
        appliedClass = 'cm';
    } else if (categoryLower.includes('tp')) {
        div.classList.add('tp');
        appliedClass = 'tp';
    } else {
        div.classList.add('other');
    }

    console.log('Classe appliquée:', appliedClass);
    console.log('Classes finales:', div.className);
    console.groupEnd();

    const timeInfo = parseEventTime(timeData);
    const position = calculateEventPosition(timeInfo);

    div.style.top = `${position.top}px`;
    div.style.height = `${position.height}px`;
    div.style.left = `${position.left}%`;
    div.style.width = `${position.width}%`;

    div.innerHTML = `
        <div class="event-time">${timeData}</div>
        <div class="event-subject">${subject}</div>
        <div class="event-details">${group} - ${category}</div>
    `;

    return div;
}

// Event listeners
document.getElementById('prev').addEventListener('click', () => {
    currentDate.setDate(currentDate.getDate() - 7);
    displaySchedule();
});

document.getElementById('next').addEventListener('click', () => {
    currentDate.setDate(currentDate.getDate() + 7);
    displaySchedule();
});

document.getElementById('today').addEventListener('click', () => {
    currentDate = adjustForWeekend(new Date());
    displaySchedule();
});

// Initialize
const classes = ['inf1-b', 'mmi1-a2'];
const dropdownContent = document.querySelector('.dropdown-content');
const dropdownButton = document.querySelector('.dropbtn');
const dropdown = document.querySelector('.dropdown');

// Gestion du clic sur le bouton dropdown
dropdownButton.addEventListener('click', (e) => {
    e.stopPropagation();
    dropdown.classList.toggle('open');
});

// Fermer le dropdown si on clique ailleurs
document.addEventListener('click', () => {
    dropdown.classList.remove('open');
});

classes.forEach(classe => {
    const a = document.createElement('a');
    a.href = '#';
    a.textContent = classe;
    a.onclick = (e) => {
        e.preventDefault();
        dropdownButton.textContent = classe;
        dropdown.classList.remove('open');
        displaySchedule();
    };
    dropdownContent.appendChild(a);
});

// Set default class and display schedule
document.querySelector('.dropbtn').textContent = classes[0];
displaySchedule();
