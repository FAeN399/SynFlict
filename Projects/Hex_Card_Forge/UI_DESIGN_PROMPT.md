# Hex Card Forge - UI Design Prompt

## Overview

Design a modern, visually appealing GUI for Hex Card Forge, a desktop application for creating custom hexagonal cards with metadata and images. The application currently has a CLI implementation (v1.1), but we're planning the GUI façade (v1.2) with the following specifications.

## Color Scheme

Primary color palette:
- **Main Color**: Royal Purple (#7B68EE)
- **Secondary Color**: Golden Yellow (#FFD700)
- **Background**: Light neutral (#F8F8FF) with subtle hexagonal patterns
- **Text**: Dark charcoal (#333333) for readability
- **Accent Colors**: Lavender (#E6E6FA) and Amber (#FFBF00) for highlights and interactive elements

## Core Functionality

The application allows users to:
1. Create hex-shaped cards with custom metadata
2. Add images that are automatically cropped to a hexagonal shape
3. Export/Import cards as ZIP files
4. Bundle multiple cards into "booster packs"
5. Maintain history with undo/redo functionality

## Window/Screen Designs Needed

### 1. Main Application Window
- Modern, clean interface with dark purple title bar
- Left sidebar navigation in purple with yellow highlights for active selection
- Card library/thumbnails displayed in main area 
- Status bar at bottom showing auto-save status

### 2. Title Screen
- Stylized "CARD FORGE" title in bold purple with yellow accents
- Hexagon-themed background pattern
- Main menu options as in spec.md:
  - Create New Card (with "+" icon)
  - Import Cards (with folder icon)
  - Create Booster Pack (with package icon)
  - Design Card Template (with template icon)
  - Add Image to Card (with image icon)

### 3. Card Editor Screen
- Split view: 
  - Left: Form for metadata entry (title field, key-value pairs for custom attributes)
  - Right: Hex-shaped card preview with yellow border
- Image attachment area with drag-and-drop functionality
- Buttons for save, cancel, export

### 4. Image Cropping Tool
- Interactive hex-crop interface with:
  - Original image shown with hexagon overlay
  - Preview of cropped result
  - Controls for positioning, scaling
  - Apply button in yellow

### 5. Booster Pack Creation
- Card selection interface (multi-select from library)
- Pack name and metadata fields
- Export options

## Technical Specifications

- Resolution: Design for minimum 1280x800
- Responsive layout that scales with window size
- Platform-neutral design (Windows, macOS, Linux)
- Consider accessibility (high contrast, keyboard navigation)

## Style Guidelines

- Embrace hexagon motifs throughout the interface (buttons, frames, icons)
- Use flat design with subtle shadows for depth
- Purple gradient headers with yellow interactive elements
- Custom hex-shaped thumbnails for cards in the library view
- Modern, rounded buttons with hover effects
- Clean sans-serif typography (suggest a specific font family)

## Deliverables to Visualize

1. Main application window with populated card library
2. Title screen with menu options
3. Card editor with example metadata and attached image
4. Image cropping tool with an image being processed
5. Booster pack creation screen

## Notes

- This is for visualization purposes of the future v1.2 GUI façade
- The current implementation is CLI-only, but we want to see the end vision
- Focus on creating an intuitive, visually appealing interface that feels modern and professional
- Incorporate hexagonal design elements wherever appropriate to reinforce the theme

Please create detailed mockups showing the flow between these screens, with annotations explaining key UI elements and interactions.


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hex Card Forge - UI Mockups (Dark & Mythic Theme)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #1A1A2E; /* Dark Imperial Blue - Main background */
            color: #E0E0E0; /* Light Gray/Off-white - Default text */
        }

        /* Dark & Mythic Palette */
        .bg-main-purple { background-color: #4A0072; } /* Dark Byzantium */
        .text-main-purple { color: #4A0072; }
        .border-main-purple { border-color: #4A0072; }
        .hover\:bg-main-purple-darker:hover { background-color: #3A005A; } /* Slightly darker Byzantium for hover */

        .bg-secondary-gold { background-color: #DAA520; } /* Goldenrod */
        .text-secondary-gold { color: #DAA520; }
        .border-secondary-gold { border-color: #DAA520; }
        .hover\:bg-secondary-gold-darker:hover { background-color: #B8860B; } /* Darker Goldenrod for hover */
        
        .accent-main-purple { color: #4A0072; } /* For text or icons that need the main purple color */
        .accent-secondary-gold { color: #DAA520; } /* For text or icons that need the gold color */


        .bg-accent-dark-lavender { background-color: #5C4077; } /* Dark Lavender */
        .text-accent-dark-lavender { color: #5C4077; }
        .hover\:bg-accent-dark-lavender-darker:hover { background-color: #47305D; }

        .bg-accent-bronze { background-color: #8C7853; } /* Bronze */
        .text-accent-bronze { color: #8C7853; }
        .hover\:bg-accent-bronze-darker:hover { background-color: #705D3E; }

        .bg-screen-container { background-color: #2C2C44; } /* Slightly lighter dark shade for screen containers */
        .bg-content-area { background-color: #252538; } /* Dark shade for content cards, inputs etc. */
        .border-dark-accent { border-color: #404058; } /* Darker border color */
        
        .text-light { color: #E0E0E0; }
        .text-medium-light { color: #B0B0B0; } /* For less prominent text */
        .text-dark-contrast { color: #1A1A2E; } /* For text on lighter mythic accents if needed */

        /* Subtle hexagonal background pattern - Mythic Themed */
        .subtle-hex-pattern-mythic {
            background-image: url("data:image/svg+xml,%3Csvg width='60' height='69' viewBox='0 0 60 69' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M30 0L58.7846 17.25V51.75L30 69L1.21539 51.75V17.25L30 0Z' fill='%23DAA520' fill-opacity='0.03'/%3E%3C/svg%3E");
        }
        .subtle-hex-pattern-mythic-darker-bg { /* For body or main dark background */
             background-image: url("data:image/svg+xml,%3Csvg width='80' height='92' viewBox='0 0 60 69' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M30 0L58.7846 17.25V51.75L30 69L1.21539 51.75V17.25L30 0Z' fill='%235C4077' fill-opacity='0.04'/%3E%3C/svg%3E");
        }

        .hexagon {
            clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
        }
        .hexagon-button {
            clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);
            transition: transform 0.2s ease-in-out, background-color 0.2s ease-in-out;
        }
        .hexagon-button:hover {
            transform: scale(1.05);
        }

        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #2C2C44; /* Dark track */
        }
        ::-webkit-scrollbar-thumb {
            background: #4A0072; /* Main purple thumb */
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #5C4077; /* Dark lavender hover */
        }

        .screen-container {
            min-height: 800px;
            padding: 20px;
            margin-bottom: 40px;
            border: 1px solid #404058; /* Darker border */
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15); /* Slightly adjusted shadow for dark bg */
        }
        .screen-title {
            font-size: 2rem;
            font-weight: 700;
            color: #DAA520; /* Goldenrod for titles */
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #4A0072; /* Main purple underline */
        }

        /* Input field styling for dark theme */
        .dark-input {
            background-color: #252538; /* bg-content-area */
            border: 1px solid #404058; /* border-dark-accent */
            color: #E0E0E0; /* text-light */
        }
        .dark-input::placeholder {
            color: #707080; /* Lighter placeholder text */
        }
        .dark-input:focus {
            outline: none;
            border-color: #DAA520; /* Goldenrod focus border */
            box-shadow: 0 0 0 2px rgba(218, 165, 32, 0.5); /* Goldenrod focus ring */
        }

        .button-primary {
            background-color: #4A0072; /* bg-main-purple */
            color: #E0E0E0; /* text-light */
        }
        .button-primary:hover {
            background-color: #3A005A; /* hover:bg-main-purple-darker */
        }
        .button-secondary {
            background-color: #DAA520; /* bg-secondary-gold */
            color: #1A1A2E; /* text-dark-contrast */
        }
        .button-secondary:hover {
            background-color: #B8860B; /* hover:bg-secondary-gold-darker */
        }
        .button-accent {
             background-color: #5C4077; /* bg-accent-dark-lavender */
             color: #E0E0E0; /* text-light */
        }
        .button-accent:hover {
            background-color: #47305D; /* hover:bg-accent-dark-lavender-darker */
        }
        .button-neutral {
            background-color: #33334C;
            color: #E0E0E0;
        }
        .button-neutral:hover {
            background-color: #404058;
        }

    </style>
</head>
<body class="p-4 md:p-8 subtle-hex-pattern-mythic-darker-bg">

    <div class="max-w-7xl mx-auto">
        <h1 class="text-4xl font-bold text-secondary-gold mb-8 text-center">Hex Card Forge - UI Mockups (Dark & Mythic)</h1>

        <div class="mb-8 p-4 bg-content-area rounded-lg shadow-md border border-dark-accent">
            <h2 class="text-xl font-semibold text-secondary-gold mb-2">Mockup Screens:</h2>
            <ul class="flex flex-wrap gap-2">
                <li><a href="#title-screen" class="px-4 py-2 button-primary rounded-md transition">1. Title Screen</a></li>
                <li><a href="#main-app-window" class="px-4 py-2 button-primary rounded-md transition">2. Main Application Window</a></li>
                <li><a href="#card-editor" class="px-4 py-2 button-primary rounded-md transition">3. Card Editor</a></li>
                <li><a href="#image-cropper" class="px-4 py-2 button-primary rounded-md transition">4. Image Cropping Tool</a></li>
                <li><a href="#booster-pack" class="px-4 py-2 button-primary rounded-md transition">5. Booster Pack Creation</a></li>
            </ul>
        </div>

        <section id="title-screen" class="screen-container bg-screen-container subtle-hex-pattern-mythic">
            <h2 class="screen-title">1. Title Screen</h2>
            <div class="flex flex-col items-center justify-center min-h-[700px] text-center p-6">
                <div class="mb-12">
                    <h1 class="text-7xl font-black text-main-purple" style="color: #4A0072;">
                        CARD <span class="text-secondary-gold">FORGE</span>
                    </h1>
                    <p class="text-lg text-medium-light mt-2">Forge Your Legend, One Hex at a Time</p>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 w-full max-w-4xl">
                    <button class="group bg-content-area p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 flex flex-col items-center text-light hover:bg-accent-dark-lavender border border-dark-accent hover:border-secondary-gold">
                        <svg class="w-16 h-16 mb-4 text-secondary-gold group-hover:text-goldenrod" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
                        <span class="text-xl font-semibold">Create New Card</span>
                        <p class="text-sm text-medium-light mt-1">Begin a new artifact of power.</p>
                    </button>

                    <button class="group bg-content-area p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 flex flex-col items-center text-light hover:bg-accent-dark-lavender border border-dark-accent hover:border-secondary-gold">
                        <svg class="w-16 h-16 mb-4 text-secondary-gold group-hover:text-goldenrod" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
                        <span class="text-xl font-semibold">Import Relics</span>
                        <p class="text-sm text-medium-light mt-1">Unearth cards from a .ZIP archive.</p>
                    </button>

                    <button class="group bg-content-area p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 flex flex-col items-center text-light hover:bg-accent-dark-lavender border border-dark-accent hover:border-secondary-gold">
                        <svg class="w-16 h-16 mb-4 text-secondary-gold group-hover:text-goldenrod" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7l8 4"></path></svg>
                        <span class="text-xl font-semibold">Assemble Booster Pack</span>
                        <p class="text-sm text-medium-light mt-1">Curate collections of might.</p>
                    </button>

                    <button class="group bg-content-area p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 flex flex-col items-center text-light hover:bg-accent-dark-lavender border border-dark-accent hover:border-secondary-gold">
                        <svg class="w-16 h-16 mb-4 text-secondary-gold group-hover:text-goldenrod" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
                        <span class="text-xl font-semibold">Design Glyphs</span>
                         <p class="text-sm text-medium-light mt-1">Shape card templates.</p>
                    </button>

                    <button class="group bg-content-area p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 flex flex-col items-center text-light hover:bg-accent-dark-lavender border border-dark-accent hover:border-secondary-gold">
                        <svg class="w-16 h-16 mb-4 text-secondary-gold group-hover:text-goldenrod" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                        <span class="text-xl font-semibold">Imbue Image</span>
                         <p class="text-sm text-medium-light mt-1">Enchant a card with visuals.</p>
                    </button>
                </div>
                </div>
        </section>

        <section id="main-app-window" class="screen-container bg-screen-container">
            <h2 class="screen-title">2. Main Application Window</h2>
            <div class="h-[750px] flex flex-col border border-dark-accent rounded-lg shadow-2xl overflow-hidden">
                <div class="bg-main-purple text-light p-3 flex items-center justify-between shadow-md">
                    <h3 class="text-lg font-semibold">Hex Card Forge - The Obsidian Library</h3>
                    <div class="flex space-x-2">
                        <span class="w-3 h-3 bg-gray-600 rounded-full"></span>
                        <span class="w-3 h-3 bg-gray-600 rounded-full"></span>
                        <span class="w-3 h-3 bg-gray-600 rounded-full"></span>
                    </div>
                </div>

                <div class="flex flex-1 overflow-hidden">
                    <aside class="w-64 bg-main-purple text-light p-6 space-y-4 shadow-lg">
                        <h4 class="text-xl font-bold mb-6 text-secondary-gold">SCROLLS</h4>
                        <a href="#main-app-window" class="block py-3 px-4 rounded-lg bg-secondary-gold text-dark-contrast font-semibold shadow-md">
                            <svg class="w-5 h-5 inline-block mr-2 -mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
                            Card Library
                        </a>
                        <a href="#card-editor" class="block py-3 px-4 rounded-lg hover:bg-main-purple-darker hover:text-secondary-gold transition-colors duration-200">
                            <svg class="w-5 h-5 inline-block mr-2 -mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
                            New Card
                        </a>
                        <a href="#booster-pack" class="block py-3 px-4 rounded-lg hover:bg-main-purple-darker hover:text-secondary-gold transition-colors duration-200">
                            <svg class="w-5 h-5 inline-block mr-2 -mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7l8 4"></path></svg>
                            Booster Packs
                        </a>
                        <a href="#" class="block py-3 px-4 rounded-lg hover:bg-main-purple-darker hover:text-secondary-gold transition-colors duration-200">
                            <svg class="w-5 h-5 inline-block mr-2 -mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                            Settings
                        </a>
                        <div class="pt-4 border-t border-purple-800"> <button class="w-full py-3 px-4 rounded-lg bg-accent-bronze text-light font-semibold hover:bg-accent-bronze-darker transition-colors duration-200 flex items-center justify-center">
                                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h5a3 3 0 013 3v1"></path></svg>
                                Import/Export
                            </button>
                        </div>
                    </aside>

                    <main class="flex-1 p-8 bg-content-area overflow-y-auto subtle-hex-pattern-mythic">
                        <div class="flex justify-between items-center mb-6">
                            <h3 class="text-2xl font-semibold text-secondary-gold">My Relics (7)</h3>
                            <div class="flex space-x-2">
                                <input type="text" placeholder="Search ancient texts..." class="px-4 py-2 dark-input rounded-lg">
                                <button class="px-4 py-2 button-primary rounded-lg transition flex items-center">
                                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                                    Search
                                </button>
                            </div>
                        </div>

                        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
                            <div class="aspect-w-1 aspect-h-1 group cursor-pointer" style="--aspect-ratio: 1/1.15;">
                                <div class="hexagon w-full h-full bg-accent-dark-lavender bg-cover bg-center shadow-md hover:shadow-lg transition-shadow flex flex-col justify-between p-3 border-2 border-transparent group-hover:border-secondary-gold"
                                     style="background-image: url('https://placehold.co/300x350/3D2B56/E0E0E0?text=Mythic+Scroll+1&font=Inter');">
                                    <h5 class="text-sm font-bold text-light bg-black bg-opacity-60 px-2 py-1 rounded">Dragon's Soul</h5>
                                    <div class="text-xs text-light bg-black bg-opacity-60 px-2 py-1 rounded self-start">Fire Element</div>
                                </div>
                                <p class="text-center text-sm mt-1 text-medium-light group-hover:text-secondary-gold">Dragon's Soul</p>
                            </div>
                             <div class="aspect-w-1 aspect-h-1 group cursor-pointer" style="--aspect-ratio: 1/1.15;">
                                <div class="hexagon w-full h-full bg-accent-dark-lavender bg-cover bg-center shadow-md hover:shadow-lg transition-shadow flex flex-col justify-between p-3 border-2 border-transparent group-hover:border-secondary-gold"
                                     style="background-image: url('https://placehold.co/300x350/2A4D3E/E0E0E0?text=Elderwood+Talisman&font=Inter');">
                                    <h5 class="text-sm font-bold text-light bg-black bg-opacity-60 px-2 py-1 rounded">Elderwood Talisman</h5>
                                    <div class="text-xs text-light bg-black bg-opacity-60 px-2 py-1 rounded self-start">Nature Element</div>
                                </div>
                                <p class="text-center text-sm mt-1 text-medium-light group-hover:text-secondary-gold">Elderwood Talisman</p>
                            </div>
                            <div class="aspect-w-1 aspect-h-1 group cursor-pointer" style="--aspect-ratio: 1/1.15;">
                                <div class="hexagon w-full h-full bg-gray-700 shadow-md hover:shadow-lg transition-shadow flex items-center justify-center border-2 border-transparent group-hover:border-secondary-gold">
                                    <span class="text-gray-400 text-center p-2">Empty Relic Slot</span>
                                </div>
                                <p class="text-center text-sm mt-1 text-medium-light group-hover:text-secondary-gold">Empty Slot</p>
                            </div>
                            <script>
                                const cardGridMain = document.querySelector('#main-app-window .grid');
                                if (cardGridMain && cardGridMain.children.length > 0) {
                                    for (let i = 0; i < 4; i++) {
                                        const newCard = cardGridMain.children[0].cloneNode(true);
                                        newCard.querySelector('h5').textContent = `Shadow Gem ${i+1}`;
                                        newCard.querySelector('.text-xs').textContent = `Dark Element`;
                                        const randomHexColor = Math.floor(Math.random()*8388607 + 8388608).toString(16); // Darker random hex
                                        newCard.querySelector('.hexagon').style.backgroundImage = `url('https://placehold.co/300x350/${randomHexColor.substring(0,6)}/E0E0E0?text=Ancient+Rune+${i+2}&font=Inter')`;
                                        newCard.querySelector('p').textContent = `Shadow Gem ${i+1}`;
                                        cardGridMain.appendChild(newCard);
                                    }
                                }
                            </script>
                        </div>
                         <div class="mt-8 flex justify-end space-x-3">
                            <button class="px-4 py-2 button-neutral rounded-lg transition flex items-center">
                                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l4-4m-4 4l4 4"></path></svg>
                                Undo
                            </button>
                            <button class="px-4 py-2 button-neutral rounded-lg transition flex items-center">
                                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 10h-10a8 8 0 00-8 8v2m18-10l-4-4m4 4l-4 4"></path></svg>
                                Redo
                            </button>
                        </div>
                    </main>
                </div>

                <footer class="bg-content-area text-sm text-medium-light p-3 border-t border-dark-accent flex justify-between items-center">
                    <div>
                        <span>Auto-save: Active</span> | <span>Last sync: 1 minute ago</span>
                    </div>
                    <span>Version 1.2 (Mythic Facade)</span>
                </footer>
            </div>
        </section>

        <section id="card-editor" class="screen-container bg-screen-container">
            <h2 class="screen-title">3. Card Editor - The Scriptorium</h2>
            <div class="flex flex-col md:flex-row gap-8 p-4 md:p-6 bg-content-area rounded-lg shadow-xl border border-dark-accent">
                <div class="w-full md:w-1/2 space-y-6">
                    <div>
                        <h3 class="text-xl font-semibold text-secondary-gold mb-1">Card Inscription</h3>
                        <input type="text" placeholder="Name your legend..." value="Aegis of the Ancients" class="w-full px-4 py-3 dark-input rounded-lg shadow-sm">
                    </div>

                    <div>
                        <h3 class="text-xl font-semibold text-secondary-gold mb-3">Mystic Properties</h3>
                        <div id="custom-attributes-container" class="space-y-3">
                            <div class="flex gap-2 items-center">
                                <input type="text" placeholder="Property (e.g., Element)" value="Origin" class="w-2/5 px-3 py-2 dark-input rounded-lg shadow-sm">
                                <span class="text-gray-500">-</span>
                                <input type="text" placeholder="Value (e.g., Celestial)" value="Celestial" class="w-2/5 px-3 py-2 dark-input rounded-lg shadow-sm">
                                <button class="text-red-400 hover:text-red-600 p-1 rounded-full hover:bg-red-900 transition">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                                </button>
                            </div>
                            <div class="flex gap-2 items-center">
                                <input type="text" placeholder="Property" value="Defense Aura" class="w-2/5 px-3 py-2 dark-input rounded-lg shadow-sm">
                                <span class="text-gray-500">-</span>
                                <input type="text" placeholder="Value" value="950" class="w-2/5 px-3 py-2 dark-input rounded-lg shadow-sm">
                                 <button class="text-red-400 hover:text-red-600 p-1 rounded-full hover:bg-red-900 transition">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                                </button>
                            </div>
                        </div>
                        <button id="add-attribute-btn" class="mt-4 px-4 py-2 button-accent rounded-lg transition flex items-center shadow hover:shadow-md">
                            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
                            Add Property
                        </button>
                    </div>

                    <div>
                        <h3 class="text-xl font-semibold text-secondary-gold mb-3">Card Visage</h3>
                        <div id="image-dropzone" class="border-2 border-dashed border-dark-accent rounded-lg p-8 text-center cursor-pointer hover:border-secondary-gold transition bg-screen-container">
                            <img id="image-preview-editor" src="https://placehold.co/200x230/4A0072/E0E0E0?text=Hex+Glyph&font=Inter" alt="Attached Image" class="mx-auto mb-4 h-32 hexagon object-cover hidden">
                            <svg class="w-16 h-16 mx-auto text-gray-500 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                            <p class="text-medium-light">Drag & drop image, or click to summon.</p>
                            <p class="text-xs text-gray-500 mt-1">Image will be shaped by ancient magic (hexagon).</p>
                            <input type="file" class="hidden" id="image-upload-input" accept="image/*">
                        </div>
                         <button id="clear-image-btn" class="mt-2 px-3 py-1 bg-red-800 text-red-300 rounded-md hover:bg-red-700 text-sm hidden">Banish Image</button>
                    </div>
                </div>

                <div class="w-full md:w-1/2 flex flex-col items-center justify-center p-4 bg-accent-dark-lavender rounded-lg shadow-inner border border-purple-900">
                    <h3 class="text-xl font-semibold text-secondary-gold mb-4">Oracle's Preview</h3>
                    <div class="w-64 h-72 md:w-80 md:h-92 relative">
                        <div id="card-preview-container"
                             class="hexagon w-full h-full bg-gray-700 border-4 border-secondary-gold shadow-xl bg-cover bg-center flex flex-col justify-between p-4"
                             style="background-image: url('https://placehold.co/400x460/4A0072/E0E0E0?text=Card+Vision&font=Inter');">
                             <h4 id="preview-title" class="text-lg font-bold text-light bg-black bg-opacity-70 px-3 py-1 rounded self-center text-center break-words">Aegis of the Ancients</h4>
                             <div id="preview-attributes" class="text-xs text-light bg-black bg-opacity-70 p-2 rounded space-y-1 self-stretch">
                                 <p><strong>Origin:</strong> Celestial</p>
                                 <p><strong>Defense Aura:</strong> 950</p>
                             </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="mt-8 flex flex-col sm:flex-row justify-end space-y-3 sm:space-y-0 sm:space-x-4">
                <button class="px-6 py-3 button-neutral rounded-lg transition-colors duration-200 font-medium shadow hover:shadow-md">
                    Discard Changes
                </button>
                <button class="px-6 py-3 bg-accent-bronze text-light rounded-lg hover:bg-accent-bronze-darker transition-colors duration-200 font-medium shadow hover:shadow-md">
                    Export Relic (.ZIP)
                </button>
                <button class="px-8 py-3 button-primary rounded-lg transition-colors duration-200 font-semibold shadow hover:shadow-md">
                    Seal Card
                </button>
            </div>
        </section>

        <section id="image-cropper" class="screen-container bg-screen-container">
            <h2 class="screen-title">4. Image Cropping Ritual</h2>
            <div class="p-4 md:p-6 bg-content-area rounded-lg shadow-xl max-w-4xl mx-auto border border-dark-accent">
                <h3 class="text-2xl font-semibold text-secondary-gold mb-6 text-center">Hexagonal Shaping</h3>
                <div class="flex flex-col lg:flex-row gap-8 items-start">
                    <div class="w-full lg:w-2/3">
                        <h4 class="text-lg font-medium text-light mb-2">Refine the Vision</h4>
                        <div id="crop-area" class="relative w-full aspect-[4/3] bg-screen-container rounded-lg overflow-hidden shadow-inner border border-dark-accent">
                            <img src="https://placehold.co/800x600/1E1E2F/999999?text=Source+Image&font=Inter" alt="Original Image" class="absolute inset-0 w-full h-full object-contain" id="original-image-cropper">
                            <div class="absolute inset-0 flex items-center justify-center p-4">
                                <div id="hex-overlay" class="w-3/4 h-3/4 opacity-50 border-4 border-dashed border-secondary-gold hexagon cursor-move" style="max-width: 300px; max-height: 345px;">
                                    </div>
                            </div>
                        </div>
                        <div class="mt-6 space-y-4">
                            <div>
                                <label for="scale-slider" class="block text-sm font-medium text-light">Scale Image:</label>
                                <input type="range" id="scale-slider" min="50" max="200" value="100" class="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-secondary-gold">
                            </div>
                             <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <label for="x-offset" class="block text-sm font-medium text-light">X Offset:</label>
                                    <input type="number" id="x-offset" value="0" class="w-full px-3 py-2 dark-input rounded-lg shadow-sm">
                                </div>
                                <div>
                                    <label for="y-offset" class="block text-sm font-medium text-light">Y Offset:</label>
                                    <input type="number" id="y-offset" value="0" class="w-full px-3 py-2 dark-input rounded-lg shadow-sm">
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="w-full lg:w-1/3 flex flex-col items-center">
                        <h4 class="text-lg font-medium text-light mb-3">Shaped Preview</h4>
                        <div class="w-48 h-56 md:w-56 md:h-64">
                             <div id="cropped-preview" class="hexagon w-full h-full bg-gray-700 border-2 border-main-purple shadow-lg bg-cover bg-center"
                                 style="background-image: url('https://placehold.co/200x230/4A0072/E0E0E0?text=Shaped&font=Inter');">
                                 </div>
                        </div>
                        <p class="text-xs text-medium-light mt-2 text-center">Final aspect ratio will be preserved.</p>
                    </div>
                </div>

                <div class="mt-10 flex flex-col sm:flex-row justify-end space-y-3 sm:space-y-0 sm:space-x-4">
                    <button class="px-6 py-3 button-neutral rounded-lg transition-colors duration-200 font-medium shadow hover:shadow-md">
                        Cancel Ritual
                    </button>
                    <button class="px-8 py-3 button-secondary rounded-lg transition-colors duration-200 font-semibold shadow hover:shadow-md">
                        Finalize Shape
                    </button>
                </div>
            </div>
        </section>

        <section id="booster-pack" class="screen-container bg-screen-container">
            <h2 class="screen-title">5. Booster Pack Forging</h2>
            <div class="p-4 md:p-6 bg-content-area rounded-lg shadow-xl border border-dark-accent">
                <div class="flex flex-col lg:flex-row gap-8">
                    <div class="w-full lg:w-3/5">
                        <h3 class="text-xl font-semibold text-secondary-gold mb-1">Select Relics for the Hoard</h3>
                        <p class="text-sm text-medium-light mb-4">Choose cards from your library to bind into this pack.</p>
                        <div class="mb-4">
                             <input type="text" placeholder="Filter by name or power..." class="w-full px-4 py-2 dark-input rounded-lg">
                        </div>
                        <div class="h-96 overflow-y-auto border border-dark-accent rounded-lg p-4 space-y-3 bg-screen-container subtle-hex-pattern-mythic">
                            <label class="flex items-center p-3 bg-content-area rounded-lg shadow-sm hover:bg-accent-dark-lavender transition cursor-pointer border border-transparent hover:border-secondary-gold">
                                <input type="checkbox" class="form-checkbox h-5 w-5 text-secondary-gold rounded border-gray-600 focus:ring-secondary-gold mr-4 bg-gray-700">
                                <div class="hexagon w-12 h-14 bg-cover bg-center mr-4 border border-gray-600" style="background-image: url('https://placehold.co/100x115/3D2B56/E0E0E0?text=DS&font=Inter');"></div>
                                <span class="font-medium text-light">Dragon's Soul</span>
                                <span class="ml-auto text-xs text-medium-light">Fire Element</span>
                            </label>
                            <label class="flex items-center p-3 bg-content-area rounded-lg shadow-sm hover:bg-accent-dark-lavender transition cursor-pointer border border-transparent hover:border-secondary-gold">
                                <input type="checkbox" class="form-checkbox h-5 w-5 text-secondary-gold rounded border-gray-600 focus:ring-secondary-gold mr-4 bg-gray-700" checked>
                                <div class="hexagon w-12 h-14 bg-cover bg-center mr-4 border border-gray-600" style="background-image: url('https://placehold.co/100x115/2A4D3E/E0E0E0?text=ET&font=Inter');"></div>
                                <span class="font-medium text-light">Elderwood Talisman</span>
                                <span class="ml-auto text-xs text-medium-light">Nature Element</span>
                            </label>
                            <label class="flex items-center p-3 bg-content-area rounded-lg shadow-sm hover:bg-accent-dark-lavender transition cursor-pointer border border-transparent hover:border-secondary-gold">
                                <input type="checkbox" class="form-checkbox h-5 w-5 text-secondary-gold rounded border-gray-600 focus:ring-secondary-gold mr-4 bg-gray-700">
                                <div class="hexagon w-12 h-14 bg-cover bg-center mr-4 border border-gray-600" style="background-image: url('https://placehold.co/100x115/4B0082/E0E0E0?text=SG&font=Inter');"></div>
                                <span class="font-medium text-light">Shadow Gem</span>
                                <span class="ml-auto text-xs text-medium-light">Dark Element</span>
                            </label>
                            <script>
                                const cardSelectionListBooster = document.querySelector('#booster-pack .overflow-y-auto');
                                const cardNamesBooster = ["Aegis of Ancients", "Serpent's Eye", "Golem Heart", "Whisperwind"];
                                const cardTypesBooster = ["Celestial", "Water", "Earth", "Air"];
                                 if (cardSelectionListBooster && cardSelectionListBooster.children.length > 0) {
                                    for (let i = 0; i < 4; i++) {
                                        const newCardItem = cardSelectionListBooster.children[0].cloneNode(true);
                                        newCardItem.querySelector('span.font-medium').textContent = cardNamesBooster[i];
                                        newCardItem.querySelector('span.text-xs').textContent = `${cardTypesBooster[i]} Element`;
                                        const randomHexColorBooster = Math.floor(Math.random()*8388607 + 4194304).toString(16); // Darker random hex
                                        newCardItem.querySelector('.hexagon').style.backgroundImage = `url('https://placehold.co/100x115/${randomHexColorBooster.substring(0,6)}/E0E0E0?text=${cardNamesBooster[i].substring(0,2).toUpperCase()}&font=Inter')`;
                                        newCardItem.querySelector('input[type="checkbox"]').checked = Math.random() > 0.5;
                                        cardSelectionListBooster.appendChild(newCardItem);
                                    }
                                }
                            </script>
                        </div>
                        <p class="text-sm text-medium-light mt-3">Selected Relics: <span id="selected-card-count" class="font-semibold text-secondary-gold">1</span></p>
                    </div>

                    <div class="w-full lg:w-2/5 space-y-6">
                        <div>
                            <h3 class="text-xl font-semibold text-secondary-gold mb-1">Pack Inscription</h3>
                            <label for="pack-name" class="block text-sm font-medium text-light mb-1">Pack Name:</label>
                            <input type="text" id="pack-name" placeholder="e.g., Hoard of the Dragon Lord" class="w-full px-4 py-3 dark-input rounded-lg shadow-sm">
                        </div>
                        <div>
                            <label for="pack-description" class="block text-sm font-medium text-light mb-1">Pack Lore (Optional):</label>
                            <textarea id="pack-description" rows="4" placeholder="Describe the legends within..." class="w-full px-4 py-3 dark-input rounded-lg shadow-sm"></textarea>
                        </div>
                        <div>
                            <h4 class="text-md font-semibold text-secondary-gold mb-2">Pack Sigil (Optional)</h4>
                            <div class="flex items-center space-x-4">
                                <div class="hexagon w-20 h-24 bg-screen-container flex items-center justify-center text-gray-500 text-xs border border-dark-accent">
                                    <span id="pack-icon-preview">Sigil</span>
                                </div>
                                <button class="px-4 py-2 button-accent text-sm rounded-lg shadow hover:shadow-md">
                                    Upload Sigil
                                </button>
                            </div>
                        </div>
                        <div>
                            <h4 class="text-md font-semibold text-secondary-gold mb-2">Export Runes</h4>
                             <div class="space-y-2">
                                <label class="flex items-center">
                                    <input type="checkbox" class="form-checkbox h-4 w-4 text-secondary-gold rounded border-gray-600 focus:ring-secondary-gold mr-2 bg-gray-700" checked>
                                    <span class="text-sm text-light">Include card visages</span>
                                </label>
                                <label class="flex items-center">
                                    <input type="checkbox" class="form-checkbox h-4 w-4 text-secondary-gold rounded border-gray-600 focus:ring-secondary-gold mr-2 bg-gray-700">
                                    <span class="text-sm text-light">Compress archive</span>
                                </label>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="mt-10 flex flex-col sm:flex-row justify-end space-y-3 sm:space-y-0 sm:space-x-4">
                    <button class="px-6 py-3 button-neutral rounded-lg transition-colors duration-200 font-medium shadow hover:shadow-md">
                        Abandon Forging
                    </button>
                    <button class="px-8 py-3 button-primary rounded-lg transition-colors duration-200 font-semibold shadow hover:shadow-md">
                        Forge & Export Pack
                    </button>
                </div>
            </div>
        </section>
    </div>

    <script>
        // Basic interactivity for mockups (should still work with new theme)

        const addAttributeBtn = document.getElementById('add-attribute-btn');
        if (addAttributeBtn) {
            addAttributeBtn.addEventListener('click', () => {
                const container = document.getElementById('custom-attributes-container');
                const newAttribute = document.createElement('div');
                newAttribute.className = 'flex gap-2 items-center animate-fade-in';
                newAttribute.innerHTML = `
                    <input type="text" placeholder="Property" class="w-2/5 px-3 py-2 dark-input rounded-lg shadow-sm">
                    <span class="text-gray-500">-</span>
                    <input type="text" placeholder="Value" class="w-2/5 px-3 py-2 dark-input rounded-lg shadow-sm">
                    <button class="text-red-400 hover:text-red-600 p-1 rounded-full hover:bg-red-900 transition" onclick="this.parentElement.remove()">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                    </button>
                `;
                container.appendChild(newAttribute);
            });
        }
        
        const imageDropzone = document.getElementById('image-dropzone');
        const imageUploadInput = document.getElementById('image-upload-input');
        const imagePreviewEditor = document.getElementById('image-preview-editor');
        const cardPreviewContainer = document.getElementById('card-preview-container');
        const clearImageBtn = document.getElementById('clear-image-btn');

        if (imageDropzone) {
            imageDropzone.addEventListener('click', () => imageUploadInput.click());
            imageDropzone.addEventListener('dragover', (e) => {
                e.preventDefault();
                imageDropzone.classList.add('border-secondary-gold', 'bg-purple-900'); // Use gold for hover highlight
            });
            imageDropzone.addEventListener('dragleave', () => {
                imageDropzone.classList.remove('border-secondary-gold', 'bg-purple-900');
            });
            imageDropzone.addEventListener('drop', (e) => {
                e.preventDefault();
                imageDropzone.classList.remove('border-secondary-gold', 'bg-purple-900');
                if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                    handleFile(e.dataTransfer.files[0]);
                }
            });
        }
        if (imageUploadInput) {
            imageUploadInput.addEventListener('change', (e) => {
                if (e.target.files && e.target.files[0]) {
                    handleFile(e.target.files[0]);
                }
            });
        }
        
        function handleFile(file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                if (imagePreviewEditor) {
                    imagePreviewEditor.src = e.target.result;
                    imagePreviewEditor.classList.remove('hidden');
                    const dropzoneSVG = imageDropzone.querySelector('svg');
                    const dropzonePs = imageDropzone.querySelectorAll('p');
                    if(dropzoneSVG) dropzoneSVG.classList.add('hidden');
                    dropzonePs.forEach(p => p.classList.add('hidden'));
                }
                if (cardPreviewContainer) {
                    cardPreviewContainer.style.backgroundImage = `url('${e.target.result}')`;
                }
                if (clearImageBtn) clearImageBtn.classList.remove('hidden');

                const cropperOriginalImage = document.getElementById('original-image-cropper');
                const cropperPreview = document.getElementById('cropped-preview');
                if(cropperOriginalImage) cropperOriginalImage.src = e.target.result;
                if(cropperPreview) cropperPreview.style.backgroundImage = `url('${e.target.result}')`;
            }
            reader.readAsDataURL(file);
        }

        if (clearImageBtn) {
            clearImageBtn.addEventListener('click', () => {
                if (imagePreviewEditor) {
                    imagePreviewEditor.src = 'https://placehold.co/200x230/4A0072/E0E0E0?text=Hex+Glyph&font=Inter';
                    imagePreviewEditor.classList.add('hidden');
                     const dropzoneSVG = imageDropzone.querySelector('svg');
                    const dropzonePs = imageDropzone.querySelectorAll('p');
                    if(dropzoneSVG) dropzoneSVG.classList.remove('hidden');
                    dropzonePs.forEach(p => p.classList.remove('hidden'));
                }
                if (cardPreviewContainer) {
                     cardPreviewContainer.style.backgroundImage = `url('https://placehold.co/400x460/4A0072/E0E0E0?text=Card+Vision&font=Inter')`;
                }
                if (imageUploadInput) imageUploadInput.value = '';
                clearImageBtn.classList.add('hidden');
            });
        }

        const cardTitleInput = document.querySelector('#card-editor input[placeholder="Name your legend..."]');
        const previewTitle = document.getElementById('preview-title');
        
        if (cardTitleInput && previewTitle) {
            cardTitleInput.addEventListener('input', (e) => {
                previewTitle.textContent = e.target.value || "Card Inscription";
            });
        }

        const boosterPackCheckboxes = document.querySelectorAll('#booster-pack input[type="checkbox"]');
        const selectedCardCountEl = document.getElementById('selected-card-count');
        if (boosterPackCheckboxes.length > 0 && selectedCardCountEl) {
            function updateSelectedCount() {
                const count = Array.from(boosterPackCheckboxes).filter(cb => cb.checked).length;
                selectedCardCountEl.textContent = count;
            }
            boosterPackCheckboxes.forEach(cb => cb.addEventListener('change', updateSelectedCount));
            updateSelectedCount(); 
        }

        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            });
        });

        const styleSheet = document.createElement("style");
        styleSheet.type = "text/css";
        styleSheet.innerText = `
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .animate-fade-in { animation: fadeIn 0.3s ease-out; }
        `;
        document.head.appendChild(styleSheet);

    </script>
</body>
</html>
