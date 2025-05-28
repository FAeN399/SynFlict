# Script to restore modern_gui.py to a working state
import os
import shutil

# Create a backup of the current file
if os.path.exists('modern_gui.py'):
    shutil.copy('modern_gui.py', 'modern_gui.py.bak')
    print("Created backup of modern_gui.py as modern_gui.py.bak")

# Create a minimal working version with essential imports and structure
with open('modern_gui.py', 'w') as f:
    f.write('''import sys
import os
import time
import pathlib
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QComboBox, QCheckBox, QFrame, QScrollArea,
    QGridLayout, QProgressBar, QFileDialog, QMessageBox, QSpinBox,
    QGraphicsDropShadowEffect, QGroupBox, QFormLayout, QRadioButton, QTabWidget,
    QToolButton, QSpacerItem, QSizePolicy, QDialog
)
from PySide6.QtCore import QTimer, Qt, Signal, QSize, QThread, Slot, QUrl
from PySide6.QtGui import QIcon, QFont, QPalette, QColor, QPixmap, QPainter, QBrush, QDesktopServices

# Import custom modules
from gui_backend import GUIBackend
import theme as app_theme

# Worker class for search functionality
class SearchWorker(QThread):
    """Thread worker for handling searches"""
    results_ready = Signal(list)
    search_error = Signal(str)
    search_completed = Signal()
    
    def __init__(self, backend, keywords, media_type="All", sort="relevance", time_filter="all", limit=50, allow_nsfw=False):
        super().__init__()
        self.backend = backend
        self.keywords = keywords
        self.media_type = media_type
        self.sort = sort
        self.time_filter = time_filter
        self.limit = limit
        self.allow_nsfw = allow_nsfw
        self.is_running = True
    
    def run(self):
        """Main search function"""
        try:
            # Call backend search method
            results = self.backend.search_reddit(
                keywords=self.keywords,
                media_type=self.media_type,
                sort=self.sort,
                time_filter=self.time_filter,
                limit=self.limit,
                allow_nsfw=self.allow_nsfw
            )
            
            # Emit results if we're still running
            if self.is_running:
                self.results_ready.emit(results)
        except Exception as e:
            # Emit error if we're still running
            if self.is_running:
                self.search_error.emit(str(e))
        finally:
            # Emit completed signal if we're still running
            if self.is_running:
                self.search_completed.emit()
    
    def stop(self):
        """Stop the search worker"""
        self.is_running = False

# Worker class for download functionality
class DownloadWorker(QThread):
    """Thread worker for handling downloads"""
    progress_updated = Signal(str, int, str)
    download_completed = Signal(str, bool, str)
    
    def __init__(self, backend, download_ids):
        super().__init__()
        self.backend = backend
        self.download_ids = download_ids
        self.is_running = True
        
    def run(self):
        """Main download loop"""
        # Process all download IDs in the queue
        while self.is_running and self.download_ids:
            # Get the first download ID from the queue
            download_id = self.download_ids[0]
            
            # Check status every 0.5 seconds and update progress
            success = False
            while self.is_running:
                # Get current status from backend
                status_data = self.backend.get_queue_status()
                
                # Find our download
                current_item = None
                for item in status_data:
                    if item.get('download_id') == download_id:
                        current_item = item
                        break
                
                if not current_item:
                    # Download might be completed or removed from queue
                    break
                    
                # Update progress
                progress = current_item.get('progress', 0)
                status = current_item.get('status', 'Queued')
                self.progress_updated.emit(download_id, progress, status)
                
                # Check if download completed
                if status in ['Completed', 'Failed', 'Cancelled']:
                    success = status == 'Completed'
                    message = current_item.get('message', 'Download completed' if success else 'Download failed')
                    break
                    
                # Sleep before checking again
                time.sleep(0.5)
            
            # Emit completion signal
            if self.is_running:
                message = 'Download completed successfully' if success else 'Download failed'
                self.download_completed.emit(download_id, success, message)
                
                # Remove from our processing queue
                if download_id in self.download_ids:
                    self.download_ids.remove(download_id)
            
    def stop(self):
        """Stop the download worker"""
        self.is_running = False

# Main window class for the application
class ModernMainWindow(QMainWindow):
    theme_changed_signal = Signal(bool)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reddit Media Grabber")
        self.setGeometry(100, 100, 1350, 950)
        self.current_theme = 'light'
        
        # Initialize backend integration
        self.backend = GUIBackend()
        
        # Set up UI
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Add status bar
        self.statusBar().showMessage("Ready")
        
        # Create a label for demonstration
        label = QLabel("Reddit Media Grabber")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 24))
        main_layout.addWidget(label)
        
        # Create a descriptive label
        desc_label = QLabel("The application UI has been temporarily simplified while we fix the styling issues.")
        desc_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(desc_label)
        
    def _format_file_size(self, size_bytes):
        """Format file size in human-readable format"""
        if size_bytes is None:
            return "Unknown size"
                    
        size_bytes = int(size_bytes)
                
        # Define units and thresholds
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        size = float(size_bytes)
        unit_index = 0
                
        # Find appropriate unit
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
            
        # Format with 2 decimal places if not bytes
        if unit_index == 0:
            return f"{int(size)} {units[unit_index]}"
        else:
            return f"{size:.2f} {units[unit_index]}"

# Application entry point
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Create icons directory if it doesn't exist
    icons_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons')
    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir)
        print(f"Created icons directory: {icons_dir}")
    else:
        print(f"Icons directory exists: {icons_dir}")
    
    main_window = ModernMainWindow()
    main_window.show()
    sys.exit(app.exec())
''')

print("Created a clean version of modern_gui.py")
