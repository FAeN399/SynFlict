import { useState, useEffect } from 'react';
import './App.css';
import Wizard from './Wizard';
import CardGallery from './components/CardGallery';
import useSearchStore, { IndexItem } from './store/searchStore';
import TagManager from './components/TagManager';

function App() {
  const [count, setCount] = useState(0);
  const setItems = useSearchStore(state => state.setItems);
  const setQuery = useSearchStore(state => state.setQuery);
  const results = useSearchStore(state => state.getResults());

  useEffect(() => {
    if (window.fs && (window as any).app) {
      (window as any).app.getUserDataDir()
        .then((dir: string) => window.fs.read(`${dir}/readings/index.json`))
        .then((data: string) => setItems(JSON.parse(data)))
        .catch((err: any) => console.warn('Failed to load index.json', err));
    }
  }, [setItems]);

  return (
    <>
      {/* Search bar */}
      <div className="search-bar">
        <input
          type="text"
          placeholder="Search readings..."
          onChange={e => setQuery(e.target.value)}
        />
      </div>
      {/* Tag management */}
      <TagManager />
      {/* Search results */}
      <ul className="search-results">
        {results.map((item: IndexItem) => (
          <li key={item.id}>
            {item.title} - {item.tags.join(', ')}
          </li>
        ))}
      </ul>
      <div className="app-container">
        <h1>Hello Offline</h1>
        <p className="subtitle">Welcome to Tarot Journal</p>
        
        <div className="card">
          <p>
            This application works completely offline.
            All your data is stored locally on your device.
          </p>
          <button onClick={() => setCount(count => count + 1)}>
            Count is {count}
          </button>
          <div className="version-info">
            <p>Using:</p>
            <ul>
              <li>Chrome <span id="chrome-version"></span></li>
              <li>Node <span id="node-version"></span></li>
              <li>Electron <span id="electron-version"></span></li>
            </ul>
          </div>
        </div>
        {window.fs && <Wizard />}
        <CardGallery />
      </div>
    </>
  );
}

export default App;
