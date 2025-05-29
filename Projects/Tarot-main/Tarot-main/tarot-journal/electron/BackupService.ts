import * as path from 'path';
import * as fs from 'fs/promises';
import * as os from 'os';
import AdmZip from 'adm-zip';
import * as crypto from 'crypto';

export class BackupService {
  static async zipDir(srcDir: string, outPath: string): Promise<void> {
    const zip = new AdmZip();
    zip.addLocalFolder(srcDir);
    await fs.mkdir(path.dirname(outPath), { recursive: true });
    zip.writeZip(outPath);
  }

  static async unzip(zipPath: string, destDir: string): Promise<void> {
    const zip = new AdmZip(zipPath);
    await fs.mkdir(destDir, { recursive: true });
    zip.extractAllTo(destDir, true);
  }

  static async getIndexHash(dir: string): Promise<string> {
    const indexPath = path.join(dir, 'readings', 'index.json');
    const data = await fs.readFile(indexPath);
    return crypto.createHash('sha256').update(data).digest('hex');
  }

  static async getZipIndexHash(zipPath: string): Promise<string> {
    const zip = new AdmZip(zipPath);
    const entry = zip.getEntry('readings/index.json');
    if (!entry) throw new Error('index.json not found in backup');
    const data = entry.getData();
    return crypto.createHash('sha256').update(data).digest('hex');
  }

  static async backupNow(userDataDir: string): Promise<void> {
    const timestamp = new Date().toISOString().split('T')[0];
    const backupsDir = path.join(userDataDir, 'backups');
    const outPath = path.join(backupsDir, `${timestamp}.zip`);
    await this.zipDir(userDataDir, outPath);
    // Rotate backups: keep latest 3
    const files = await fs.readdir(backupsDir);
    const zips = files.filter(f => f.endsWith('.zip')).sort();
    if (zips.length > 3) {
      const remove = zips.slice(0, zips.length - 3);
      for (const f of remove) {
        await fs.unlink(path.join(backupsDir, f));
      }
    }
  }

  static async restore(zipPath: string, mode: 'merge' | 'replace', userDataDir: string): Promise<void> {
    const tmpDir = await fs.mkdtemp(path.join(os.tmpdir(), 'tarot-restore-'));
    await this.unzip(zipPath, tmpDir);
    const srcReadings = path.join(tmpDir, 'readings');
    const destReadings = path.join(userDataDir, 'readings');
    if (mode === 'replace') {
      await fs.rm(destReadings, { recursive: true, force: true });
      await fs.rename(srcReadings, destReadings);
    } else {
      // merge: copy new folders and merge index.json
      const existingIndexPath = path.join(destReadings, 'index.json');
      const backupIndexPath = path.join(srcReadings, 'index.json');
      const existing = JSON.parse(await fs.readFile(existingIndexPath, 'utf8'));
      const backup = JSON.parse(await fs.readFile(backupIndexPath, 'utf8'));
      const merged = [...existing];
      for (const item of backup) {
        if (!existing.find((e: any) => e.id === item.id)) {
          merged.push(item);
        }
      }
      await fs.writeFile(existingIndexPath, JSON.stringify(merged, null, 2));
      const entries = await fs.readdir(srcReadings);
      for (const entry of entries) {
        const src = path.join(srcReadings, entry);
        const dest = path.join(destReadings, entry);
        await fs.cp(src, dest, { recursive: true });
      }
    }
  }
}
