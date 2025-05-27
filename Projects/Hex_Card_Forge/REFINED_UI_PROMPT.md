# Hex Card Forge - Refined UI Design Prompt

## Overview

Create a polished, production-ready user interface design for Hex Card Forge, a specialized desktop application for creating custom hexagonal cards with metadata and images. This design should balance mystical aesthetics with functional clarity, serving as the blueprint for the v1.2 GUI implementation of the currently CLI-only tool.

## Design Foundation

### Color Palette
- **Primary**: Rich Byzantine Purple (#4A0072) - For main UI elements, headers, and primary actions
- **Secondary**: Goldenrod (#DAA520) - For highlights, important UI elements, and calls to action
- **Background**: Dark Imperial Blue (#1A1A2E) with subtle hexagonal patterns
- **Content Areas**: Slightly lighter dark shades (#252538, #2C2C44) for content containers
- **Text**: Light Gray/Off-white (#E0E0E0) for primary text, medium gray (#B0B0B0) for secondary text
- **Accents**: Dark Lavender (#5C4077) and Bronze (#8C7853) for tertiary elements

### Typography
- **Primary Font**: Inter - Clean, modern sans-serif with excellent readability
- **Header Style**: Bold weight for titles, with secondary titles in goldenrod
- **Text Hierarchy**: Clear distinction between headers (goldenrod), primary content (light gray), and secondary information (medium gray)

### Core Design Elements
- **Hexagon Motif**: Incorporate the hexagon shape throughout the interface, especially for cards, buttons, and decorative elements
- **Flat Design**: Modern, flat UI with subtle shadows for depth
- **Card Frames**: Distinctive hexagonal frames with golden borders for selected items
- **Interactive Elements**: Clear visual feedback on hover/active states with subtle animations

## Screen Specifications

### 1. Title Screen ("The Gateway")
- **Background**: Dark with subtle animated hexagonal patterns that emanate from the center
- **Logo Treatment**: "CARD FORGE" in large, bold typography with "FORGE" in goldenrod 
- **Menu Options**: Present the five core functions in hexagonal cards arranged in a visually balanced pattern
- **Each Option Should Include**:
  - Distinctive icon representing the function
  - Clear, concise title
  - Brief description of purpose (1-2 lines)
- **Visual Hierarchy**: Create clear visual prominence for "Create New Card" as the primary action

### 2. Main Application Window ("The Obsidian Library")
- **Layout**: 
  - Left sidebar for navigation (purple background)
  - Main content area for card display (dark background with subtle hex pattern)
  - Status bar at bottom showing auto-save status and app version
- **Card Library**:
  - Display hexagonal card thumbnails in a responsive grid
  - Show card titles beneath thumbnails
  - Visual indicators for card types/categories
- **Toolbar**: Search functionality with filters for card attributes
- **Navigation**: Clearly highlight the current section in the sidebar

### 3. Card Editor ("The Scriptorium")
- **Split View Layout**:
  - Left panel: Form inputs for card metadata
  - Right panel: Real-time hexagonal card preview
- **Metadata Entry**:
  - Clean input fields with subtle borders
  - "Add Property" button to dynamically add key-value pairs
  - Input validation with elegant error states
- **Image Management**:
  - Drag-and-drop upload area with clear visual feedback
  - Preview of how the image will appear in hexagonal form
  - Option to remove or replace images
- **Card Preview**:
  - Accurate representation of the final card
  - Real-time updates as metadata is changed
  - Proper hexagonal cropping of attached images
- **Action Buttons**: Clear hierarchy for save, export, and cancel actions

### 4. Image Cropping Tool ("The Visage Shaper")
- **Layout**:
  - Left: Original image with movable/resizable hexagonal mask
  - Right: Live preview of the cropped hexagonal result
- **Controls**:
  - Intuitive sliders for scaling and positioning
  - Direct numeric input options for precise control
  - Preset aspect ratios optimized for hexagonal cards
- **Visual Guidance**: Clear indicators for optimal positioning
- **Action Buttons**: Cancel and confirm options with proper visual hierarchy

### 5. Booster Pack Creation ("The Collection Forge")
- **Card Selection**:
  - Scrollable list of available cards with checkboxes
  - Compact card previews that show essential info
  - Counter showing number of selected cards
- **Pack Metadata**:
  - Input fields for pack name and description
  - Optional pack icon/sigil upload
- **Export Options**:
  - Settings for compression and content inclusion
  - Clear call-to-action for the export process
- **Preview**: Visual representation of the pack contents

## Technical Implementation Details

- **Responsive Design**: Fluid layouts that work from 1280x800 up to 4K resolutions
- **Accessibility**: Support for keyboard navigation, screen readers, and high-contrast mode
- **Animation**: Subtle transitions between states (250-350ms duration) with easing functions
- **Cross-Platform Consistency**: Ensure UI elements maintain appearance across Windows, macOS, and Linux
- **Performance**: Optimize image rendering for smooth hexagonal previews

## Final Deliverables

Create high-fidelity mockups of all five screens showing:
1. Default states
2. Active/hover states for interactive elements
3. Populated with realistic data (sample cards with fantasy/gaming themed content)
4. Error states where relevant
5. Transitions between related screens

Include annotations explaining:
- Key UI components and their purpose
- Animation and interaction behaviors
- Implementation recommendations for developers

The design should feel mystical and professional while maintaining excellent usability. It should serve as both inspiration and practical guidance for implementing the GUI version of Hex Card Forge.

## References

The interactive HTML prototype demonstrates the core concepts but should be enhanced with:
- More consistent spacing and alignment
- Improved contrast for better readability
- Refined interactions for the hex cropping tool
- Enhanced visual hierarchy across all screens

The final design should feel like a premium, specialized tool for card creation while maintaining the hexagonal theme and dark purple/gold aesthetic established in the prototype.


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hex Card Forge - UI Mockups (Dark & Mythic Theme - Refined)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #1A1A2E; /* Dark Imperial Blue - Main background */
            color: #E0E0E0; /* Light Gray/Off-white - Default text */
        }

        /* Refined Dark & Mythic Palette */
        .bg-primary-purple { background-color: #4A0072; } /* Rich Byzantine Purple */
        .text-primary-purple { color: #4A0072; }
        .border-primary-purple { border-color: #4A0072; }
        .hover\:bg-primary-purple-darker:hover { background-color: #3A005A; }

        .bg-secondary-gold { background-color: #DAA520; } /* Goldenrod */
        .text-secondary-gold { color: #DAA520; }
        .border-secondary-gold { border-color: #DAA520; }
        .hover\:bg-secondary-gold-darker:hover { background-color: #B8860B; }
        .focus\:ring-secondary-gold:focus { --tw-ring-color: #DAA520; }


        .bg-accent-dark-lavender { background-color: #5C4077; }
        .text-accent-dark-lavender { color: #5C4077; }
        .hover\:bg-accent-dark-lavender-darker:hover { background-color: #47305D; }

        .bg-accent-bronze { background-color: #8C7853; }
        .text-accent-bronze { color: #8C7853; }
        .hover\:bg-accent-bronze-darker:hover { background-color: #705D3E; }

        .bg-content-area-dark { background-color: #252538; } /* Darker shade for content cards, inputs */
        .bg-content-area-medium { background-color: #2C2C44; } /* Slightly lighter for screen containers, sidebars */
        .border-content-divider { border-color: #404058; } /* Darker border for dividers */
        
        .text-light-primary { color: #E0E0E0; } /* Primary light text */
        .text-light-secondary { color: #B0B0B0; } /* Secondary, less prominent light text */
        .text-dark-contrast { color: #1A1A2E; } /* For text on lighter mythic accents */
        .text-error { color: #F87171; } /* Red for error messages */
        .border-error { border-color: #F87171; }

        /* Subtle animated hexagonal background pattern - The Gateway */
        @keyframes hex-emanate {
            0% { transform: scale(0.5); opacity: 0; }
            50% { opacity: 0.05; }
            100% { transform: scale(2.5); opacity: 0; }
        }
        .gateway-hex-bg {
            position: relative;
            overflow: hidden;
        }
        .gateway-hex-bg::before, .gateway-hex-bg::after { /* Multiple layers for more depth */
            content: '';
            position: absolute;
            width: 200%;
            height: 200%;
            top: -50%;
            left: -50%;
            background-image: url("data:image/svg+xml,%3Csvg width='100' height='115' viewBox='0 0 100 115' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M50 0L93.3013 28.75V86.25L50 115L6.69873 86.25V28.75L50 0Z' fill='%23DAA520'/%3E%3C/svg%3E");
            background-repeat: repeat;
            background-size: 100px 115px; /* Adjust size as needed */
            animation: hex-emanate 25s linear infinite;
            opacity: 0; /* Initial opacity set by animation */
        }
        .gateway-hex-bg::after {
            animation-delay: -12.5s; /* Offset animation for second layer */
            background-image: url("data:image/svg+xml,%3Csvg width='120' height='138' viewBox='0 0 100 115' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M50 0L93.3013 28.75V86.25L50 115L6.69873 86.25V28.75L50 0Z' fill='%235C4077'/%3E%3C/svg%3E");
            background-size: 120px 138px;
        }
        /* Static hex pattern for other areas */
        .subtle-hex-pattern-static {
            background-image: url("data:image/svg+xml,%3Csvg width='80' height='92' viewBox='0 0 60 69' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M30 0L58.7846 17.25V51.75L30 69L1.21539 51.75V17.25L30 0Z' fill='%235C4077' fill-opacity='0.02'/%3E%3C/svg%3E");
        }


        .hexagon {
            clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
            transition: transform 0.3s cubic-bezier(0.25, 0.1, 0.25, 1), box-shadow 0.3s cubic-bezier(0.25, 0.1, 0.25, 1);
        }
        .hexagon:hover {
            transform: translateY(-4px) scale(1.03); /* Subtle lift and scale */
            box-shadow: 0 10px 20px rgba(218, 165, 32, 0.1), 0 6px 6px rgba(218, 165, 32, 0.08); /* Goldish glow */
        }
        
        /* Scrollbar styling */
        ::-webkit-scrollbar { width: 10px; }
        ::-webkit-scrollbar-track { background: #252538; }
        ::-webkit-scrollbar-thumb { background: #4A0072; border-radius: 5px; border: 2px solid #252538; }
        ::-webkit-scrollbar-thumb:hover { background: #5C4077; }

        .screen-container {
            min-height: 800px; /* Adjusted for typical desktop */
            padding: 24px; /* Increased padding */
            margin-bottom: 48px; /* Increased margin */
            border: 1px solid #404058;
            border-radius: 12px; /* More rounded corners */
            box-shadow: 0 8px 25px rgba(0,0,0,0.2); /* Softer, deeper shadow */
        }
        .screen-title {
            font-size: 2.25rem; /* Larger title */
            font-weight: 900; /* Bolder */
            color: #DAA520;
            margin-bottom: 24px;
            padding-bottom: 12px;
            border-bottom: 3px solid #4A0072;
        }

        /* Input field styling for dark theme */
        .dark-input {
            background-color: #252538;
            border: 1px solid #404058;
            color: #E0E0E0;
            border-radius: 6px; /* Consistent rounded corners */
            padding: 10px 14px; /* More padding */
            transition: border-color 0.25s ease-in-out, box-shadow 0.25s ease-in-out;
        }
        .dark-input::placeholder { color: #707080; }
        .dark-input:focus {
            outline: none;
            border-color: #DAA520;
            box-shadow: 0 0 0 3px rgba(218, 165, 32, 0.4); /* More prominent focus ring */
        }
        .dark-input.input-error {
            border-color: #F87171; /* text-error color */
            box-shadow: 0 0 0 3px rgba(248, 113, 113, 0.4);
        }
        .error-message-text {
            font-size: 0.875rem;
            margin-top: 4px;
        }


        /* Button Styles */
        .btn {
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 600;
            transition: all 0.25s cubic-bezier(0.25, 0.1, 0.25, 1); /* Smoother transition */
            box-shadow: 0 2px 4px rgba(0,0,0,0.15); /* Subtle shadow */
            text-align: center;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .btn:active {
            transform: translateY(0px);
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }

        .btn-primary { background-color: #4A0072; color: #E0E0E0; }
        .btn-primary:hover { background-color: #3A005A; }
        
        .btn-secondary { background-color: #DAA520; color: #1A1A2E; }
        .btn-secondary:hover { background-color: #B8860B; }

        .btn-accent { background-color: #5C4077; color: #E0E0E0; }
        .btn-accent:hover { background-color: #47305D; }

        .btn-neutral { background-color: #33334C; color: #E0E0E0; }
        .btn-neutral:hover { background-color: #404058; }

        .btn-danger { background-color: #991B1B; color: #E0E0E0; } /* For destructive actions */
        .btn-danger:hover { background-color: #7F1D1D; }

        /* Tooltip styling (basic example, can be enhanced with JS) */
        .tooltip-container { position: relative; display: inline-block; }
        .tooltip-text {
            visibility: hidden;
            width: 160px;
            background-color: #252538;
            color: #E0E0E0;
            text-align: center;
            border-radius: 6px;
            padding: 8px;
            position: absolute;
            z-index: 10;
            bottom: 125%; /* Position above the element */
            left: 50%;
            margin-left: -80px; /* Center the tooltip */
            opacity: 0;
            transition: opacity 0.3s;
            font-size: 0.875rem;
            border: 1px solid #404058;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        .tooltip-container:hover .tooltip-text { visibility: visible; opacity: 1; }

        /* Specific for hex menu items on title screen */
        .hex-menu-item {
            width: 200px; /* Fixed width for balance */
            height: 230px; /* Fixed height (approx 1.15 ratio for hexagon) */
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            cursor: pointer;
        }
        .hex-menu-item.primary-action {
            border: 3px solid #DAA520 !important; /* Emphasize primary action */
            transform: scale(1.05); /* Slightly larger */
        }
        .hex-menu-item.primary-action:hover {
            transform: scale(1.1) translateY(-4px); /* More pronounced hover for primary */
        }

        /* For card thumbnails in library */
        .card-thumbnail-hex {
            width: 100%; /* Responsive width */
            padding-bottom: 115%; /* Maintain aspect ratio for hexagon (height approx 1.15 * width) */
            position: relative;
        }
        .card-thumbnail-hex-content {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
        }
        
    </style>
</head>
<body class="p-4 md:p-8 subtle-hex-pattern-static">

    <div class="max-w-7xl mx-auto">
        <h1 class="text-4xl font-black text-secondary-gold mb-12 text-center tracking-wider">HEX CARD FORGE</h1>

        <div class="mb-12 p-6 bg-content-area-dark rounded-lg shadow-lg border border-content-divider">
            <h2 class="text-xl font-semibold text-secondary-gold mb-3">Mockup Screens Navigator:</h2>
            <ul class="flex flex-wrap gap-3">
                <li><a href="#title-screen" class="btn btn-primary text-sm">1. The Gateway (Title)</a></li>
                <li><a href="#main-app-window" class="btn btn-primary text-sm">2. The Obsidian Library</a></li>
                <li><a href="#card-editor" class="btn btn-primary text-sm">3. The Scriptorium (Editor)</a></li>
                <li><a href="#image-cropper" class="btn btn-primary text-sm">4. The Visage Shaper (Cropper)</a></li>
                <li><a href="#booster-pack" class="btn btn-primary text-sm">5. The Collection Forge</a></li>
            </ul>
            </div>

        <section id="title-screen" class="screen-container bg-content-area-medium gateway-hex-bg">
            <!-- Annotation: The Gateway serves as the entry point to the application.
                 Background features subtle, slow-emanating hexagonal patterns for a mystical feel.
                 Animation: CSS keyframes 'hex-emanate' used for background.
                 Accessibility: High contrast text on dark background. Keyboard navigation for menu items (tabbing).
            -->
            <h2 class="screen-title text-center">The Gateway</h2>
            <div class="flex flex-col items-center justify-center min-h-[700px] text-center p-6">
                <div class="mb-16">
                    <h1 class="text-8xl font-black text-primary-purple" style="color: #4A0072;">
                        CARD <span class="text-secondary-gold">FORGE</span>
                    </h1>
                    <p class="text-xl text-light-secondary mt-3">Forge Your Legend, One Hex at a Time</p>
                </div>

                <!-- Annotation: Menu options presented as hexagonal cards arranged in a visually balanced pattern.
                     "Create New Card" is given visual prominence.
                     Each hex-menu-item has hover and focus states.
                -->
                <div class="flex flex-wrap justify-center items-center gap-8">
                    <div class="hex-menu-item hexagon bg-content-area-dark border-2 border-content-divider primary-action" onclick="navigateTo('#card-editor')">
                        <svg class="w-20 h-20 mb-3 text-secondary-gold" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v6m3-3H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                        <h3 class="text-2xl font-semibold text-light-primary">Create New Card</h3>
                        <p class="text-sm text-light-secondary mt-1 px-2">Begin crafting a unique hexagonal artifact from scratch.</p>
                    </div>
                    
                    <div class="hex-menu-item hexagon bg-content-area-dark border-2 border-content-divider" onclick="alert('Navigate to Import Cards')">
                        <svg class="w-16 h-16 mb-3 text-secondary-gold" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
                        <h3 class="text-xl font-semibold text-light-primary">Import Cards</h3>
                        <p class="text-sm text-light-secondary mt-1 px-2">Unearth existing cards from a previously exported .ZIP archive.</p>
                    </div>

                    <div class="hex-menu-item hexagon bg-content-area-dark border-2 border-content-divider" onclick="navigateTo('#booster-pack')">
                        <svg class="w-16 h-16 mb-3 text-secondary-gold" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7l8 4"></path></svg>
                        <h3 class="text-xl font-semibold text-light-primary">Create Booster Pack</h3>
                        <p class="text-sm text-light-secondary mt-1 px-2">Assemble a collection of your cards into a thematic pack.</p>
                    </div>
                    
                    <div class="hex-menu-item hexagon bg-content-area-dark border-2 border-content-divider" onclick="alert('Navigate to Design Template')">
                        <svg class="w-16 h-16 mb-3 text-secondary-gold" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M9.53 16.122a3 3 0 00-5.78 1.128 2.25 2.25 0 01-2.4 2.245 4.5 4.5 0 008.4-2.245c0-.399-.078-.78-.22-1.128zm0 0a15.998 15.998 0 003.388-1.62m-5.043-.025a15.994 15.994 0 011.622-3.395m3.42 3.42a15.995 15.995 0 004.764-4.648l3.876-5.814a1.151 1.151 0 00-1.597-1.597L14.146 6.32a15.996 15.996 0 00-4.649 4.763m3.42 3.42a6.776 6.776 0 00-3.42-3.42" />
                        </svg>
                        <h3 class="text-xl font-semibold text-light-primary">Design Template</h3>
                        <p class="text-sm text-light-secondary mt-1 px-2">Customize base layouts and default fields for your cards.</p>
                    </div>
                    
                    <div class="hex-menu-item hexagon bg-content-area-dark border-2 border-content-divider" onclick="alert('Navigate to Add Image to Card')">
                         <svg class="w-16 h-16 mb-3 text-secondary-gold" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.158 0a.225.225 0 01.225-.225h.008a.225.225 0 01.225.225v.008a.225.225 0 01-.225.225h-.008a.225.225 0 01-.225-.225z" />
                        </svg>
                        <h3 class="text-xl font-semibold text-light-primary">Add Image to Card</h3>
                        <p class="text-sm text-light-secondary mt-1 px-2">Quickly imbue an existing card with a new visage.</p>
                    </div>
                </div>
            </div>
        </section>

        <section id="main-app-window" class="screen-container bg-content-area-medium">
            <!-- Annotation: Main application view.
                 Layout: Left sidebar for navigation, main area for card library, bottom status bar.
                 Responsive: Card grid adjusts to screen size.
                 Accessibility: Sidebar links are keyboard navigable. Search input has a label (visually hidden but present for screen readers).
            -->
            <h2 class="screen-title">The Obsidian Library</h2>
            <div class="h-[750px] flex flex-col border border-content-divider rounded-lg shadow-2xl overflow-hidden bg-primary-purple">
                <div class="bg-primary-purple text-light-primary p-3 flex items-center justify-between shadow-md">
                    <h3 class="text-lg font-semibold">Hex Card Forge - My Reliquary</h3>
                    <div class="flex space-x-2">
                        <span class="w-3.5 h-3.5 bg-gray-700 rounded-full opacity-50"></span>
                        <span class="w-3.5 h-3.5 bg-gray-700 rounded-full opacity-50"></span>
                        <span class="w-3.5 h-3.5 bg-gray-700 rounded-full opacity-50"></span>
                    </div>
                </div>

                <div class="flex flex-1 overflow-hidden">
                    <aside class="w-72 bg-primary-purple text-light-primary p-6 space-y-3 shadow-lg">
                        <!-- Annotation: Sidebar uses primary purple. Active selection highlighted with Goldenrod.
                             Icons aid visual recognition. Tooltips provide extra info on hover.
                             Transition: Smooth color change on hover (0.25s).
                        -->
                        <h4 class="text-2xl font-bold mb-6 text-secondary-gold tracking-wide">NAVIGATION</h4>
                        <a href="#main-app-window" class="block py-3.5 px-5 rounded-lg bg-secondary-gold text-dark-contrast font-semibold shadow-md text-left">
                            <svg class="w-6 h-6 inline-block mr-3 -mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
                            Card Library
                        </a>
                        <a href="#card-editor" class="tooltip-container block py-3.5 px-5 rounded-lg hover:bg-primary-purple-darker hover:text-secondary-gold transition-colors duration-200 text-left">
                            <svg class="w-6 h-6 inline-block mr-3 -mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
                            New Card
                            <span class="tooltip-text">Craft a new hexagonal card.</span>
                        </a>
                        <a href="#booster-pack" class="tooltip-container block py-3.5 px-5 rounded-lg hover:bg-primary-purple-darker hover:text-secondary-gold transition-colors duration-200 text-left">
                            <svg class="w-6 h-6 inline-block mr-3 -mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7l8 4"></path></svg>
                            Booster Packs
                             <span class="tooltip-text">Manage your card collections.</span>
                        </a>
                        <a href="#" class="tooltip-container block py-3.5 px-5 rounded-lg hover:bg-primary-purple-darker hover:text-secondary-gold transition-colors duration-200 text-left">
                            <svg class="w-6 h-6 inline-block mr-3 -mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                            Settings
                             <span class="tooltip-text">Configure application preferences.</span>
                        </a>
                        <div class="pt-6 border-t border-purple-700">
                            <button class="btn btn-accent w-full flex items-center justify-center">
                                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h5a3 3 0 013 3v1"></path></svg>
                                Import/Export All
                            </button>
                             </div>
                    </aside>

                    <main class="flex-1 p-8 bg-content-area-dark overflow-y-auto subtle-hex-pattern-static">
                        <div class="flex flex-col sm:flex-row justify-between items-center mb-8 gap-4">
                            <h3 class="text-3xl font-bold text-secondary-gold">My Relics (12)</h3>
                            <div class="flex items-center space-x-3">
                                <label for="search-library" class="sr-only">Search Library</label>
                                <input type="search" id="search-library" placeholder="Search relics by name or lore..." class="px-4 py-2.5 dark-input rounded-lg w-64 sm:w-auto">
                                <button class="btn btn-accent flex items-center">
                                    <svg class="w-5 h-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 01-.659 1.591l-5.432 5.432a2.25 2.25 0 00-.659 1.591v2.927a2.25 2.25 0 01-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 00-.659-1.591L3.659 7.409A2.25 2.25 0 013 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0112 3z" /></svg>
                                    Filters
                                </button>
                                </div>
                        </div>

                        <!-- Annotation: Cards are displayed as hex-shaped thumbnails.
                             Clicking a card would open it in the Card Editor.
                             Hover state includes a subtle lift and a golden border.
                             Visual indicators for card types (e.g., small icon or color-coded tag).
                        -->
                        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-x-6 gap-y-8">
                            <div class="group cursor-pointer">
                                <div class="card-thumbnail-hex">
                                   <div class="card-thumbnail-hex-content hexagon bg-content-area-medium bg-cover bg-center shadow-lg border-2 border-content-divider group-hover:border-secondary-gold flex flex-col justify-end p-2.5"
                                         style="background-image: url('https://placehold.co/300x345/2E0854/FFFFFF?text=Flame+Serpent&font=Inter');">
                                        <span class="absolute top-2 right-2 bg-red-600 text-white text-xs font-bold px-1.5 py-0.5 rounded-full shadow-sm tooltip-container">
                                            F<span class="tooltip-text">Fire Element</span>
                                        </span>
                                        <div class="bg-black bg-opacity-70 p-1.5 rounded-md">
                                            <h5 class="text-sm font-semibold text-light-primary truncate">Flame Serpent</h5>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="group cursor-pointer">
                                <div class="card-thumbnail-hex">
                                   <div class="card-thumbnail-hex-content hexagon bg-content-area-medium bg-cover bg-center shadow-lg border-2 border-content-divider group-hover:border-secondary-gold flex flex-col justify-end p-2.5"
                                         style="background-image: url('https://placehold.co/300x345/0A3B0A/FFFFFF?text=Grove+Warden&font=Inter');">
                                        <span class="absolute top-2 right-2 bg-green-600 text-white text-xs font-bold px-1.5 py-0.5 rounded-full shadow-sm tooltip-container">
                                            N<span class="tooltip-text">Nature Element</span>
                                        </span>
                                        <div class="bg-black bg-opacity-70 p-1.5 rounded-md">
                                            <h5 class="text-sm font-semibold text-light-primary truncate">Grove Warden</h5>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="group cursor-pointer opacity-70 hover:opacity-100">
                                 <div class="card-thumbnail-hex">
                                   <div class="card-thumbnail-hex-content hexagon bg-gray-700 shadow-md border-2 border-dashed border-gray-600 group-hover:border-secondary-gold flex items-center justify-center p-3">
                                        <svg class="w-10 h-10 text-gray-500 group-hover:text-secondary-gold" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
                                    </div>
                                </div>
                                <p class="text-center text-sm mt-1.5 text-light-secondary group-hover:text-secondary-gold">Add New Relic</p>
                            </div>
                            
                            <script>
                                const cardGridLib = document.querySelector('#main-app-window .grid');
                                const sampleCards = [
                                    { name: "Void Fiend", type: "D", typeFull: "Dark", color: "4B0082", imgText: "Void+Fiend" },
                                    { name: "Celestial Guardian", type: "L", typeFull: "Light", color: "FFFAF0", textColor: "333333", imgText: "Celestial+Guardian" },
                                    { name: "Tidal Drake", type: "W", typeFull: "Water", color: "006994", imgText: "Tidal+Drake" },
                                    { name: "Stoneheart Golem", type: "E", typeFull: "Earth", color: "8B4513", imgText: "Stoneheart+Golem" },
                                    { name: "Skywing Griffin", type: "A", typeFull: "Air", color: "ADD8E6", textColor: "333333", imgText: "Skywing+Griffin" },
                                    { name: "Arcane Scholar", type: "M", typeFull: "Magic", color: "800080", imgText: "Arcane+Scholar" },
                                    { name: "Ironclad Knight", type: "P", typeFull: "Physical", color: "A9A9A9", textColor: "333333", imgText: "Ironclad+Knight" },
                                ];
                                const typeColors = { 'F': 'bg-red-600', 'N': 'bg-green-600', 'D': 'bg-indigo-700', 'L': 'bg-yellow-300 text-dark-contrast', 'W': 'bg-blue-600', 'E': 'bg-yellow-700', 'A': 'bg-sky-400', 'M': 'bg-purple-600', 'P': 'bg-gray-500' };

                                if (cardGridLib && cardGridLib.children.length > 0) {
                                    sampleCards.forEach(card => {
                                        const cardClone = cardGridLib.children[0].cloneNode(true);
                                        const hexContent = cardClone.querySelector('.card-thumbnail-hex-content');
                                        const titleEl = hexContent.querySelector('h5');
                                        const typeIndicator = hexContent.querySelector('.tooltip-container');
                                        
                                        hexContent.style.backgroundImage = `url('https://placehold.co/300x345/${card.color}/${card.textColor || "FFFFFF"}?text=${card.imgText.replace(/\s/g, "+")}&font=Inter')`;
                                        titleEl.textContent = card.name;
                                        
                                        typeIndicator.childNodes[0].nodeValue = card.type; // The text node itself
                                        typeIndicator.className = `absolute top-2 right-2 ${typeColors[card.type] || 'bg-gray-500'} text-white text-xs font-bold px-1.5 py-0.5 rounded-full shadow-sm tooltip-container`;
                                        typeIndicator.querySelector('.tooltip-text').textContent = `${card.typeFull} Element`;
                                        
                                        cardGridLib.insertBefore(cardClone, cardGridLib.lastElementChild); // Insert before the "Add New"
                                    });
                                }
                            </script>
                        </div>
                         <!-- Annotation: Undo/Redo functionality would be critical.
                              These buttons could be part of a top toolbar or accessible via standard keyboard shortcuts (Ctrl/Cmd+Z, Ctrl/Cmd+Y).
                         -->
                        <div class="mt-10 flex justify-end space-x-4">
                            <button class="btn btn-neutral flex items-center">
                                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l4-4m-4 4l4 4"></path></svg>
                                Undo
                            </button>
                            <button class="btn btn-neutral flex items-center">
                                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 10h-10a8 8 0 00-8 8v2m18-10l-4-4m4 4l-4 4"></path></svg>
                                Redo
                            </button>
                        </div>
                    </main>
                </div>

                <footer class="bg-content-area-dark text-sm text-light-secondary p-3.5 border-t border-content-divider flex justify-between items-center">
                    <div>
                        <span>Auto-save: <span class="text-green-400">Enabled</span></span> | <span>Last saved: Just now</span>
                    </div>
                    <span>Version 1.2 (Mythic Facade - Refined)</span>
                </footer>
            </div>
        </section>

        <section id="card-editor" class="screen-container bg-content-area-medium">
            <!-- Annotation: Card Editor for creating and modifying cards.
                 Split view: Metadata on left, live preview on right.
                 Real-time updates to preview as user types or adds images.
                 Accessibility: All form fields have labels. Proper focus states.
            -->
            <h2 class="screen-title">The Scriptorium</h2>
            <div class="flex flex-col lg:flex-row gap-8 p-6 bg-content-area-dark rounded-lg shadow-xl border border-content-divider">
                <div class="w-full lg:w-1/2 space-y-6">
                    <div>
                        <label for="card-title" class="block text-lg font-semibold text-secondary-gold mb-1.5">Card Inscription (Title)</label>
                        <input type="text" id="card-title" placeholder="Name of the Relic..." value="Aegis of Eternal Dawn" class="w-full dark-input text-lg">
                        </div>

                    <div>
                        <h3 class="text-lg font-semibold text-secondary-gold mb-3">Mystic Properties (Attributes)</h3>
                        <!-- Annotation: Dynamically addable key-value pairs for custom attributes.
                             Input validation: Keys should be unique, values can be various types (future enhancement).
                             Error states: Highlight fields with invalid input.
                        -->
                        <div id="custom-attributes-container" class="space-y-4">
                            <div class="flex gap-3 items-start">
                                <div class="flex-1">
                                    <label for="attr-key-1" class="sr-only">Attribute Name 1</label>
                                    <input type="text" id="attr-key-1" placeholder="Property Name (e.g., Element)" value="Element" class="w-full dark-input">
                                </div>
                                <span class="text-gray-400 pt-2.5">-</span>
                                <div class="flex-1">
                                    <label for="attr-value-1" class="sr-only">Attribute Value 1</label>
                                    <input type="text" id="attr-value-1" placeholder="Property Value (e.g., Celestial)" value="Celestial" class="w-full dark-input">
                                </div>
                                <button class="btn btn-danger p-2.5 mt-0.5" onclick="this.closest('.flex.gap-3').remove()" aria-label="Remove Property">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                                </button>
                            </div>
                            <div class="flex gap-3 items-start">
                                <div class="flex-1">
                                     <label for="attr-key-2" class="sr-only">Attribute Name 2</label>
                                    <input type="text" id="attr-key-2" placeholder="Property Name" value="Power Level" class="w-full dark-input">
                                    </div>
                                <span class="text-gray-400 pt-2.5">-</span>
                                <div class="flex-1">
                                    <label for="attr-value-2" class="sr-only">Attribute Value 2</label>
                                    <input type="number" id="attr-value-2" placeholder="Numerical Value" value="1200" class="w-full dark-input">
                                </div>
                                 <button class="btn btn-danger p-2.5 mt-0.5" onclick="this.closest('.flex.gap-3').remove()" aria-label="Remove Property">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                                </button>
                            </div>
                        </div>
                        <button id="add-attribute-btn-refined" class="btn btn-accent mt-5 flex items-center">
                            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
                            Add Mystic Property
                        </button>
                    </div>

                    <div>
                        <h3 class="text-lg font-semibold text-secondary-gold mb-3">Card Visage (Image)</h3>
                        <!-- Annotation: Drag-and-drop area. Shows preview of hex-cropped image.
                             Option to remove/replace. Clear visual feedback on hover/drag.
                             Interaction: Clicking opens file dialog. Dropping file initiates upload/crop process.
                        -->
                        <div id="image-dropzone-refined" class="border-3 border-dashed border-content-divider rounded-lg p-10 text-center cursor-pointer hover:border-secondary-gold hover:bg-content-area-medium transition-all duration-300 ease-in-out bg-content-area-dark relative min-h-[200px] flex flex-col justify-center items-center">
                            <img id="image-preview-editor-refined" src="https://placehold.co/200x230/4A0072/E0E0E0?text=Hex+Glyph&font=Inter" alt="Attached Hex Image Preview" class="mx-auto mb-4 max-h-40 hexagon object-cover hidden shadow-lg">
                            <div id="image-dropzone-prompt">
                                <svg class="w-20 h-20 mx-auto text-gray-600 group-hover:text-secondary-gold mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                                <p class="text-light-secondary">Drag & drop image, or <span class="text-secondary-gold font-semibold">click to summon</span>.</p>
                                <p class="text-xs text-gray-500 mt-1">Image will be shaped into a hexagon (max 5MB).</p>
                            </div>
                            <input type="file" class="hidden" id="image-upload-input-refined" accept="image/*">
                        </div>
                         <button id="clear-image-btn-refined" class="btn btn-danger mt-3 text-sm hidden">Banish Visage</button>
                         <button id="edit-crop-btn-refined" class="btn btn-neutral mt-3 text-sm hidden">Refine Visage Shape</button>
                    </div>
                </div>

                <div class="w-full lg:w-1/2 flex flex-col items-center justify-start p-6 bg-accent-dark-lavender rounded-lg shadow-inner border border-purple-900">
                    <h3 class="text-xl font-semibold text-secondary-gold mb-6">Oracle's Preview</h3>
                    <!-- Annotation: Real-time preview. Accurately reflects metadata and hex-cropped image.
                         Golden border signifies it's a preview of the final card.
                    -->
                    <div class="w-72 h-80 md:w-80 md:h-92 relative">
                        <div id="card-preview-container-refined"
                             class="hexagon w-full h-full bg-gray-700 border-4 border-secondary-gold shadow-2xl bg-cover bg-center flex flex-col justify-between items-center p-5 text-center"
                             style="background-image: url('https://placehold.co/400x460/4A0072/E0E0E0?text=Aegis+of+Dawn&font=Inter');">
                             <h4 id="preview-title-refined" class="text-xl font-bold text-light-primary bg-black bg-opacity-75 px-4 py-2 rounded-md shadow-md break-words w-full max-w-[90%]">Aegis of Eternal Dawn</h4>
                             <div id="preview-attributes-refined" class="text-xs text-light-primary bg-black bg-opacity-75 p-3 rounded-md space-y-1.5 self-stretch max-w-[90%] overflow-y-auto max-h-24 shadow-md">
                                 <p><strong>Element:</strong> Celestial</p>
                                 <p><strong>Power Level:</strong> 1200</p>
                                 </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Annotation: Clear hierarchy for actions. Save is primary.
                 Hover/active states for all buttons.
            -->
            <div class="mt-10 flex flex-col sm:flex-row justify-end space-y-3 sm:space-y-0 sm:space-x-4">
                <button class="btn btn-neutral">Discard Changes</button>
                <button class="btn btn-accent-bronze text-light-primary">Export Relic (.ZIP)</button>
                <button class="btn btn-primary text-lg px-10 py-3">Seal Card (Save)</button>
            </div>
        </section>

        <section id="image-cropper" class="screen-container bg-content-area-medium">
            <!-- Annotation: Modal or dedicated view for cropping.
                 Left: Original image with movable/resizable hex mask. Right: Live preview.
                 Intuitive controls.
            -->
            <h2 class="screen-title">The Visage Shaper</h2>
            <div class="p-6 bg-content-area-dark rounded-lg shadow-xl max-w-5xl mx-auto border border-content-divider">
                <h3 class="text-2xl font-semibold text-secondary-gold mb-8 text-center">Shape the Hexagonal Visage</h3>
                <div class="flex flex-col lg:flex-row gap-8 items-start">
                    <div class="w-full lg:w-[60%]">
                        <h4 class="text-lg font-semibold text-light-primary mb-3">Adjust Crop Area</h4>
                        <!-- Annotation: Interactive hex-crop interface. User can drag/scale the image OR the hex overlay.
                             Visual guidance: Grid lines or center point might appear on hex overlay during interaction.
                        -->
                        <div id="crop-area-refined" class="relative w-full aspect-square sm:aspect-[4/3] bg-content-area-medium rounded-lg overflow-hidden shadow-inner border-2 border-content-divider">
                            <img src="https://placehold.co/800x600/100F1F/A0A0A0?text=Source+Artwork&font=Inter" alt="Original Image" class="absolute inset-0 w-full h-full object-contain" id="original-image-cropper-refined">
                            <div id="hex-overlay-interactive" class="absolute w-1/2 h-[57.5%] hexagon border-4 border-dashed border-secondary-gold cursor-move shadow-lg" style="top: 21.25%; left: 25%;">
                                <div class="absolute -top-1.5 -left-1.5 w-3 h-3 bg-secondary-gold rounded-full cursor-nwse-resize"></div>
                                <div class="absolute -top-1.5 -right-1.5 w-3 h-3 bg-secondary-gold rounded-full cursor-nesw-resize"></div>
                                <div class="absolute -bottom-1.5 -left-1.5 w-3 h-3 bg-secondary-gold rounded-full cursor-nesw-resize"></div>
                                <div class="absolute -bottom-1.5 -right-1.5 w-3 h-3 bg-secondary-gold rounded-full cursor-nwse-resize"></div>
                            </div>
                             </div>
                        <div class="mt-6 space-y-5">
                            <div>
                                <label for="scale-slider-refined" class="block text-sm font-medium text-light-primary mb-1">Scale Image:</label>
                                <input type="range" id="scale-slider-refined" min="20" max="300" value="100" class="w-full h-2.5 bg-gray-700 rounded-lg appearance-none cursor-pointer focus:ring-secondary-gold accent-secondary-gold">
                            </div>
                             <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                                <div>
                                    <label for="x-offset-refined" class="block text-sm font-medium text-light-primary mb-1">X Offset:</label>
                                    <input type="number" id="x-offset-refined" value="0" class="w-full dark-input">
                                </div>
                                <div>
                                    <label for="y-offset-refined" class="block text-sm font-medium text-light-primary mb-1">Y Offset:</label>
                                    <input type="number" id="y-offset-refined" value="0" class="w-full dark-input">
                                </div>
                                <div>
                                    <label for="aspect-ratio-select" class="block text-sm font-medium text-light-primary mb-1">Aspect Ratio:</label>
                                    <select id="aspect-ratio-select" class="w-full dark-input">
                                        <option value="hex_default">Hex Default (1:1.15)</option>
                                        <option value="square">Square (1:1)</option>
                                        <option value="free">Freeform</option>
                                    </select>
                                    </div>
                            </div>
                        </div>
                    </div>

                    <div class="w-full lg:w-[40%] flex flex-col items-center lg:pl-6">
                        <h4 class="text-lg font-semibold text-light-primary mb-4">Shaped Visage Preview</h4>
                        <div class="w-56 h-64 md:w-64 md:h-[290px]">
                             <div id="cropped-preview-refined" class="hexagon w-full h-full bg-gray-700 border-2 border-primary-purple shadow-2xl bg-cover bg-center"
                                 style="background-image: url('https://placehold.co/256x294/4A0072/E0E0E0?text=Shaped+Preview&font=Inter');">
                                 </div>
                        </div>
                        <p class="text-xs text-light-secondary mt-3 text-center">This is how the visage will appear on the card.</p>
                    </div>
                </div>

                <div class="mt-12 flex flex-col sm:flex-row justify-end space-y-3 sm:space-y-0 sm:space-x-4">
                    <button class="btn btn-neutral">Cancel Shaping</button>
                    <button class="btn btn-secondary text-lg px-8 py-3">Finalize Visage</button>
                </div>
            </div>
        </section>

        <section id="booster-pack" class="screen-container bg-content-area-medium">
            <!-- Annotation: Interface for creating booster packs.
                 Card selection with compact previews. Metadata fields. Export options.
            -->
            <h2 class="screen-title">The Collection Forge</h2>
            <div class="p-6 bg-content-area-dark rounded-lg shadow-xl border border-content-divider">
                <div class="flex flex-col lg:flex-row gap-10">
                    <div class="w-full lg:w-3/5">
                        <h3 class="text-xl font-semibold text-secondary-gold mb-2">Select Relics for the Pack</h3>
                        <p class="text-sm text-light-secondary mb-5">Choose cards from your library to bind into this collection.</p>
                        <div class="mb-5">
                             <label for="filter-pack-cards" class="sr-only">Filter Cards</label>
                             <input type="search" id="filter-pack-cards" placeholder="Filter relics by name, type, or lore..." class="w-full dark-input">
                        </div>
                        <!-- Annotation: Scrollable list with checkboxes. Compact previews show essential info.
                             Counter for selected cards. Hover state for list items.
                        -->
                        <div class="h-[450px] overflow-y-auto border border-content-divider rounded-lg p-4 space-y-3 bg-content-area-medium subtle-hex-pattern-static">
                            <label class="flex items-center p-3.5 bg-content-area-dark rounded-lg shadow-md hover:bg-accent-dark-lavender transition-all duration-200 ease-in-out cursor-pointer border-2 border-transparent hover:border-secondary-gold focus-within:border-secondary-gold">
                                <input type="checkbox" class="form-checkbox h-5 w-5 text-secondary-gold rounded border-gray-600 focus:ring-secondary-gold mr-4 bg-gray-700 flex-shrink-0">
                                <div class="hexagon w-12 h-14 bg-cover bg-center mr-4 border border-gray-600 flex-shrink-0" style="background-image: url('https://placehold.co/100x115/3D2B56/E0E0E0?text=DS&font=Inter');"></div>
                                <div class="flex-grow">
                                    <span class="font-semibold text-light-primary">Dragon's Soul Relic</span>
                                    <p class="text-xs text-light-secondary">Type: Fire, Power: 850</p>
                                </div>
                                <span class="ml-auto text-xs text-light-secondary px-2 py-1 bg-gray-700 rounded-full">Common</span>
                            </label>
                            <label class="flex items-center p-3.5 bg-content-area-dark rounded-lg shadow-md hover:bg-accent-dark-lavender transition-all duration-200 ease-in-out cursor-pointer border-2 border-transparent hover:border-secondary-gold focus-within:border-secondary-gold">
                                <input type="checkbox" class="form-checkbox h-5 w-5 text-secondary-gold rounded border-gray-600 focus:ring-secondary-gold mr-4 bg-gray-700 flex-shrink-0" checked>
                                <div class="hexagon w-12 h-14 bg-cover bg-center mr-4 border border-gray-600 flex-shrink-0" style="background-image: url('https://placehold.co/100x115/2A4D3E/E0E0E0?text=ET&font=Inter');"></div>
                                <div class="flex-grow">
                                    <span class="font-semibold text-light-primary">Elderwood Talisman</span>
                                    <p class="text-xs text-light-secondary">Type: Nature, Defense: 700</p>
                                </div>
                                <span class="ml-auto text-xs text-light-secondary px-2 py-1 bg-purple-700 rounded-full">Rare</span>
                            </label>
                            <script>
                                const cardSelectionListPack = document.querySelector('#booster-pack .overflow-y-auto');
                                const samplePackCards = [
                                    { name: "Void Fiend Specter", type: "Dark", detail: "Attack: 900", rarity: "Epic", bgColor: "4B0082", imgText: "VFS" },
                                    { name: "Celestial Orb", type: "Light", detail: "Utility: Heal", rarity: "Common", bgColor: "FFFAF0", textColor:"1A1A2E", imgText: "CO" },
                                    { name: "Kraken's Tentacle", type: "Water", detail: "Special: Grapple", rarity: "Rare", bgColor: "006994", imgText: "KT" },
                                ];
                                if (cardSelectionListPack && cardSelectionListPack.children.length > 0) {
                                    samplePackCards.forEach(card => {
                                        const item = cardSelectionListPack.children[0].cloneNode(true);
                                        item.querySelector('.hexagon').style.backgroundImage = `url('https://placehold.co/100x115/${card.bgColor}/${card.textColor || "E0E0E0"}?text=${card.imgText}&font=Inter')`;
                                        item.querySelector('.font-semibold').textContent = card.name;
                                        item.querySelector('.text-xs.text-light-secondary').textContent = `Type: ${card.type}, ${card.detail}`;
                                        item.querySelector('.ml-auto').textContent = card.rarity;
                                        item.querySelector('.ml-auto').className = `ml-auto text-xs px-2 py-1 rounded-full ${card.rarity === 'Common' ? 'bg-gray-700 text-light-secondary' : card.rarity === 'Rare' ? 'bg-blue-700 text-light-primary' : 'bg-purple-700 text-light-primary'}`;
                                        cardSelectionListPack.appendChild(item);
                                    });
                                }
                            </script>
                        </div>
                        <p class="text-sm text-light-secondary mt-4">Selected Relics for Pack: <span id="selected-card-count-refined" class="font-semibold text-secondary-gold">1</span></p>
                    </div>

                    <div class="w-full lg:w-2/5 space-y-7">
                        <div>
                            <label for="pack-name-refined" class="block text-lg font-semibold text-secondary-gold mb-1.5">Pack Inscription (Name)</label>
                            <input type="text" id="pack-name-refined" placeholder="e.g., Hoard of the Shadow Dragon" class="w-full dark-input text-lg">
                        </div>
                        <div>
                            <label for="pack-description-refined" class="block text-sm font-medium text-light-primary mb-1.5">Pack Lore (Description)</label>
                            <textarea id="pack-description-refined" rows="5" placeholder="Legends contained within this collection..." class="w-full dark-input"></textarea>
                        </div>
                        <div>
                            <h4 class="text-sm font-medium text-light-primary mb-2">Pack Sigil (Icon - Optional)</h4>
                            <div class="flex items-center space-x-4">
                                <div class="hexagon w-24 h-28 bg-content-area-medium flex items-center justify-center text-gray-500 text-sm border-2 border-content-divider shadow-md">
                                    <span id="pack-icon-preview-refined">Sigil</span>
                                </div>
                                <button class="btn btn-accent text-sm">Upload Sigil</button>
                            </div>
                             </div>
                        <div>
                            <h4 class="text-sm font-medium text-light-primary mb-2">Export Runes (Options)</h4>
                             <div class="space-y-2.5">
                                <label class="flex items-center cursor-pointer">
                                    <input type="checkbox" class="form-checkbox h-4.5 w-4.5 text-secondary-gold rounded border-gray-600 focus:ring-secondary-gold mr-2.5 bg-gray-700" checked>
                                    <span class="text-sm text-light-primary">Include full card visages (images)</span>
                                </label>
                                <label class="flex items-center cursor-pointer">
                                    <input type="checkbox" class="form-checkbox h-4.5 w-4.5 text-secondary-gold rounded border-gray-600 focus:ring-secondary-gold mr-2.5 bg-gray-700">
                                    <span class="text-sm text-light-primary">Compress .ZIP archive for smaller size</span>
                                </label>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="mt-12 flex flex-col sm:flex-row justify-end space-y-3 sm:space-y-0 sm:space-x-4">
                    <button class="btn btn-neutral">Abandon Forging</button>
                    <button class="btn btn-primary text-lg px-10 py-3">Forge & Export Pack</button>
                </div>
            </div>
        </section>
    </div>

    <script>
        // Refined interactivity for mockups

        // Helper to navigate for title screen (mock)
        function navigateTo(targetId) {
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth' });
            } else {
                alert('Navigation target ' + targetId + ' not found.');
            }
        }

        // Card Editor: Add attribute (Refined)
        const addAttributeBtnRefined = document.getElementById('add-attribute-btn-refined');
        if (addAttributeBtnRefined) {
            addAttributeBtnRefined.addEventListener('click', () => {
                const container = document.getElementById('custom-attributes-container');
                const attributeCount = container.children.length;
                const newAttributeHTML = `
                    <div class="flex gap-3 items-start animate-fade-in">
                        <div class="flex-1">
                            <label for="attr-key-${attributeCount + 1}" class="sr-only">Attribute Name ${attributeCount + 1}</label>
                            <input type="text" id="attr-key-${attributeCount + 1}" placeholder="Property Name" class="w-full dark-input">
                        </div>
                        <span class="text-gray-400 pt-2.5">-</span>
                        <div class="flex-1">
                             <label for="attr-value-${attributeCount + 1}" class="sr-only">Attribute Value ${attributeCount + 1}</label>
                            <input type="text" id="attr-value-${attributeCount + 1}" placeholder="Property Value" class="w-full dark-input">
                        </div>
                        <button class="btn btn-danger p-2.5 mt-0.5" onclick="this.closest('.flex.gap-3').remove()" aria-label="Remove Property">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                        </button>
                    </div>
                `;
                container.insertAdjacentHTML('beforeend', newAttributeHTML);
            });
        }
        
        // Card Editor: Image Upload & Preview (Refined)
        const imageDropzoneRefined = document.getElementById('image-dropzone-refined');
        const imageUploadInputRefined = document.getElementById('image-upload-input-refined');
        const imagePreviewEditorRefined = document.getElementById('image-preview-editor-refined');
        const cardPreviewContainerRefined = document.getElementById('card-preview-container-refined');
        const clearImageBtnRefined = document.getElementById('clear-image-btn-refined');
        const editCropBtnRefined = document.getElementById('edit-crop-btn-refined');
        const imageDropzonePrompt = document.getElementById('image-dropzone-prompt');


        function handleFileRefined(file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const imageUrl = e.target.result;
                if (imagePreviewEditorRefined) {
                    imagePreviewEditorRefined.src = imageUrl;
                    imagePreviewEditorRefined.classList.remove('hidden');
                }
                if (cardPreviewContainerRefined) {
                    cardPreviewContainerRefined.style.backgroundImage = `url('${imageUrl}')`;
                }
                if (imageDropzonePrompt) imageDropzonePrompt.classList.add('hidden');
                if (clearImageBtnRefined) clearImageBtnRefined.classList.remove('hidden');
                if (editCropBtnRefined) editCropBtnRefined.classList.remove('hidden');

                // Simulate updating cropper tool as well
                const cropperOriginalImage = document.getElementById('original-image-cropper-refined');
                const cropperPreview = document.getElementById('cropped-preview-refined');
                if(cropperOriginalImage) cropperOriginalImage.src = imageUrl;
                if(cropperPreview) cropperPreview.style.backgroundImage = `url('${imageUrl}')`; // Simplified: real crop needed
            }
            reader.readAsDataURL(file);
        }
        
        if (imageDropzoneRefined) {
            imageDropzoneRefined.addEventListener('click', (e) => {
                // Prevent click on buttons inside from triggering file input
                if (e.target === imageDropzoneRefined || imageDropzonePrompt.contains(e.target)) {
                    imageUploadInputRefined.click();
                }
            });
            imageDropzoneRefined.addEventListener('dragover', (e) => { e.preventDefault(); imageDropzoneRefined.classList.add('border-secondary-gold', 'bg-content-area-medium'); });
            imageDropzoneRefined.addEventListener('dragleave', () => { imageDropzoneRefined.classList.remove('border-secondary-gold', 'bg-content-area-medium'); });
            imageDropzoneRefined.addEventListener('drop', (e) => {
                e.preventDefault();
                imageDropzoneRefined.classList.remove('border-secondary-gold', 'bg-content-area-medium');
                if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                    handleFileRefined(e.dataTransfer.files[0]);
                }
            });
        }
        if (imageUploadInputRefined) {
            imageUploadInputRefined.addEventListener('change', (e) => {
                if (e.target.files && e.target.files[0]) {
                    handleFileRefined(e.target.files[0]);
                }
            });
        }

        if (clearImageBtnRefined) {
            clearImageBtnRefined.addEventListener('click', () => {
                if (imagePreviewEditorRefined) {
                    imagePreviewEditorRefined.src = 'https://placehold.co/200x230/4A0072/E0E0E0?text=Hex+Glyph&font=Inter';
                    imagePreviewEditorRefined.classList.add('hidden');
                }
                if (cardPreviewContainerRefined) {
                     cardPreviewContainerRefined.style.backgroundImage = `url('https://placehold.co/400x460/4A0072/E0E0E0?text=Card+Vision&font=Inter')`;
                }
                if (imageDropzonePrompt) imageDropzonePrompt.classList.remove('hidden');
                if (imageUploadInputRefined) imageUploadInputRefined.value = '';
                clearImageBtnRefined.classList.add('hidden');
                if (editCropBtnRefined) editCropBtnRefined.classList.add('hidden');
            });
        }
        if (editCropBtnRefined) {
            editCropBtnRefined.addEventListener('click', () => {
                // In a real app, this would navigate to or open the image cropper modal.
                navigateTo('#image-cropper'); // For mockup purposes
            });
        }

        // Card Editor: Live title and attribute preview (Refined)
        const cardTitleInputRefined = document.getElementById('card-title');
        const previewTitleRefined = document.getElementById('preview-title-refined');
        const customAttributesContainerRefined = document.getElementById('custom-attributes-container');
        const previewAttributesContainerRefined = document.getElementById('preview-attributes-refined');

        function updateCardPreviewAttributes() {
            if (!customAttributesContainerRefined || !previewAttributesContainerRefined) return;
            previewAttributesContainerRefined.innerHTML = ''; // Clear previous
            const attributeRows = customAttributesContainerRefined.querySelectorAll('.flex.gap-3');
            attributeRows.forEach(row => {
                const keyInput = row.querySelector('input[id^="attr-key-"]');
                const valueInput = row.querySelector('input[id^="attr-value-"]');
                if (keyInput && valueInput && keyInput.value.trim() !== '') {
                    const p = document.createElement('p');
                    p.innerHTML = `<strong>${keyInput.value.trim()}:</strong> ${valueInput.value.trim() || 'N/A'}`;
                    previewAttributesContainerRefined.appendChild(p);
                }
            });
        }

        if (cardTitleInputRefined && previewTitleRefined) {
            cardTitleInputRefined.addEventListener('input', (e) => {
                previewTitleRefined.textContent = e.target.value.trim() || "Card Title";
            });
        }
        if (customAttributesContainerRefined) {
            customAttributesContainerRefined.addEventListener('input', updateCardPreviewAttributes);
            updateCardPreviewAttributes(); // Initial call
        }
         if (addAttributeBtnRefined) { // Also update on adding new attribute
            addAttributeBtnRefined.addEventListener('click', updateCardPreviewAttributes);
        }


        // Booster Pack: Update selected card count (Refined)
        const boosterPackCheckboxesRefined = document.querySelectorAll('#booster-pack input[type="checkbox"]');
        const selectedCardCountElRefined = document.getElementById('selected-card-count-refined');
        if (boosterPackCheckboxesRefined.length > 0 && selectedCardCountElRefined) {
            function updateSelectedCountRefined() {
                const count = Array.from(boosterPackCheckboxesRefined).filter(cb => cb.checked).length;
                selectedCardCountElRefined.textContent = count;
            }
            boosterPackCheckboxesRefined.forEach(cb => cb.addEventListener('change', updateSelectedCountRefined));
            updateSelectedCountRefined(); 
        }

        // Smooth scroll for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });

        // Add a simple fade-in animation style for dynamically added elements
        const dynamicStyleSheet = document.createElement("style");
        dynamicStyleSheet.type = "text/css";
        dynamicStyleSheet.innerText = `
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .animate-fade-in { animation: fadeIn 0.35s ease-out; }
        `;
        document.head.appendChild(dynamicStyleSheet);

        // Input error simulation (conceptual)
        // const exampleErrorInput = document.querySelector('#card-title'); // Example
        // if (exampleErrorInput) {
        //     // To test error state: exampleErrorInput.classList.add('input-error');
        //     // And un-comment the error message p tag in HTML
        // }

    </script>
</body>
</html>
