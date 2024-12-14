import { connection } from './API.js';

(async () => {
    const api = (await import('./API.js')).default;

    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const id = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try {
            // Si ID n'est pas un nombre
            if (isNaN(id)) {
                throw new Error('ID must be a number');
            }
            const result = await connection(id, password);
            console.log(result);
        } catch (error) {
            console.error(error);
        }
    });
})();