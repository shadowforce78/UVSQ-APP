import { connection } from './API.js';

// Fonction pour afficher le mot de passe
function showPassword() {
    const password = document.getElementById('password');
    if (password.type === 'password') {
        password.type = 'text';
    } else {
        password.type = 'password';
    }
}

document.getElementById('showpwd').addEventListener('change', showPassword);

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

(async () => {
    // Vérifier s'il existe des identifiants stockés
    const storedId = localStorage.getItem('userId');
    const storedPassword = localStorage.getItem('userPassword');
    
    if (storedId && storedPassword) {
        try {
            const result = await connection(storedId, storedPassword);
            if (!result.error) {
                // Stocker les données de l'utilisateur
                localStorage.setItem('userData', JSON.stringify(result));
                console.log('Connexion automatique réussie');
                window.location.href = '../html/home.html';
                return;
            }
        } catch (error) {
            console.error(error);
        }
    }

    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();

        const id = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const errorMessage = document.getElementById('errorMessage');

        try {
            // Si ID n'est pas un nombre
            if (isNaN(id)) {
                errorMessage.innerText = 'ID doit être un nombre';
                return;
            }
            const result = await connection(id, password);
            if (result.error) {
                errorMessage.innerText = result.error;
            } else {
                // Sauvegarder les identifiants et les données
                localStorage.setItem('userId', id);
                localStorage.setItem('userPassword', password);
                localStorage.setItem('userData', JSON.stringify(result));
                console.log('Connecté');
                window.location.href = '../html/home.html';
            }
        } catch (error) {
            console.error(error);
        }
    })
})();