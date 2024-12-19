
const { app, BrowserWindow } = require('electron')
const path = require('node:path')

// Définir le dossier utilisateur pour le cache
const userDataPath = path.join(app.getPath('userData'), 'Cache');

const createWindow = () => {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            // Ajouter ces options pour gérer le cache
            partition: 'persist:main',
            enableRemoteModule: true
        }
    })

    // Configurer le chemin du cache
    app.setPath('userData', userDataPath);

    // win.loadFile('./src/renderer/index.html')
    win.loadFile('./src/renderer/html/login.html')
}

app.whenReady().then(() => {
    createWindow()

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow()
    })
})


app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit()
})