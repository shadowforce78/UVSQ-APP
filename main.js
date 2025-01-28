import { app, BrowserWindow } from 'electron';
import { exec } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import { spawn } from 'child_process';
import http from 'http';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

let mainWindow;
let serverProcess;

// Fonction pour tuer le processus sur le port 3000
async function killProcess() {
    return new Promise((resolve, reject) => {
        if (process.platform === 'win32') {
            exec('netstat -ano | findstr :3000', (error, stdout) => {
                if (!error && stdout) {
                    const pid = stdout.split('\r\n')[0].split(/\s+/)[5];
                    exec(`taskkill /F /PID ${pid}`, (err) => {
                        if (err) {
                            console.warn('Aucun processus à tuer');
                        }
                        resolve();
                    });
                } else {
                    resolve();
                }
            });
        } else {
            resolve();
        }
    });
}

// Fonction pour vérifier si le serveur est prêt
function isServerReady() {
    return new Promise((resolve) => {
        const checkServer = () => {
            http.get('http://localhost:3000', (res) => {
                if (res.statusCode === 200) {
                    resolve(true);
                } else {
                    setTimeout(checkServer, 1000);
                }
            }).on('error', () => {
                setTimeout(checkServer, 1000);
            });
        };
        checkServer();
    });
}

async function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: true
        },
        show: false // Ne pas montrer la fenêtre tout de suite
    });

    // Attendre que le serveur soit vraiment prêt
    await isServerReady();
    
    mainWindow.loadURL('http://localhost:3000');
    mainWindow.show(); // Montrer la fenêtre une fois chargée
    
    mainWindow.webContents.on('did-fail-load', () => {
        console.log('Échec du chargement de la page, nouvelle tentative...');
        mainWindow.loadURL('http://localhost:3000');
    });
}

app.on('ready', async () => {
    try {
        // Tuer tout processus existant sur le port 3000
        await killProcess();

        const serverPath = path.join(__dirname, 'server.js');
        serverProcess = spawn('node', [serverPath], {
            stdio: ['inherit', 'inherit', 'inherit']
        });

        serverProcess.on('error', (err) => {
            console.error('Erreur de démarrage du serveur:', err);
            app.quit();
        });

        // Créer la fenêtre après avoir démarré le serveur
        await createWindow();
    } catch (error) {
        console.error('Erreur lors du démarrage:', error);
        app.quit();
    }
});

app.on('window-all-closed', () => {
    if (serverProcess) {
        serverProcess.kill();
    }
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (mainWindow === null) {
        createWindow();
    }
});
