import { useState } from 'react';
import './App.css';

function App() {
  const [count, setCount] = useState(0);

  return (
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
    </div>
  );
}

export default App;
