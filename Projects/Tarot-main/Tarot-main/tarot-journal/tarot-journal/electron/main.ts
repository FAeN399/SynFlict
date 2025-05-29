import { app, BrowserWindow, session, ipcMain, dialog } from 'electron';
import * as path from 'path';
import * as fs from 'fs/promises';

// Handle creating/removing shortcuts on Windows when installing/uninstalling
if (require('electron-squirrel-startup')) {
  app.quit();
}

const createWindow = (): void => {
  // Create the browser window with secure defaults
  const mainWindow = new BrowserWindow({
    width: 900,
    height: 670,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      sandbox: true,
      nodeIntegration: false,
    },
  });

  // Block all network requests
  session.defaultSession.webRequest.onBeforeRequest((details, callback) => {
    const { url } = details;
    const isLocalResource =
      url.startsWith('file://') ||
      url.startsWith('devtools://') ||
      url.includes('localhost') ||
      url.includes('127.0.0.1');

    callback({ cancel: !isLocalResource });
  });

  // Load the app
  if (app.isPackaged) {
    mainWindow.loadFile(path.join(__dirname, '../renderer/index.html'));
  } else {
    // In development, load from the dev server
    mainWindow.loadURL('http://localhost:5173');
    // Open the DevTools in development
    mainWindow.webContents.openDevTools();
  }
};

// File system operations
ipcMain.handle('fs:read', async (_, filePath) => {
  try {
    return await fs.readFile(filePath, 'utf8');
  } catch (error) {
    console.error('Error reading file:', error);
    throw error;
  }
});

ipcMain.handle('fs:write', async (_, filePath, data, options = {}) => {
  try {
    await fs.writeFile(filePath, data, options);
    return true;
  } catch (error) {
    console.error('Error writing file:', error);
    throw error;
  }
});

ipcMain.handle('fs:mkdirp', async (_, dir) => {
  try {
    await fs.mkdir(dir, { recursive: true });
    return true;
  } catch (error) {
    console.error('Error creating directory:', error);
    throw error;
  }
});

ipcMain.handle('dialog:selectFolder', async () => {
  const result = await dialog.showOpenDialog({
    properties: ['openDirectory', 'createDirectory'],
  });
  
  if (result.canceled) {
    return null;
  }
  
  return result.filePaths[0];
});

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    // On macOS it's common to re-create a window when the 
    // dock icon is clicked and there are no other windows open
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

// Quit when all windows are closed, except on macOS.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
