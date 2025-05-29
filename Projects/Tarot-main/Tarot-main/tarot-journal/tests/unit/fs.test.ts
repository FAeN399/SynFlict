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

// Setup global window.fs
vi.stubGlobal('window', { fs: mockFs });

describe('FileSystem Utilities', () => {
  let tempDir: string;

  beforeEach(async () => {
    tempDir = path.join(os.tmpdir(), `tarot-journal-test-${Date.now()}`);
    await fs.mkdir(tempDir, { recursive: true });
    vi.resetAllMocks();
    mockFs.read.mockImplementation(async (p: string) => fs.readFile(p, 'utf8'));
    mockFs.write.mockImplementation(async (p: string, data: string, options?: any) => fs.writeFile(p, data, options));
    mockFs.mkdirp.mockImplementation(async (dir: string) => fs.mkdir(dir, { recursive: true }));
  });

  afterEach(async () => {
    await fs.rm(tempDir, { recursive: true, force: true }).catch(() => {});
  });

  it('should create directories recursively with mkdirp', async () => {
    const nestedDir = path.join(tempDir, 'nested', 'dir');
    await window.fs.mkdirp(nestedDir);
    const stats = await fs.stat(nestedDir);
    expect(stats.isDirectory()).toBe(true);
    expect(mockFs.mkdirp).toHaveBeenCalledWith(nestedDir);
  });

  it('should write and read a file', async () => {
    const filePath = path.join(tempDir, 'test.txt');
    const content = 'Hello, Tarot Journal!';
    await window.fs.write(filePath, content);
    expect(mockFs.write).toHaveBeenCalledWith(filePath, content);
    const readContent = await window.fs.read(filePath);
    expect(mockFs.read).toHaveBeenCalledWith(filePath);
    expect(readContent).toBe(content);
  });

  it('should handle Unicode content correctly', async () => {
    const filePath = path.join(tempDir, 'unicode.txt');
    const unicode = '✨🔮 Tarot Journal 🌙✨';
    await window.fs.write(filePath, unicode);
    const output = await window.fs.read(filePath);
    expect(output).toBe(unicode);
  });
});
