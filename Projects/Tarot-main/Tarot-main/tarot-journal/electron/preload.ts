import { contextBridge, ipcRenderer } from 'electron';

// Expose file system operations to renderer process
contextBridge.exposeInMainWorld('fs', {
  read: (path: string): Promise<string> => ipcRenderer.invoke('fs:read', path),
  write: (
    path: string,
    data: string | Buffer | Uint8Array,
    options?: any
  ): Promise<boolean> => ipcRenderer.invoke('fs:write', path, data, options),
  mkdirp: (dir: string): Promise<boolean> => ipcRenderer.invoke('fs:mkdirp', dir),
});

contextBridge.exposeInMainWorld('dialog', {
  selectFolder: (): Promise<string | null> => ipcRenderer.invoke('dialog:selectFolder'),
});

contextBridge.exposeInMainWorld('app', {
  getUserDataDir: () => ipcRenderer.invoke('app:getUserDataDir'),
  getAppPath: () => ipcRenderer.invoke('app:getAppPath'),
});

// Preload script with secure context isolation
window.addEventListener('DOMContentLoaded', () => {
  const replaceText = (selector: string, text: string) => {
    const element = document.getElementById(selector);
    if (element) {
      element.innerText = text;
    }
  };

  // Display electron version information for debugging
  for (const dependency of ['chrome', 'node', 'electron']) {
    replaceText(`${dependency}-version`, process.versions[dependency] || 'unknown');
  }
});
