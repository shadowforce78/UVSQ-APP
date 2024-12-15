
const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

function createWindow() {
    const mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            contextIsolation: true,
            enableRemoteModule: false,
            nodeIntegration: false
        }
    });

    mainWindow.loadFile('src/renderer/html/login.html');

    // Open the DevTools.
    // mainWindow.webContents.openDevTools();
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

// Ajouter dans la configuration des IPC handlers
ipcMain.on('navigate', (event, page) => {
    const currentWindow = BrowserWindow.getFocusedWindow();
    if (currentWindow) {
        currentWindow.loadFile(`src/renderer/html/${page}.html`);
    }
});