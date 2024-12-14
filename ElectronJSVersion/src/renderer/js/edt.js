import { edt } from './API.js';

// Date handling
let currentDate = new Date();

function getWeekDates(date) {
    const first = date.getDate() - date.getDay() + 1;
    const last = first + 6;
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
    
    // Add headers for days
    const days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'];
    days.forEach(day => {
        const dayHeader = document.createElement('div');
        dayHeader.className = 'day-header';
        dayHeader.textContent = day;
        grid.appendChild(dayHeader);
    });

    // Process and display events
    scheduleData.forEach(event => {
        const eventDiv = createEventElement(event);
        grid.appendChild(eventDiv);
    });

    content.appendChild(grid);
}

function createEventElement(event) {
    const div = document.createElement('div');
    div.className = 'event';
    
    // Fonction utilitaire pour extraire le contenu en toute sécurité
    const getElementContent = (label) => {
        const element = event.elements.find(e => e.label === label);
        return element ? element.content : 'Non spécifié';
    };
    
    const timeData = getElementContent("Heure");
    const subject = getElementContent("Matière");
    const group = getElementContent("Groupe");
    const category = getElementContent("Catégorie d'événement");
    
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
    currentDate = new Date();
    displaySchedule();
});

// Initialize
const classes = ['inf1-b'];
const dropdownContent = document.querySelector('.dropdown-content');
classes.forEach(classe => {
    const a = document.createElement('a');
    a.href = '#';
    a.textContent = classe;
    a.onclick = () => {
        document.querySelector('.dropbtn').textContent = classe;
        displaySchedule();
    };
    dropdownContent.appendChild(a);
});

// Set default class and display schedule
document.querySelector('.dropbtn').textContent = classes[0];
displaySchedule();
