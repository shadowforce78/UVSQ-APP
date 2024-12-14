window.addEventListener('DOMContentLoaded', () => {
    const replaceText = (selector, text) => {
        const elements = document.getElementsByClassName(selector)
        if (elements.length > 0) elements[0].innerText = text
    }

    const storedData = localStorage.getItem('userData');

    function getName(data) {
        data = JSON.parse(data);
        let prenom = data['auth'].name;
        return prenom || 'Nom Introuvable';
    }

    function getEdt() {
        window.location.href = 'edt.html';
    }
    document.getElementById('edt').addEventListener('click', getEdt);

    replaceText('prenom', getName(storedData));

    // Gestionnaire de déconnexion
    document.getElementById('logout').addEventListener('click', () => {
        localStorage.removeItem('userData');
        localStorage.removeItem('userId');
        localStorage.removeItem('userPassword');
        window.location.href = 'login.html';
    });
})