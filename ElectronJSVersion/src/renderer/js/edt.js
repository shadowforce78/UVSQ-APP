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
    
    // Add time header (empty cell for the corner)
    const timeHeader = document.createElement('div');
    timeHeader.className = 'time-header';
    grid.appendChild(timeHeader);
    
    // Add headers for days
    const days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'];
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
        for (let i = 0; i < 6; i++) {
            const emptyCell = document.createElement('div');
            emptyCell.className = 'time-cell';
            grid.appendChild(emptyCell);
        }
    }

    // Process and display events
    scheduleData.forEach(event => {
        const eventDiv = createEventElement(event);
        grid.appendChild(eventDiv);
    });

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
    const startPixels = (timeInfo.startTime - 8) * 60; // 60px par heure
    const duration = (timeInfo.endTime - timeInfo.startTime) * 60;
    const dayOffset = timeInfo.day + 1;

    return {
        gridColumn: dayOffset + 1,
        gridRowStart: Math.floor(startPixels / 60) + 2,
        gridRowEnd: Math.floor((startPixels + duration) / 60) + 2
    };
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
    
    const timeInfo = parseEventTime(timeData);
    const position = calculateEventPosition(timeInfo);
    
    div.style.gridColumn = position.gridColumn;
    div.style.gridRow = `${position.gridRowStart} / ${position.gridRowEnd}`;
    
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
