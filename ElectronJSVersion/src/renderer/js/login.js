
document.getElementById('loginForm').addEventListener('submit', (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // TODO: Ajouter la validation et l'authentification ici
    // Pour l'instant, on simule une connexion simple
    if (username && password) {
        // Envoyer les informations au processus principal via IPC
        window.electron.login({ username, password });
    }
});