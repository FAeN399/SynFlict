interface Window {
  fs: {
    read: (path: string) => Promise<string>;
    write: (
      path: string,
      data: string | Buffer | Uint8Array,
      options?: any
    ) => Promise<boolean>;
    mkdirp: (dir: string) => Promise<boolean>;
  };
  
  dialog: {
    selectFolder: () => Promise<string | null>;
  };
}
