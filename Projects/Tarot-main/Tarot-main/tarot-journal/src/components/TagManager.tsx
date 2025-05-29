import { useState, useEffect } from 'react';
import './TagManager.css';

const TagManager = () => {
  const [userDataDir, setUserDataDir] = useState<string>('');
  const [tags, setTags] = useState<string[]>([]);
  const [newTag, setNewTag] = useState<string>('');
  const tagsFile = `${userDataDir}/tags.json`;

  // Load userDataDir and existing tags
  useEffect(() => {
    (window as any).app.getUserDataDir().then((dir: string) => {
      setUserDataDir(dir);
      // Read tags.json or initialize
      window.fs.read(`${dir}/tags.json`)
        .then(data => setTags(JSON.parse(data)))
        .catch(() => {
          // If file doesn't exist, start with empty and create file
          setTags([]);
          window.fs.write(`${dir}/tags.json`, JSON.stringify([], null, 2));
        });
    });
  }, []);

  // Save tags to file
  const saveTags = (updated: string[]) => {
    setTags(updated);
    window.fs.write(tagsFile, JSON.stringify(updated, null, 2))
      .catch(err => console.error('Error saving tags:', err));
  };

  const handleAdd = () => {
    const tag = newTag.trim();
    if (tag && !tags.includes(tag)) {
      saveTags([...tags, tag]);
      setNewTag('');
    }
  };

  const handleDelete = (tagToDelete: string) => {
    saveTags(tags.filter(t => t !== tagToDelete));
  };

  return (
    <div className="tag-manager">
      <h3>Tags</h3>
      <div className="tag-input">
        <input
          type="text"
          value={newTag}
          placeholder="New tag"
          onChange={e => setNewTag(e.target.value)}
        />
        <button onClick={handleAdd}>Add</button>
      </div>
      <ul className="tag-list">
        {tags.map(tag => (
          <li key={tag}>
            <span>{tag}</span>
            <button onClick={() => handleDelete(tag)}>×</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TagManager;
