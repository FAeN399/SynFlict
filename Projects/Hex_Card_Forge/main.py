"""
Hex Card Forge - Main Application

This file serves as the entry point for the Hex Card Forge desktop application,
implementing the GUI version using PySide6 based on HTML prototype designs.
"""

import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QStackedWidget)
from PySide6.QtGui import QIcon, QFontDatabase
from PySide6.QtCore import QResource, QFile, Qt

# Import screen modules
from screens.gateway import GatewayScreen
from screens.scriptorium import ScriptoriumScreen
from screens.visage_shaper import VisageShaper
from screens.obsidian_library import ObsidianLibrary
from screens.collection_forge import CollectionForge

# Import helpers and resources
from utils.hex_widgets import set_app_style

class HexCardForgeApp(QMainWindow):
    """Main application window for Hex Card Forge."""
    
    def __init__(self):
        super().__init__()
        
        # Setup window properties
        self.setWindowTitle("Hex Card Forge")
        self.setMinimumSize(1200, 800)
        
        # Create stacked widget to manage screens
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Initialize screens
        self.gateway_screen = GatewayScreen(self)
        self.scriptorium_screen = ScriptoriumScreen(self)
        self.visage_shaper = VisageShaper(self)
        self.obsidian_library = ObsidianLibrary(self)
        self.collection_forge = CollectionForge(self)
        
        # Add screens to stacked widget
        self.stacked_widget.addWidget(self.gateway_screen)
        self.stacked_widget.addWidget(self.scriptorium_screen)
        self.stacked_widget.addWidget(self.visage_shaper)
        self.stacked_widget.addWidget(self.obsidian_library)
        self.stacked_widget.addWidget(self.collection_forge)
        
        # Initialize with Gateway screen
        self.show_gateway()
        
        # Connect navigation signals
        self.setup_navigation()
        
    def setup_navigation(self):
        """Connect navigation signals between screens."""
        # Gateway navigation signals
        self.gateway_screen.navigate_to_scriptorium.connect(self.show_scriptorium)
        self.gateway_screen.navigate_to_obsidian_library.connect(self.show_obsidian_library)
        self.gateway_screen.navigate_to_collection_forge.connect(self.show_collection_forge)
        self.gateway_screen.navigate_to_visage_shaper.connect(self.show_visage_shaper)
        
        # Common navigation signals for returning to gateway
        self.scriptorium_screen.return_to_gateway.connect(self.show_gateway)
        self.visage_shaper.return_to_gateway.connect(self.show_gateway)
        self.obsidian_library.return_to_gateway.connect(self.show_gateway)
        self.collection_forge.return_to_gateway.connect(self.show_gateway)
        
        # Additional cross-screen navigation
        self.obsidian_library.edit_card_signal.connect(self.scriptorium_screen.edit_card)
        self.scriptorium_screen.edit_image_signal.connect(self.visage_shaper.edit_image)
    
    # Screen navigation methods
    def show_gateway(self):
        self.stacked_widget.setCurrentWidget(self.gateway_screen)
        
    def show_scriptorium(self):
        self.stacked_widget.setCurrentWidget(self.scriptorium_screen)
        
    def show_visage_shaper(self):
        self.stacked_widget.setCurrentWidget(self.visage_shaper)
        
    def show_obsidian_library(self):
        self.stacked_widget.setCurrentWidget(self.obsidian_library)
        
    def show_collection_forge(self):
        self.stacked_widget.setCurrentWidget(self.collection_forge)


def main():
    """Application entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("Hex Card Forge")
    
    # Set application style and theme
    set_app_style(app)
    
    # Create and show main window
    window = HexCardForgeApp()
    window.show()
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
