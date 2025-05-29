import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import * as path from 'path';
import * as os from 'os';
import * as fs from 'fs/promises';

// Mock the electron bridge
const mockFs = {
  read: vi.fn(),
  write: vi.fn(),
  mkdirp: vi.fn(),
};

const mockDialog = {
  selectFolder: vi.fn(),
};

// Setup the global window object with our mocks
vi.stubGlobal('window', {
  fs: mockFs,
  dialog: mockDialog,
});

describe('FileSystem Utilities', () => {
  let tempDir: string;
  
  beforeEach(async () => {
    // Create a unique temp directory for each test
    tempDir = path.join(os.tmpdir(), `tarot-journal-test-${Date.now()}`);
    await fs.mkdir(tempDir, { recursive: true });
    
    // Reset all mocks before each test
    vi.resetAllMocks();
    
    // Setup the mocks to use the real filesystem for testing
    mockFs.read.mockImplementation(async (p: string) => {
      return fs.readFile(p, 'utf8');
    });
    
    mockFs.write.mockImplementation(async (p: string, data: string) => {
      await fs.writeFile(p, data);
      return true;
    });
    
    mockFs.mkdirp.mockImplementation(async (dir: string) => {
      await fs.mkdir(dir, { recursive: true });
      return true;
    });
  });
  
  afterEach(async () => {
    // Clean up our temp directory after each test
    try {
      await fs.rm(tempDir, { recursive: true, force: true });
    } catch (error) {
      console.error('Error cleaning up test directory:', error);
    }
  });
  
  it('should create directories recursively with mkdirp', async () => {
    const nestedDir = path.join(tempDir, 'nested', 'directory', 'structure');
    
    await window.fs.mkdirp(nestedDir);
    
    // Check if directory was created
    const stats = await fs.stat(nestedDir);
    expect(stats.isDirectory()).toBe(true);
    expect(mockFs.mkdirp).toHaveBeenCalledWith(nestedDir);
  });
  
  it('should write and read a file', async () => {
    const filePath = path.join(tempDir, 'test-file.txt');
    const testContent = 'Hello, Tarot Journal!';
    
    // Write the file
    await window.fs.write(filePath, testContent);
    expect(mockFs.write).toHaveBeenCalledWith(filePath, testContent, undefined);
    
    // Read the file back
    const content = await window.fs.read(filePath);
    expect(mockFs.read).toHaveBeenCalledWith(filePath);
    expect(content).toBe(testContent);
  });
  
  it('should handle Unicode content correctly', async () => {
    const filePath = path.join(tempDir, 'unicode-test.txt');
    const testContent = '✨🔮 Tarot Journal 🌙✨';
    
    await window.fs.write(filePath, testContent);
    const content = await window.fs.read(filePath);
    
    expect(content).toBe(testContent);
  });
});
