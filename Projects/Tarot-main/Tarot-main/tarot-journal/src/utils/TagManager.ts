// filepath: src/utils/TagManager.ts

export default class TagManager {
  private index: Record<string, string[]>;

  constructor() {
    this.index = {};
  }

  addTags(id: string, tags: string[]) {
    this.index[id] = tags;
  }

  searchByTag(tag: string): string[] {
    return Object.entries(this.index)
      .filter(([, tags]) => tags.includes(tag))
      .map(([id]) => id);
  }
}
