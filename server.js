import express from 'express';
import path from 'path';
import cors from 'cors';
import fetch from 'node-fetch';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = 3000;
const API_BASE_URL = 'https://api.saumondeluxe.com';

// Middleware CORS
app.use(cors({
    origin: 'https://api.saumondeluxe.com', // Mise à jour de l'origine CORS
}));

// Servir les fichiers statiques en premier
app.use(express.static(path.join(__dirname, 'public')));

// Proxy endpoint for bulletin
app.get('/api/bulletin/:credentials', async (req, res) => {
    // console.log('API request:', req.params.credentials);
    try {
        const response = await fetch(`${API_BASE_URL}/uvsq/bulletin/${req.params.credentials}`);
        const data = await response.json();
        res.json(data);
    } catch (error) {
        res.status(500).json({ error: 'Proxy error' });
    }
});

// Proxy endpoint for EDT
app.get('/api/edt/:params', async (req, res) => {
    // console.log('API request:', req.params.params);
    try {
        const response = await fetch(`${API_BASE_URL}/uvsq/edt/${req.params.params}`);
        const data = await response.json();
        res.json(data);
    } catch (error) {
        res.status(500).json({ error: 'Proxy error' });
    }
});

// Route 404 en dernier
app.use((req, res) => {
    res.status(404).send("Page non trouvée 👀");
});

// Démarrer le serveur
const server = app.listen(PORT, () => {
    console.log(`Serveur démarré avec succès sur http://localhost:${PORT}`);
}).on('error', (err) => {
    if (err.code === 'EADDRINUSE') {
        console.error(`Le port ${PORT} est déjà utilisé. Fermeture de l'application.`);
        process.exit(1);
    } else {
        console.error('Erreur du serveur:', err);
    }
});

process.on('SIGTERM', () => {
    server.close(() => {
        console.log('Serveur arrêté');
        process.exit(0);
    });
});