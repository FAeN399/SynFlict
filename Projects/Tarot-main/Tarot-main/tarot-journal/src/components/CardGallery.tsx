import { useState, useEffect } from 'react';
import './CardGallery.css';

const CARD_NAMES = [
  '00-The-Fool.png', '01-The-Magician.png', '02-The-High-Priestess.png',
  '03-The-Empress.png', '04-The-Emperor.png', '05-The-Hierophant.png',
  '06-The-Lovers.png', '07-The-Chariot.png', '08-Strength.png',
  '09-The-Hermit.png', '10-Wheel-of-Fortune.png', '11-Justice.png',
  '12-The-Hanged-Man.png', '13-Death.png', '14-Temperance.png',
  '15-The-Devil.png', '16-The-Tower.png', '17-The-Star.png',
  '18-The-Moon.png', '19-The-Sun.png', '20-Judgement.png',
  '21-The-World.png'
];

export default function CardGallery() {
  const [userDataDir, setUserDataDir] = useState<string>('');

  useEffect(() => {
    (window as any).app.getUserDataDir().then(setUserDataDir);
  }, []);

  if (!userDataDir) {
    return <div className="card-gallery">Loading...</div>;
  }

  return (
    <div className="card-gallery">
      {CARD_NAMES.map(name => (
        <img
          key={name}
          src={`file://${userDataDir}/decks/rider-waite/${name}`}
          alt={name.replace('.png', '').replace(/-/g, ' ')}
        />
      ))}
    </div>
  );
}
