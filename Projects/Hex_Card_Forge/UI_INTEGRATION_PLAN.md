# Hex Card Forge - PySide6/PyQt6 UI Integration Plan

This plan describes how to implement the Hex Card Forge UI as a modern, accessible, and visually distinctive desktop application using PySide6/PyQt6. It translates the design and interaction goals from the HTML prototypes and image prompts into actionable steps for Qt developers.

## 1. Application Structure & Component Architecture

- **Screen Modules:**
  - Implement each major screen as a dedicated QWidget subclass in `screens/`:
    - `GatewayScreen` (main menu)
    - `ScriptoriumScreen` (card editor)
    - `VisageShaper` (image cropping)
    - `ObsidianLibrary` (card library)
    - `CollectionForge` (booster pack builder)
- **Navigation:**
  - Use `QStackedWidget` for screen transitions (already scaffolded in `main.py`).
  - Implement custom signals for navigation and cross-screen actions.
- **Reusable Custom Widgets:**
  - `HexButton` (hexagonal QPushButton with hover/active effects)
  - `CardWidget` (card preview in hex frame)
  - `HexImageCropper` (interactive hex cropping tool)
  - `CardGrid` (grid layout for card thumbnails)

## 2. Theming & Styling

- **Color Palette:**
  - Primary: Byzantine Purple `#4A0072`
  - Secondary: Goldenrod `#DAA520`
  - Background: Dark Imperial Blue `#1A1A2E`
  - Content: #252538 (dark), #2C2C44 (medium)
  - Text: #E0E0E0 (light), #B0B0B0 (medium)
- **Theme Application:**
  - Implement a `set_app_style(app)` function in `utils/hex_widgets.py` or `themes.py`.
  - Apply palette and custom QSS (Qt Stylesheets) to all widgets.
  - Use SVG/QPainter for advanced hex borders, shadows, and glow effects.
- **Accessibility:**
  - Ensure keyboard navigation and focus outlines (e.g., gold 3px border on focus).
  - Use accessible colors and tooltips throughout.

## 3. Advanced Visuals & Interactions

- **Hexagonal UI:**
  - Use QPainterPath for true hexagonal masking and hit detection in `HexButton` and `CardWidget`.
  - Animate menu transitions and button hover using QPropertyAnimation.
- **Image Cropping Tool:**
  - `HexImageCropper` should allow drag, zoom, and rotate of the image within a hex mask.
  - Integrate with `cardforge.image.crop_hex` for final export.
- **Particle/Glow Effects:**
  - Simulate floating hex particles in the background using QGraphicsScene or custom paint events.
  - Add subtle animated glows to key interactive elements.

## 4. Performance & Responsiveness

- **Lazy Loading:**
  - Load card images/thumbnails on demand in library and booster pack screens.
- **Efficient Rendering:**
  - Cache QPixmaps for hex-masked images.
  - Optimize QPainter usage for real-time cropping/preview.
- **Responsive Layouts:**
  - Use QHBoxLayout/QVBoxLayout and QGridLayout with stretch factors for adaptive resizing.
  - Ensure touch targets are ≥44px for accessibility.

## 5. Accessibility & Internationalization

- Add ARIA-like descriptions via `setAccessibleName` and `setToolTip`.
- Ensure all interactive elements are reachable by keyboard.
- Prepare for translation by using Qt's tr() functions for all user-facing text.

## 6. Implementation Steps

1. **Scaffold all screen classes in `screens/` as QWidgets.**
2. **Implement `HexButton` and `CardWidget` in `utils/hex_widgets.py`.**
3. **Develop `set_app_style()` and theme system.**
4. **Build out GatewayScreen with animated hex menu and navigation.**
5. **Implement ScriptoriumScreen with form, live preview, and model binding.**
6. **Develop VisageShaper as an interactive image cropper.**
7. **Create ObsidianLibrary with CardGrid and search/filter.**
8. **Build CollectionForge for booster pack creation.**
9. **Iterate on accessibility, performance, and polish.**

## 7. Visual/Interaction References

- Follow the color, layout, and animation cues from the HTML prototypes and image_prompt_*.txt files.
- Use Inter or Noto Sans font if available for modern look.
- Maintain the "mystical, arcane" feel with premium shadows, glows, and subtle motion.

## 8. Example: HexButton Skeleton (PyQt6)

```python
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QPainter, QPainterPath, QColor
from PySide6.QtCore import Qt

class HexButton(QPushButton):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        # ... calculate hex path ...
        painter.fillPath(path, QColor("#4A0072"))
        # ... draw border, icon, text ...
        super().paintEvent(event)
```

---

**Note:** This plan replaces the previous web-based integration plan and is intended for PySide6/PyQt6 desktop application development. For detailed visual references, see the HTML prototypes and image prompts in the project root.

Create a production-ready, accessible HTML/CSS/JS implementation for Hex Card Forge that elevates the existing prototype with these specific enhancements:

## Core Architecture Improvements

1. **Component Architecture**
   - Implement a modular component structure using Web Components or a lightweight framework
   - Create reusable hex card, form input, and modal components
   - Establish clear component APIs with proper event handling and state management

2. **Advanced Hexagonal Visuals**
   - Replace basic polygon clip-paths with SVG-based hexagons that support proper borders
   - Implement multi-layered hexagonal masks with inner shadows and highlight effects
   - Create smooth hexagon rotation animations for loading states (120° increments)
   - Add particle effects with small animated hexagons for the title screen background

3. **Refined Interactions**
   - Implement drag-and-drop for the hex cropping tool with precise resizing handles
   - Create a tactile feedback system with subtle animations (200-250ms) on all interactions
   - Develop advanced form validation with contextual error messages and recovery suggestions
   - Add interactive tooltips that appear on hover with keyboard-accessible alternatives

4. **Visual Hierarchy Enhancements**
   - Implement consistent spacing using a 8px grid system throughout the interface
   - Create clear focus states with 3px gold outlines and subtle glow effects
   - Improve color contrast ratios to meet WCAG AA standards while maintaining aesthetics
   - Design a unified icon system with consistent stroke weights and hexagonal motifs

## Technical Requirements

1. **Performance Optimization**
   - Implement lazy loading for card images and thumbnails
   - Use requestAnimationFrame for smooth animations at 60fps
   - Optimize SVG rendering for the hexagonal patterns and masks
   - Implement efficient canvas-based rendering for the card preview

2. **Accessibility Improvements**
   - Add proper ARIA labels and roles for all interactive elements
   - Implement keyboard navigation with visible focus indicators
   - Support screen readers with descriptive text for all UI elements
   - Create a high-contrast mode that maintains the purple/gold theme

3. **Responsive Enhancement**
   - Design mobile-first layouts that adapt from 320px to 4K resolutions
   - Implement appropriate touch targets (min 44×44px) for mobile users
   - Create contextual UI adaptations for different screen sizes and input methods
   - Ensure all features remain accessible across device types

The implementation should strictly follow the Byzantine Purple (#4A0072) and Goldenrod (#DAA520) color scheme with the Dark Imperial Blue (#1A1A2E) background. Maintain the mystical aesthetic while ensuring professional usability and accessibility.

Create a professional showcase image for Hex Card Forge featuring:

A polished desktop application interface with a dark purple/blue gradient background (#1A1A2E to #252538) featuring an elegant hexagonal pattern overlay at 5% opacity. The interface should display:

1. Left panel: A sleek sidebar in Byzantine Purple (#4A0072) with golden highlights and five hexagonal navigation icons
2. Center/Main area: "The Scriptorium" card editor showing:
   - Left side: A form with elegant input fields for card metadata in a dark container (#252538)
   - Right side: A striking hexagonal card with golden borders (#DAA520) displaying a fantasy creature
3. The hexagonal card should feature:
   - A vibrant fantasy image properly cropped to hexagonal shape
   - A clean title at the bottom in Inter font
   - 2-3 metadata attributes visible below the title
   - A subtle inner glow in gold
4. UI elements should include:
   - Floating golden particles (small hexagons) around active areas
   - A visual "aura" effect where the purple and gold elements subtly glow
   - One visible tooltip showing a helpful hint
5. Add depth through:
   - Subtle shadows under all elements
   - Varying levels of background darkness to create visual hierarchy
   - A faint hexagonal grid as guides around the card preview

The image should evoke both mystical craftsmanship and professional software design, with photorealistic quality that showcases the application's premium, specialized nature. Use dramatic lighting to highlight the card as the focal point.

Implement a modular component architecture that:

- Separates the UI into reusable components (cards, forms, panels, cropper)
- Uses a lightweight design system for consistent spacing and sizing
- Implements proper state management between UI elements
- Allows for dynamic UI updates without page refreshes

<!-- Implement custom Web Components for reusable elements -->
<script>
// Example of a HexCard component
class HexCard extends HTMLElement {
  constructor() {
    super();
    this._shadowRoot = this.attachShadow({mode: 'open'});
    this._title = '';
    this._metadata = {};
    this._imageUrl = '';
    this.render();
  }
  
  static get observedAttributes() {
    return ['title', 'image-url'];
  }
  
  attributeChangedCallback(name, oldValue, newValue) {
    if (name === 'title') this._title = newValue;
    if (name === 'image-url') this._imageUrl = newValue;
    this.render();
  }
  
  set metadata(value) {
    this._metadata = value;
    this.render();
  }
  
  render() {
    this._shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          width: 300px;
          height: 345px;
          position: relative;
        }
        .hex-container {
          clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
          width: 100%;
          height: 100%;
          background: #252538;
          position: relative;
          overflow: hidden;
          transition: transform 0.3s cubic-bezier(0.25, 0.1, 0.25, 1), 
                      box-shadow 0.3s cubic-bezier(0.25, 0.1, 0.25, 1);
        }
        .hex-container:hover {
          transform: translateY(-4px) scale(1.03);
          box-shadow: 0 10px 20px rgba(218, 165, 32, 0.2), 
                      0 6px 10px rgba(218, 165, 32, 0.15);
        }
        .hex-border {
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
          background: transparent;
          border: 3px solid #DAA520;
          pointer-events: none;
        }
        .card-image {
          width: 100%;
          height: 75%;
          object-fit: cover;
        }
        .card-content {
          padding: 15px;
          background: linear-gradient(to bottom, rgba(74, 0, 114, 0.7), rgba(26, 26, 46, 0.9));
          position: absolute;
          bottom: 0;
          left: 0;
          right: 0;
          color: #E0E0E0;
        }
        .card-title {
          font-weight: 700;
          font-size: 1.2rem;
          margin: 0 0 8px 0;
          color: #DAA520;
        }
        .metadata-item {
          font-size: 0.8rem;
          margin: 4px 0;
          display: flex;
          justify-content: space-between;
        }
        .metadata-key {
          color: #B0B0B0;
        }
        .metadata-value {
          color: #E0E0E0;
        }
      </style>
      <div class="hex-container">
        ${this._imageUrl ? 
          `<img src="${this._imageUrl}" class="card-image" alt="Card image">` : 
          '<div class="card-image" style="background: #1A1A2E;"></div>'}
        <div class="card-content">
          <h3 class="card-title">${this._title || 'Card Title'}</h3>
          <div class="metadata-list">
            ${Object.entries(this._metadata).map(([key, value]) => `
              <div class="metadata-item">
                <span class="metadata-key">${key}:</span>
                <span class="metadata-value">${value}</span>
              </div>
            `).join('')}
          </div>
        </div>
        <div class="hex-border"></div>
      </div>
    `;
  }
}

customElements.define('hex-card', HexCard);
</script>

<!-- Example usage -->
<hex-card 
  title="Mystic Dragon" 
  image-url="path/to/dragon.jpg">
</hex-card>
<script>
  // Set metadata dynamically
  const card = document.querySelector('hex-card');
  card.metadata = {
    'power': '7',
    'element': 'fire',
    'rarity': 'legendary'
  };
</script>

/* Enhanced hexagon styling with better border effects */
.hexagon-advanced {
  position: relative;
  width: 300px; /* Adjust as needed */
  height: 345px; /* Maintain ~1.15 ratio for flat-top hexagon */
}

/* SVG-based hexagon instead of clip-path for better border control */
.hexagon-advanced::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("data:image/svg+xml,%3Csvg width='300' height='345' viewBox='0 0 300 345' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M150 0L300 86.25V258.75L150 345L0 258.75V86.25L150 0Z' fill='%23252538' stroke='%23DAA520' stroke-width='3'/%3E%3C/svg%3E");
  background-size: 100% 100%;
}

/* Enhanced card hover effects */
.card-hover-effects {
  transition: all 0.35s cubic-bezier(0.2, 0.85, 0.4, 1.5);
}
.card-hover-effects:hover {
  transform: translateY(-8px);
  filter: drop-shadow(0 10px 15px rgba(218, 165, 32, 0.2)) 
          drop-shadow(0 5px 8px rgba(74, 0, 114, 0.25));
}
.card-hover-effects:active {
  transform: translateY(-2px);
  transition: all 0.15s cubic-bezier(0.2, 0.85, 0.4, 1);
}

/* Enhanced input field styling */
.input-enhanced {
  background: #252538;
  border: 1px solid #404058;
  border-radius: 6px;
  padding: 12px 16px;
  color: #E0E0E0;
  transition: all 0.25s cubic-bezier(0.2, 0.85, 0.4, 1);
  font-family: 'Inter', sans-serif;
}
.input-enhanced:focus {
  border-color: #DAA520;
  box-shadow: 0 0 0 3px rgba(218, 165, 32, 0.3), 
              inset 0 1px 5px rgba(0, 0, 0, 0.15);
  outline: none;
}

// Enhanced drag and drop for hex image cropping
function setupHexCropper() {
  const cropperContainer = document.getElementById('hex-cropper');
  const sourceImage = document.getElementById('source-image');
  const cropPreview = document.getElementById('crop-preview');
  const hexMask = document.getElementById('hex-mask');
  
  let isDragging = false;
  let startX, startY, startLeft, startTop;
  
  // Initialize cropper position
  let maskPosition = { left: 0, top: 0 };
  let maskScale = 1.0;
  
  // Add handlers
  hexMask.addEventListener('mousedown', startDrag);
  document.addEventListener('mousemove', drag);
  document.addEventListener('mouseup', endDrag);
  
  // Scale controls
  const scaleSlider = document.getElementById('scale-slider');
  scaleSlider.addEventListener('input', updateScale);
  
  function startDrag(e) {
    isDragging = true;
    startX = e.clientX;
    startY = e.clientY;
    startLeft = maskPosition.left;
    startTop = maskPosition.top;
    hexMask.classList.add('grabbing');
    e.preventDefault();
  }
  
  function drag(e) {
    if (!isDragging) return;
    
    const deltaX = e.clientX - startX;
    const deltaY = e.clientY - startY;
    
    maskPosition.left = startLeft + deltaX;
    maskPosition.top = startTop + deltaY;
    
    updateMaskPosition();
    updatePreview();
  }
  
  function endDrag() {
    isDragging = false;
    hexMask.classList.remove('grabbing');
  }
  
  function updateScale(e) {
    maskScale = parseFloat(e.target.value);
    updateMaskPosition();
    updatePreview();
  }
  
  function updateMaskPosition() {
    hexMask.style.transform = `translate(${maskPosition.left}px, ${maskPosition.top}px) scale(${maskScale})`;
  }
  
  function updatePreview() {
    // Calculate crop parameters based on mask position and scale
    const cropX = -maskPosition.left / maskScale;
    const cropY = -maskPosition.top / maskScale;
    const cropWidth = cropperContainer.offsetWidth / maskScale;
    const cropHeight = cropperContainer.offsetHeight / maskScale;
    
    // Update preview with same parameters but with hex clipping
    cropPreview.style.backgroundPosition = `${cropX}px ${cropY}px`;
    cropPreview.style.backgroundSize = `${sourceImage.offsetWidth / maskScale}px ${sourceImage.offsetHeight / maskScale}px`;
  }
}

