// filepath: src/store/searchStore.ts
import { create } from 'zustand';
import Fuse from 'fuse.js';

export interface IndexItem {
  id: string;
  title: string;
  tags: string[];
  cards: string[];
}

interface SearchState {
  items: IndexItem[];
  query: string;
  setItems: (items: IndexItem[]) => void;
  setQuery: (query: string) => void;
  getResults: () => IndexItem[];
}

export const useSearchStore = create<SearchState>((set, get) => {
  const fuse = new Fuse<IndexItem>([], {
    keys: ['title', 'tags', 'cards'],
    threshold: 0.3,
  });

  return {
    items: [],
    query: '',
    setItems: (items) => {
      fuse.setCollection(items);
      set({ items });
    },
    setQuery: (query) => set({ query }),
    getResults: () => {
      const { items, query } = get();
      if (!query) return items;
      return fuse.search(query).map(result => result.item);
    },
  };
});

export default useSearchStore;
