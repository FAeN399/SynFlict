import { useState, useEffect } from 'react';
import './TemplateGallery.css';

interface TemplateData {
  name: string;
  description: string;
  file: string;
}

const TEMPLATE_FILES: TemplateData[] = [
  { name: 'Daily Draw', file: 'daily_draw.json', description: '' },
  { name: 'Celtic Cross', file: 'celtic_cross.json', description: '' },
];

interface TemplateGalleryProps {
  selected: string;
  onSelect: (file: string) => void;
}

export default function TemplateGallery({ selected, onSelect }: TemplateGalleryProps) {
  const [appPath, setAppPath] = useState<string>('');
  const [templates, setTemplates] = useState<TemplateData[]>([]);

  useEffect(() => {
    (window as any).app.getAppPath().then((dir: string) => {
      setAppPath(dir);
      Promise.all(
        TEMPLATE_FILES.map(t =>
          window.fs
            .read(`${dir}/resources/templates/${t.file}`)
            .then(data => {
              const json = JSON.parse(data);
              return { file: t.file, name: json.name, description: json.description };
            })
        )
      )
        .then(results => setTemplates(results))
        .catch(err => console.error('Error loading templates:', err));
    });
  }, []);

  if (!appPath) {
    return <div className="template-gallery">Loading templates...</div>;
  }

  return (
    <div className="template-gallery">
      {templates.map(t => (
        <div
          key={t.file}
          className={`template-card${t.file === selected ? ' selected' : ''}`}
          onClick={() => onSelect(t.file)}
        >
          <h4>{t.name}</h4>
          <p>{t.description}</p>
        </div>
      ))}
    </div>
  );
}
