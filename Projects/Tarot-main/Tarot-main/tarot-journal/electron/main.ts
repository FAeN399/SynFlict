import { app, BrowserWindow, session, ipcMain, dialog } from 'electron';
import * as path from 'path';
import * as fs from 'fs/promises';
import cron from 'node-cron';
import { BackupService } from './BackupService';

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
app.whenReady().then(async () => {
  // On first run, copy Rider–Waite deck to user data dir if not present
  const userDataDir = path.join(app.getPath('documents'), 'TarotJournal');
  const userDeckDir = path.join(userDataDir, 'decks', 'rider-waite');
  const bundledDeckDir = path.join(__dirname, '../resources/decks/rider-waite');

  try {
    // Check if deck already exists in user data dir
    await fs.access(userDeckDir);
    // If no error, deck exists, do nothing
  } catch {
    // If error, deck does not exist, copy it
    await fs.mkdir(userDeckDir, { recursive: true });
    const files = await fs.readdir(bundledDeckDir);
    for (const file of files) {
      if (file.endsWith('.png')) {
        const src = path.join(bundledDeckDir, file);
        const dest = path.join(userDeckDir, file);
        await fs.copyFile(src, dest);
      }
    }
  }

  // Ensure readings directory and initial index.json
  const readingsDir = path.join(userDataDir, 'readings');
  try {
    await fs.mkdir(readingsDir, { recursive: true });
  } catch {}
  const indexJsonPath = path.join(readingsDir, 'index.json');
  try {
    await fs.access(indexJsonPath);
  } catch {
    await fs.writeFile(indexJsonPath, '[]', 'utf8');
  }

  // Schedule daily backup at 2:00 AM
  cron.schedule('0 2 * * *', () => {
    BackupService.backupNow(userDataDir).catch(console.error);
  });

  // IPC handlers for backup and restore
  ipcMain.handle('backup:now', async () => {
    await BackupService.backupNow(userDataDir);
  });
  ipcMain.handle('backup:getIndexHash', async (_, dir) => {
    return BackupService.getIndexHash(dir || userDataDir);
  });
  ipcMain.handle('backup:getZipIndexHash', async (_, zipPath) => {
    return BackupService.getZipIndexHash(zipPath);
  });
  ipcMain.handle('backup:restore', async (_, zipPath, mode) => {
    await BackupService.restore(zipPath, mode, userDataDir);
  });
  ipcMain.handle('app:getUserDataDir', () => userDataDir);
  // Expose application base path to renderer for resource access
  ipcMain.handle('app:getAppPath', () => app.getAppPath());

  createWindow();

  app.on('activate', () => {
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
