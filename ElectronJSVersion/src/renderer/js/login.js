import { connection } from './API.js';

(async () => {
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
                console.log(result);
            }
        } catch (error) {
            console.error(error);
        }
    });
})();