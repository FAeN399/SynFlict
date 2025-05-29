import React, { useState, useEffect } from 'react';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import { Editor } from '@toast-ui/react-editor';
import TemplateGallery from './components/TemplateGallery';

const CARD_FILENAMES = [
  '00-The-Fool.png', '01-The-Magician.png', '02-The-High-Priestess.png', '03-The-Empress.png',
  '04-The-Emperor.png', '05-The-Hierophant.png', '06-The-Lovers.png', '07-The-Chariot.png',
  '08-Strength.png', '09-The-Hermit.png', '10-Wheel-of-Fortune.png', '11-Justice.png',
  '12-The-Hanged-Man.png', '13-Death.png', '14-Temperance.png', '15-The-Devil.png',
  '16-The-Tower.png', '17-The-Star.png', '18-The-Moon.png', '19-The-Sun.png',
  '20-Judgement.png', '21-The-World.png',
  '22-Ace-of-Wands.png', '23-Two-of-Wands.png', '24-Three-of-Wands.png', '25-Four-of-Wands.png',
  '26-Five-of-Wands.png', '27-Six-of-Wands.png', '28-Seven-of-Wands.png', '29-Eight-of-Wands.png',
  '30-Nine-of-Wands.png', '31-Ten-of-Wands.png', '32-Page-of-Wands.png', '33-Knight-of-Wands.png',
  '34-Queen-of-Wands.png', '35-King-of-Wands.png',
  '36-Ace-of-Cups.png', '37-Two-of-Cups.png', '38-Three-of-Cups.png', '39-Four-of-Cups.png',
  '40-Five-of-Cups.png', '41-Six-of-Cups.png', '42-Seven-of-Cups.png', '43-Eight-of-Cups.png',
  '44-Nine-of-Cups.png', '45-Ten-of-Cups.png', '46-Page-of-Cups.png', '47-Knight-of-Cups.png',
  '48-Queen-of-Cups.png', '49-King-of-Cups.png',
  '50-Ace-of-Swords.png', '51-Two-of-Swords.png', '52-Three-of-Swords.png', '53-Four-of-Swords.png',
  '54-Five-of-Swords.png', '55-Six-of-Swords.png', '56-Seven-of-Swords.png', '57-Eight-of-Swords.png',
  '58-Nine-of-Swords.png', '59-Ten-of-Swords.png', '60-Page-of-Swords.png', '61-Knight-of-Swords.png',
  '62-Queen-of-Swords.png', '63-King-of-Swords.png',
  '64-Ace-of-Pentacles.png', '65-Two-of-Pentacles.png', '66-Three-of-Pentacles.png', '67-Four-of-Pentacles.png',
  '68-Five-of-Pentacles.png', '69-Six-of-Pentacles.png', '70-Seven-of-Pentacles.png', '71-Eight-of-Pentacles.png',
  '72-Nine-of-Pentacles.png', '73-Ten-of-Pentacles.png', '74-Page-of-Pentacles.png', '75-Knight-of-Pentacles.png',
  '76-Queen-of-Pentacles.png', '77-King-of-Pentacles.png',
];

const TEMPLATE_FILES = [
  { name: 'Daily Draw', file: 'daily_draw.json' },
  { name: 'Celtic Cross', file: 'celtic_cross.json' },
];

const getToday = () => {
  const d = new Date();
  return d.toISOString().slice(0, 10);
};

const Wizard: React.FC = () => {
  const [template, setTemplate] = useState(TEMPLATE_FILES[0].file);
  const [title, setTitle] = useState('');
  const [tags, setTags] = useState('');
  const [selectedCards, setSelectedCards] = useState<string[]>([]);
  const [notes, setNotes] = useState('');
  const [userDataDir, setUserDataDir] = useState<string>('');
  const [_templateData, _setTemplateData] = useState<any>(null);

  // Fetch base path for user data directory
  useEffect(() => {
    (window as any).app.getUserDataDir().then(setUserDataDir);
  }, []);

  // Drag and drop handlers
  const onDragEnd = (result: any) => {
    if (!result.destination) return;
    const items = Array.from(selectedCards);
    const [reordered] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reordered);
    setSelectedCards(items);
  };

  // Add card to grid
  const addCard = (card: string) => {
    if (!selectedCards.includes(card)) {
      setSelectedCards([...selectedCards, card]);
    }
  };

  // Remove card from grid
  const removeCard = (idx: number) => {
    setSelectedCards(selectedCards.filter((_, i) => i !== idx));
  };

  // Save reading
  const handleSave = async () => {
    const date = getToday();
    const safeTitle = title.replace(/[^a-zA-Z0-9-_]/g, '_');
    const readingDir = `${userDataDir}/readings/${date}-${safeTitle}`;
    const imagesDir = `${readingDir}/images`;
    await window.fs.mkdirp(imagesDir);
    // Copy card images
    for (const card of selectedCards) {
      const src = `${userDataDir}/decks/rider-waite/${card}`;
      const dest = `${imagesDir}/${card}`;
      await window.fs.write(dest, await window.fs.read(src));
    }
    // Generate HTML
    const html = `<!DOCTYPE html><html><head><meta charset='utf-8'><title>${title}</title><link rel='stylesheet' href='../reading.css'></head><body><h1>${title}</h1><div>${notes}</div></body></html>`;
    await window.fs.write(`${readingDir}/reading.html`, html);
    // Append to index.json
    let index = [];
    try {
      index = JSON.parse(await window.fs.read(`${userDataDir}/readings/index.json`));
    } catch {}
    index.push({
      id: `${date}-${safeTitle}`,
      title,
      date,
      tags: tags.split(',').map(t => t.trim()),
      cards: selectedCards,
      path: readingDir,
    });
    await window.fs.write(`${userDataDir}/readings/index.json`, JSON.stringify(index, null, 2));
    alert('Reading saved!');
  };

  return (
    <div className="wizard">
      <h2>New Reading</h2>
      <div className="wizard-section">
        <h3>Select Template</h3>
        <TemplateGallery selected={template} onSelect={setTemplate} />
      </div>
      <label>Title:
        <input value={title} onChange={e => setTitle(e.target.value)} />
      </label>
      <label>Tags (comma separated):
        <input value={tags} onChange={e => setTags(e.target.value)} />
      </label>
      <div>
        <h3>Card Grid</h3>
        <DragDropContext onDragEnd={onDragEnd}>
          <Droppable droppableId="card-grid" direction="horizontal">
            {(provided: any) => (
              <div ref={provided.innerRef} {...provided.droppableProps} style={{ display: 'flex', gap: 8 }}>
                {selectedCards.map((card, idx) => (
                  <Draggable key={card} draggableId={card} index={idx}>
                    {(prov: any) => (
                      <div ref={prov.innerRef} {...prov.draggableProps} {...prov.dragHandleProps}>
                        <img src={`file://${userDataDir}/decks/rider-waite/${card}`} alt={card} width={60} />
                        <button onClick={() => removeCard(idx)}>Remove</button>
                      </div>
                    )}
                  </Draggable>
                ))}
                {provided.placeholder}
              </div>
            )}
          </Droppable>
        </DragDropContext>
        <div style={{ marginTop: 16 }}>
          <label>Add Card:
            <select onChange={e => addCard(e.target.value)} value="">
              <option value="">--Select--</option>
              {CARD_FILENAMES.map(card => (
                <option key={card} value={card}>{card}</option>
              ))}
            </select>
          </label>
        </div>
      </div>
      <div style={{ marginTop: 16 }}>
        <h3>Notes</h3>
        <Editor
          initialValue={notes}
          previewStyle="vertical"
          height="200px"
          initialEditType="markdown"
          useCommandShortcut={true}
          onChange={() => setNotes((window as any).editorRef.getInstance().getMarkdown())}
          ref={el => (window as any).editorRef = el}
        />
      </div>
      <button onClick={handleSave}>Save Reading</button>
    </div>
  );
};

export default Wizard;
