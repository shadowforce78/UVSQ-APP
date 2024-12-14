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

    replaceText('prenom', getName(storedData));
})