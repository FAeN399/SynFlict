"""Reddit Grabber - Modern UI
A modern, responsive PySide6 GUI for Reddit Media Grabber with a purple and yellow theme.
"""

# Import standard modules
import sys
import os
import time
import json
import logging
import datetime
import webbrowser
from urllib.parse import urlparse
import pathlib
from functools import partial

# Configure logging to show debug messages
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Import PySide6 modules
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QComboBox, QCheckBox, QFrame, QScrollArea,
    QGridLayout, QProgressBar, QFileDialog, QMessageBox, QSpinBox,
    QGraphicsDropShadowEffect, QGroupBox, QFormLayout, QRadioButton, QTabWidget,
    QToolButton, QSpacerItem, QSizePolicy, QDialog, QTableWidget, QTableWidgetItem,
    QHeaderView, QStackedWidget, QListWidget, QListWidgetItem, QDateEdit, QSlider,
    QToolBar, QStatusBar, QMenu
)
from PySide6.QtCore import QTimer, Qt, Signal, QSize, QThread, Slot, QUrl, QDate, QRect
from PySide6.QtGui import QAction, QIcon, QFont, QPalette, QColor, QPixmap, QPainter, QBrush, QDesktopServices, QCursor, QMovie

# Import custom modules
from gui_backend import GUIBackend
import theme as app_theme

# Worker class for search functionality
class SearchWorker(QThread):
    """Thread worker for handling searches"""
    results_ready = Signal(list)
    search_error = Signal(str)
    search_completed = Signal()
    
    def __init__(self, backend, keywords, media_type="All", sort="relevance", time_period="all", limit=50, allow_nsfw=False, only_nsfw=False):
        super().__init__()
        self.backend = backend
        self.keywords = keywords
        self.media_type = media_type
        self.sort = sort
        self.time_period = time_period
        self.limit = limit
        self.allow_nsfw = allow_nsfw
        self.only_nsfw = only_nsfw
        self.is_running = True
        
        # Add debug logging for initialization
        logging.debug("[SearchWorker] Initialized with NSFW flags - allow:%s only:%s", 
                     self.allow_nsfw, self.only_nsfw)
    
    def run(self):
        """Main search function"""
        try:
            logging.debug("[SearchWorker] Starting search with parameters:")
            logging.debug("  keywords: %s", self.keywords)
            logging.debug("  media_type: %s", self.media_type)
            logging.debug("  sort: %s", self.sort)
            logging.debug("  time_period: %s", self.time_period)
            logging.debug("  limit: %d", self.limit)
            logging.debug("  NSFW flags - allow:%s only:%s", self.allow_nsfw, self.only_nsfw)
            
            # Call backend search method with consistent parameter naming
            results = self.backend.search_reddit(
                keywords=self.keywords,
                media_type=self.media_type,
                sort_by=self.sort,
                time_period=self.time_period,
                limit=self.limit,
                allow_nsfw=self.allow_nsfw,
                only_nsfw=self.only_nsfw
            )
            
            # Debug info about results
            logging.debug("[SearchWorker] Search completed:")
            logging.debug("  Total results: %d", len(results) if results else 0)
            if results:
                nsfw_count = sum(1 for r in results if r.get('nsfw', False))
                logging.debug("  NSFW results: %d", nsfw_count)
            
            # Emit results if we're still running
            if self.is_running:
                self.results_ready.emit(results)
        except Exception as e:
            # Print detailed error for debugging
            import traceback
            logging.error("[SearchWorker] Search error: %s", str(e))
            traceback.print_exc()
            
            # Emit error if we're still running
            if self.is_running:
                self.search_error.emit(f"Search failed: {str(e)}")
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
        self.setMinimumSize(900, 600)
        self.current_theme = 'light'
        
        # Initialize backend integration
        self.backend = GUIBackend()
        
        # Initialize worker threads
        self.download_worker = None
        self.search_worker = None
        
        # Initialize UI element references to None to prevent AttributeError
        self.client_id_input = None
        self.client_secret_input = None
        self.reddit_status_label = None
        self.nsfw_filter_toggle = None
        self.download_dir_input = None
        self.theme_toggle_button = None
        self.light_theme_radio = None
        self.dark_theme_radio = None
        
        # Dictionary to track download items in the UI
        self.download_items = {}
        self.history_items = []
        
        # Set up UI
        self.init_ui()
        
        # Apply theme
        self.set_theme(self.current_theme)
        
        # Load settings
        self._load_settings()
        
    def _load_settings(self):
        """Load settings from backend"""
        # Load Reddit credentials
        self._load_reddit_credentials()
        
        # Load other settings if needed
        # ...
        
    def _load_reddit_credentials(self):
        """Load Reddit credentials from config and populate UI fields"""
        if not hasattr(self, 'backend') or not self.backend:
            return
        
        # Get config from backend
        config = self.backend.config
        if 'reddit' in config:
            # Update UI fields if they exist
            if hasattr(self, 'client_id_input') and self.client_id_input is not None:
                self.client_id_input.setText(config['reddit'].get('client_id', ''))
            if hasattr(self, 'client_secret_input') and self.client_secret_input is not None:
                self.client_secret_input.setText(config['reddit'].get('client_secret', ''))
            
            # Update connection status
            if hasattr(self, 'reddit_status_label') and self.reddit_status_label is not None:
                if self.backend.reddit:
                    if hasattr(self.backend, 'is_mock_mode') and self.backend.is_mock_mode:
                        self.reddit_status_label.setText("<font color='orange'>Connected (Mock Mode)</font>")
                        # Show tooltip explaining mock mode
                        self.reddit_status_label.setToolTip("Using mock data for testing. To use real Reddit data, update your credentials in the Settings tab.")
                    else:
                        self.reddit_status_label.setText("<font color='green'>Connected to Reddit API</font>")
                else:
                    self.reddit_status_label.setText("<font color='red'>Disconnected</font>")
    
    def init_ui(self):
        """Initialize the user interface"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create status bar
        self.statusBar().showMessage("Ready")
        
        # Create main tab widget for different sections
        self.main_tabs = QTabWidget()
        
        # Create tabs
        self.download_tab = QWidget()
        self.queue_history_tab = QWidget()
        self.settings_tab = QWidget()
        
        # Add tabs to tab widget
        self.main_tabs.addTab(self.download_tab, "Download")
        self.main_tabs.addTab(self.queue_history_tab, "Queue & History")
        self.main_tabs.addTab(self.settings_tab, "Settings")
        
        # Setup tab layouts
        self.setup_download_tab()
        self.setup_queue_history_tab()
        self.setup_settings_tab()
        
        # Add the main tabs to the main layout
        main_layout.addWidget(self.main_tabs)
        
    def setup_download_tab(self):
        """Set up the Download tab with Reddit authentication, single post download, and global search"""
        layout = QVBoxLayout(self.download_tab)
        layout.setSpacing(15)
        
        # Reddit Authentication Group
        auth_group = QGroupBox("Reddit Authentication")
        auth_layout = QVBoxLayout(auth_group)
        
        auth_status = QHBoxLayout()
        status_label = QLabel("Status:")
        self.reddit_status_label = QLabel("Not Connected")
        auth_status.addWidget(status_label)
        auth_status.addWidget(self.reddit_status_label)
        auth_status.addStretch(1)
        
        auth_button = QPushButton("Connect to Reddit API")
        auth_button.setObjectName("primaryButton")
        auth_button.clicked.connect(self.handle_reddit_connect)
        
        auth_layout.addLayout(auth_status)
        auth_layout.addWidget(auth_button)
        
        # Single Post Download Card
        single_post_group = QGroupBox("Single Post Download")
        single_post_layout = QVBoxLayout(single_post_group)
        
        url_layout = QHBoxLayout()
        url_label = QLabel("Reddit URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter Reddit post URL (e.g., https://www.reddit.com/r/...)")
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input, 1)
        
        single_download_button = QPushButton("Download")
        single_download_button.setObjectName("downloadButton")
        single_download_button.clicked.connect(self.handle_single_download)
        
        single_progress = QProgressBar()
        single_progress.setRange(0, 100)
        single_progress.setValue(0)
        
        single_status = QLabel("Ready to download")
        
        single_post_layout.addLayout(url_layout)
        single_post_layout.addWidget(single_download_button, 0, Qt.AlignRight)
        single_post_layout.addWidget(single_progress)
        single_post_layout.addWidget(single_status)
        
        # Global Search Download Card
        global_search_group = QGroupBox("Global Search Download")
        global_search_layout = QVBoxLayout(global_search_group)
        
        # Search parameters form
        search_form = QFormLayout()
        search_form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        search_form.setHorizontalSpacing(10)
        search_form.setVerticalSpacing(10)
        
        # Keywords
        self.keywords_input = QLineEdit()
        self.keywords_input.setPlaceholderText("Enter search keywords...")
        search_form.addRow("Keywords:", self.keywords_input)
        
        # Media type
        self.media_type_combo = QComboBox()
        self.media_type_combo.addItems(["All", "Images", "Videos", "GIFs", "Articles"])
        search_form.addRow("Media Type:", self.media_type_combo)
        
        # Sort options
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Relevance", "Hot", "New", "Top", "Comments"])
        search_form.addRow("Sort By:", self.sort_combo)
        
        # Time period
        self.time_period_combo = QComboBox()
        self.time_period_combo.addItems(["All Time", "Day", "Week", "Month", "Year"])
        search_form.addRow("Time Period:", self.time_period_combo)
        
        # NSFW filter options
        nsfw_layout = QHBoxLayout()
        self.nsfw_filter_toggle = QCheckBox("Allow NSFW Content")
        self.only_nsfw_toggle = QCheckBox("Only NSFW")
        
        # Connect the checkboxes to handle mutual exclusivity
        self.nsfw_filter_toggle.stateChanged.connect(self._handle_nsfw_toggle)
        self.only_nsfw_toggle.stateChanged.connect(self._handle_only_nsfw_toggle)
        
        nsfw_layout.addWidget(self.nsfw_filter_toggle)
        nsfw_layout.addWidget(self.only_nsfw_toggle)
        nsfw_layout.addStretch(1)
        search_form.addRow("NSFW Options:", nsfw_layout)
        
        # Result limit
        self.limit_input = QSpinBox()
        self.limit_input.setRange(10, 500)
        self.limit_input.setValue(50)
        self.limit_input.setSingleStep(10)
        search_form.addRow("Result Limit:", self.limit_input)
        
        # Output directory
        output_layout = QHBoxLayout()
        self.output_dir_input = QLineEdit()
        self.output_dir_input.setPlaceholderText("Default output directory")
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(lambda: self.browse_directory(self.output_dir_input))
        output_layout.addWidget(self.output_dir_input, 1)
        output_layout.addWidget(browse_button)
        search_form.addRow("Output:", output_layout)
        
        # Search button
        self.search_button = QPushButton("Search & Download")
        self.search_button.setObjectName("searchButton")
        self.search_button.clicked.connect(self.handle_global_search)
        self.search_button.setMinimumHeight(35)  # Make button taller
        self.search_button.setStyleSheet("font-weight: bold; font-size: 14px;")  # Make text bold and larger
        
        # Progress indicators
        self.global_progress = QProgressBar()
        self.global_progress.setRange(0, 100)
        self.global_progress.setValue(0)
        
        self.global_status = QLabel("Ready to search")
        
        # Add a visible button container
        button_container = QHBoxLayout()
        button_container.addStretch(1)  # Push button to the right
        button_container.addWidget(self.search_button)
        
        # Add form to layout
        global_search_layout.addLayout(search_form)
        global_search_layout.addLayout(button_container)  # Add the button container
        global_search_layout.addWidget(self.global_progress)
        global_search_layout.addWidget(self.global_status)
        
        # Add all components to main layout
        layout.addWidget(auth_group)
        layout.addWidget(single_post_group)
        layout.addWidget(global_search_group)
        layout.addStretch(1)
    
    def setup_queue_history_tab(self):
        """Set up the Queue and History tab"""
        layout = QVBoxLayout(self.queue_history_tab)
        
        # Create subtabs for Queue and History
        subtabs = QTabWidget()
        
        # Queue tab
        queue_tab = QWidget()
        queue_layout = QVBoxLayout(queue_tab)
        
        # Queue filter controls
        queue_filter_layout = QHBoxLayout()
        queue_filter_label = QLabel("Filter:")
        queue_filter_combo = QComboBox()
        queue_filter_combo.addItems(["All", "Images", "Videos", "GIFs", "Articles"])
        queue_filter_layout.addWidget(queue_filter_label)
        queue_filter_layout.addWidget(queue_filter_combo)
        queue_filter_layout.addStretch(1)
        
        # Queue table
        self.queue_table = QTableWidget(0, 5)
        self.queue_table.setHorizontalHeaderLabels(["Title", "Type", "Progress", "Status", "Actions"])
        self.queue_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.queue_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.queue_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.queue_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.queue_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        # Add to layout
        queue_layout.addLayout(queue_filter_layout)
        queue_layout.addWidget(self.queue_table)
        
        # History tab
        history_tab = QWidget()
        history_layout = QVBoxLayout(history_tab)
        
        # History filter controls
        history_filter_layout = QHBoxLayout()
        
        media_filter_label = QLabel("Media Type:")
        media_filter_combo = QComboBox()
        media_filter_combo.addItems(["All", "Images", "Videos", "GIFs", "Articles"])
        
        date_range_label = QLabel("Date Range:")
        date_from = QDateEdit(QDate.currentDate().addDays(-7))
        date_to = QDateEdit(QDate.currentDate())
        date_from.setCalendarPopup(True)
        date_to.setCalendarPopup(True)
        
        history_filter_layout.addWidget(media_filter_label)
        history_filter_layout.addWidget(media_filter_combo)
        history_filter_layout.addSpacing(20)
        history_filter_layout.addWidget(date_range_label)
        history_filter_layout.addWidget(date_from)
        history_filter_layout.addWidget(QLabel("to"))
        history_filter_layout.addWidget(date_to)
        history_filter_layout.addStretch(1)
        
        # History table
        self.history_table = QTableWidget(0, 5)
        self.history_table.setHorizontalHeaderLabels(["Title", "Type", "Date", "Status", "Actions"])
        self.history_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.history_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        # Clear history button
        clear_history_button = QPushButton("Clear History")
        clear_history_button.clicked.connect(self.clear_history)
        
        # Add to layout
        history_layout.addLayout(history_filter_layout)
        history_layout.addWidget(self.history_table)
        history_layout.addWidget(clear_history_button, 0, Qt.AlignRight)
        
        # Add tabs to subtabs
        subtabs.addTab(queue_tab, "Queue")
        subtabs.addTab(history_tab, "History")
        
        # Add subtabs to main layout
        layout.addWidget(subtabs)
    
    def setup_settings_tab(self):
        """Set up the Settings tab"""
        layout = QVBoxLayout(self.settings_tab)
        
        # Reddit API settings section
        reddit_settings_group = QGroupBox("Reddit API Settings")
        reddit_settings_layout = QFormLayout(reddit_settings_group)
        
        # Client ID input
        self.client_id_input = QLineEdit()
        self.client_id_input.setPlaceholderText("Enter your Reddit API Client ID")
        reddit_settings_layout.addRow("Client ID:", self.client_id_input)
        
        # Client Secret input
        self.client_secret_input = QLineEdit()
        self.client_secret_input.setPlaceholderText("Enter your Reddit API Client Secret")
        self.client_secret_input.setEchoMode(QLineEdit.EchoMode.Password)
        reddit_settings_layout.addRow("Client Secret:", self.client_secret_input)
        
        # Redirect URI input
        self.redirect_uri_input = QLineEdit()
        self.redirect_uri_input.setPlaceholderText("Enter your Redirect URI (optional)")
        reddit_settings_layout.addRow("Redirect URI:", self.redirect_uri_input)
        
        # Test & Save button
        reddit_save_button = QPushButton("Test & Save")
        reddit_save_button.setObjectName("primaryButton")
        reddit_save_button.clicked.connect(self.save_reddit_credentials)
        reddit_settings_layout.addRow("", reddit_save_button)
        
        # Download settings section
        download_settings_group = QGroupBox("Download Settings")
        download_settings_layout = QFormLayout(download_settings_group)
        
        # Default download directory
        dir_layout = QHBoxLayout()
        self.download_dir_input = QLineEdit()
        self.download_dir_input.setPlaceholderText("Select default download directory")
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(lambda: self.browse_directory(self.download_dir_input, True))
        dir_layout.addWidget(self.download_dir_input)
        dir_layout.addWidget(browse_button)
        download_settings_layout.addRow("Default Directory:", dir_layout)
        
        # Rate limit slider
        rate_limit_layout = QHBoxLayout()
        self.rate_limit_slider = QSlider(Qt.Horizontal)
        self.rate_limit_slider.setRange(1, 10)
        self.rate_limit_slider.setValue(5)
        self.rate_limit_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.rate_limit_slider.setTickInterval(1)
        self.rate_limit_value = QLabel("5")
        self.rate_limit_slider.valueChanged.connect(lambda v: self.rate_limit_value.setText(str(v)))
        rate_limit_layout.addWidget(self.rate_limit_slider)
        rate_limit_layout.addWidget(self.rate_limit_value)
        download_settings_layout.addRow("Rate Limit:", rate_limit_layout)
        
        # Save button
        download_save_button = QPushButton("Save Settings")
        download_save_button.clicked.connect(self.save_download_settings)
        download_settings_layout.addRow("", download_save_button)
        
        # Theme settings section
        theme_settings_group = QGroupBox("Theme Settings")
        theme_settings_layout = QVBoxLayout(theme_settings_group)
        
        # Theme options
        theme_radio_layout = QHBoxLayout()
        self.light_theme_radio = QRadioButton("Light")
        self.dark_theme_radio = QRadioButton("Dark")
        self.light_theme_radio.setChecked(True)  # Default to light theme
        
        # Connect signals
        self.light_theme_radio.toggled.connect(lambda checked: self.set_theme('light') if checked else None)
        self.dark_theme_radio.toggled.connect(lambda checked: self.set_theme('dark') if checked else None)
        
        theme_radio_layout.addWidget(self.light_theme_radio)
        theme_radio_layout.addWidget(self.dark_theme_radio)
        theme_radio_layout.addStretch(1)
        
        # Preview section
        theme_preview = QLabel("Theme Preview")
        theme_preview.setAlignment(Qt.AlignCenter)
        theme_preview.setFont(QFont(app_theme.FONT_FAMILY, app_theme.FONT_SIZE_LARGE))
        
        # Add to layout
        theme_settings_layout.addLayout(theme_radio_layout)
        theme_settings_layout.addWidget(theme_preview)
        
        # Add all sections to main layout
        layout.addWidget(reddit_settings_group)
        layout.addWidget(download_settings_group)
        layout.addWidget(theme_settings_group)
        layout.addStretch(1)
    
    def set_theme(self, theme_name):
        """Set the application theme"""
        self.current_theme = theme_name
        
        # Determine if we should use dark mode
        use_dark_mode = theme_name == 'dark'
        
        # Apply the theme
        app.setStyleSheet(app_theme.get_style_sheet(use_dark_mode))
        
        # Update radio buttons if needed
        if hasattr(self, 'light_theme_radio') and self.light_theme_radio is not None:
            self.light_theme_radio.setChecked(not use_dark_mode)
        if hasattr(self, 'dark_theme_radio') and self.dark_theme_radio is not None:
            self.dark_theme_radio.setChecked(use_dark_mode)
        
        # Emit theme changed signal
        self.theme_changed_signal.emit(use_dark_mode)
    
    def browse_directory(self, line_edit_widget, is_default_setting=False):
        """Open a file dialog to select a directory"""
        current_dir = line_edit_widget.text() or os.path.expanduser("~")
        new_dir = QFileDialog.getExistingDirectory(self, "Select Directory", current_dir)
        
        if new_dir:  # User selected a directory
            line_edit_widget.setText(new_dir)
            
            # If this is the default download directory, save to settings
            if is_default_setting and hasattr(self, 'backend') and self.backend:
                settings = {"download_dir": new_dir}
                self.backend.save_settings(settings)
                self.statusBar().showMessage(f"Download directory set to: {new_dir}", 3000)
    
    def handle_reddit_connect(self):
        """Connect to Reddit API with credentials"""
        # Get credentials from UI
        client_id = self.client_id_input.text().strip()
        client_secret = self.client_secret_input.text().strip()
        redirect_uri = self.redirect_uri_input.text().strip()
        
        if not client_id or not client_secret:
            QMessageBox.warning(self, "Input Error", "Please enter both Client ID and Client Secret.")
            return
        
        # Try to connect
        self.statusBar().showMessage("Connecting to Reddit API...")
        
        # Connect (mock implementation for now)
        if self.backend:
            success = self.backend.connect_to_reddit(client_id=client_id, client_secret=client_secret)
            
            if success:
                self.reddit_status_label.setText("<font color='green'>Connected</font>")
                self.statusBar().showMessage("Successfully connected to Reddit API.", 3000)
                # Save credentials
                self.save_reddit_credentials()
            else:
                self.reddit_status_label.setText("<font color='red'>Connection Failed</font>")
                self.statusBar().showMessage("Failed to connect to Reddit API.", 3000)
                QMessageBox.critical(self, "Connection Error", "Failed to connect to Reddit API. Please check your credentials.")
    
    def save_reddit_credentials(self):
        """Save Reddit API credentials"""
        if self.backend:
            credentials = {
                "client_id": self.client_id_input.text().strip(),
                "client_secret": self.client_secret_input.text().strip(),
                "redirect_uri": self.redirect_uri_input.text().strip()
            }
            
            self.backend.save_reddit_credentials(credentials)
            self.statusBar().showMessage("Reddit API credentials saved.", 3000)
    
    def save_download_settings(self):
        """Save download settings"""
        if self.backend:
            settings = {
                "download_dir": self.download_dir_input.text().strip(),
                "rate_limit": self.rate_limit_slider.value()
            }
            
            self.backend.save_settings(settings)
            self.statusBar().showMessage("Download settings saved.", 3000)
    
    def handle_single_download(self):
        """Handle download of a single Reddit post"""
        url = self.url_input.text().strip()
        
        if not url:
            QMessageBox.warning(self, "Input Error", "Please enter a Reddit post URL.")
            return
        
        # Make sure we have a reddit instance
        if not self.backend or not self.backend.reddit:
            QMessageBox.warning(self, "Connection Error", "Please connect to Reddit API first.")
            return
            
        try:
            # Show progress
            self.statusBar().showMessage("Fetching post information...")
            
            # Extract submission ID from URL
            if '/comments/' in url:
                post_id = url.split('/comments/')[1].split('/')[0]
            elif 'redd.it/' in url:
                post_id = url.split('redd.it/')[1].split('/')[0]
            else:
                QMessageBox.warning(self, "Invalid URL", "Please enter a valid Reddit post URL.")
                return
                
            # Get submission from reddit
            submission = self.backend.reddit.submission(id=post_id)
            
            # Create download item data
            item_data = {
                "id": submission.id,
                "title": submission.title,
                "url": submission.url,
                "nsfw": submission.over_18,
                "sub": f"r/{submission.subreddit.display_name}",
                "upvotes": f"{submission.score:,}",
                "author": str(submission.author),
                "permalink": submission.permalink
            }
            
            # Determine media type
            if hasattr(submission, "is_video") and submission.is_video:
                item_data["type"] = "Video"
            elif submission.url.endswith((".jpg", ".jpeg", ".png")):
                item_data["type"] = "Image"
            elif submission.url.endswith((".gif", ".gifv")) or "gfycat.com" in submission.url:
                item_data["type"] = "GIF"
            else:
                item_data["type"] = "Article/Link"
            
            # Add to download queue
            download_ids = self.backend.add_to_download_queue([item_data])
            
            if download_ids and len(download_ids) > 0:
                download_id = download_ids[0]
                
                # Add to UI download queue
                self._add_to_download_queue(download_id, item_data)
                
                # Start download worker if not already running
                if not hasattr(self, 'download_worker') or not self.download_worker or not self.download_worker.isRunning():
                    self.download_worker = DownloadWorker(self.backend, download_ids)
                    self.download_worker.progress_updated.connect(self._update_download_progress)
                    self.download_worker.download_completed.connect(self._download_completed)
                    self.download_worker.start()
                else:
                    # Add to existing worker's queue
                    self.download_worker.download_ids.extend(download_ids)
                
                # Show success message
                self.statusBar().showMessage(f"Added '{item_data['title']}' to download queue", 3000)
                
                # Clear URL input
                self.url_input.clear()
            else:
                QMessageBox.warning(self, "Download Error", "Failed to add post to download queue.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            self.statusBar().showMessage("Download failed", 3000)
    
    def _handle_nsfw_toggle(self, state):
        """Handle the Allow NSFW checkbox state change"""
        # Add debug logging
        logging.debug("[UI] Allow NSFW toggle changed to: %s", state == Qt.Checked)
        
        # If Allow NSFW is unchecked, we can't have Only NSFW checked
        if state == Qt.Unchecked and self.only_nsfw_toggle.isChecked():
            logging.debug("[UI] Unchecking Only NSFW due to Allow NSFW being unchecked")
            self.only_nsfw_toggle.blockSignals(True)
            self.only_nsfw_toggle.setChecked(False)
            self.only_nsfw_toggle.blockSignals(False)
    
    def _handle_only_nsfw_toggle(self, state):
        """Handle the Only NSFW checkbox state change"""
        # Add debug logging
        logging.debug("[UI] Only NSFW toggle changed to: %s", state == Qt.Checked)
        
        # One signal controls both checkboxes - ensure Allow NSFW mirrors Only NSFW
        # without emitting secondary signals
        if state == Qt.Checked:
            logging.debug("[UI] Setting Allow NSFW to checked due to Only NSFW being checked")
            self.nsfw_filter_toggle.blockSignals(True)
            self.nsfw_filter_toggle.setChecked(True)
            self.nsfw_filter_toggle.blockSignals(False)
    
    def handle_global_search(self):
        """Handle global search and download"""
        keywords = self.keywords_input.text().strip()
        
        if not keywords:
            QMessageBox.warning(self, "Input Error", "Please enter search keywords.")
            return
        
        # Make sure we have a Reddit instance
        if not self.backend or not self.backend.reddit:
            QMessageBox.warning(self, "Connection Error", "Please connect to Reddit API first.")
            return
        
        # Get search parameters
        media_type = self.media_type_combo.currentText()
        sort_by = self.sort_combo.currentText()
        time_filter_ui = self.time_period_combo.currentText()
        # Map UI time period to API value
        time_filter_map = {
            "All Time": "all",
            "Day": "day",
            "Week": "week",
            "Month": "month",
            "Year": "year"
        }
        time_filter = time_filter_map.get(time_filter_ui, "all")
        
        # Handle NSFW options
        allow_nsfw = self.nsfw_filter_toggle.isChecked()
        only_nsfw = self.only_nsfw_toggle.isChecked()
        
        # Debug logging to verify UI flags
        import logging
        logging.debug("UI-flags  allow:%s  only:%s",
                  self.nsfw_filter_toggle.isChecked(),
                  self.only_nsfw_toggle.isChecked())
        
        limit = self.limit_input.value()
        output_dir = self.output_dir_input.text().strip() or self.download_dir_input.text().strip()
        
        # Update UI to show searching state
        self.global_status.setText("Searching...")
        self.global_progress.setRange(0, 0)  # Show indeterminate progress
        self.search_button.setEnabled(False)
        self.search_button.setText("Searching...")
        
        # Create a dialog to show search results
        self.results_dialog = QDialog(self)
        self.results_dialog.setWindowTitle(f"Search Results for '{keywords}'")
        self.results_dialog.setMinimumSize(800, 600)
        
        # Create layout for results dialog
        dialog_layout = QVBoxLayout(self.results_dialog)
        
        # Create a label to show search stats
        self.results_stats_label = QLabel("Searching...")
        dialog_layout.addWidget(self.results_stats_label)
        
        # Create a table for results
        self.results_table = QTableWidget(0, 6)  # Title, Subreddit, Author, Score, Type, Actions
        self.results_table.setHorizontalHeaderLabels(["Title", "Subreddit", "Author", "Score", "Type", "Actions"])
        self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.results_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.results_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.results_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.results_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        dialog_layout.addWidget(self.results_table)
        
        # Add buttons at the bottom
        buttons_layout = QHBoxLayout()
        self.download_selected_button = QPushButton("Download Selected")
        self.download_selected_button.setEnabled(False)
        self.download_selected_button.clicked.connect(self._download_selected_results)
        
        self.download_all_button = QPushButton("Download All")
        self.download_all_button.setEnabled(False)
        self.download_all_button.clicked.connect(self._download_all_results)
        
        self.close_results_button = QPushButton("Close")
        self.close_results_button.clicked.connect(self.results_dialog.close)
        
        buttons_layout.addWidget(self.download_selected_button)
        buttons_layout.addWidget(self.download_all_button)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.close_results_button)
        dialog_layout.addLayout(buttons_layout)
        
        # Start the search worker
        self.search_worker = SearchWorker(
            self.backend,
            keywords=keywords,
            media_type=media_type,
            sort=sort_by.lower(),
            time_period=time_filter,  # Changed time_filter to time_period
            limit=limit,
            allow_nsfw=allow_nsfw,
            only_nsfw=only_nsfw
        )
        
        # Connect signals
        self.search_worker.results_ready.connect(self._handle_search_results)
        self.search_worker.search_error.connect(self._handle_search_error)
        self.search_worker.search_completed.connect(self._handle_search_completed)
        
        # Start the search
        self.search_worker.start()
        
        # Store output dir for download
        self.search_output_dir = output_dir
        
        # Show the results dialog
        self.results_dialog.exec()
        
    def _handle_search_results(self, results):
        """Handle search results"""
        # Update results table
        self.results_table.setRowCount(0)  # Clear table
        
        # Store results
        self.search_results = results
        
        # Update stats label
        self.results_stats_label.setText(f"Found {len(results)} results")
        
        # Enable buttons if we have results
        self.download_all_button.setEnabled(len(results) > 0)
        
        # Add results to table
        for i, result in enumerate(results):
            self.results_table.insertRow(i)
            
            # Title
            title_item = QTableWidgetItem(result.get('title', 'Unknown'))
            title_item.setToolTip(result.get('title', ''))
            self.results_table.setItem(i, 0, title_item)
            
            # Subreddit
            subreddit_item = QTableWidgetItem(result.get('sub', 'Unknown'))
            self.results_table.setItem(i, 1, subreddit_item)
            
            # Author
            author_item = QTableWidgetItem(result.get('author', 'Unknown'))
            self.results_table.setItem(i, 2, author_item)
            
            # Score
            score_item = QTableWidgetItem(result.get('upvotes', '0'))
            self.results_table.setItem(i, 3, score_item)
            
            # Type
            type_item = QTableWidgetItem(result.get('type', 'Unknown'))
            self.results_table.setItem(i, 4, type_item)
            
            # Actions - Add checkbox for selection and Preview button
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 2, 5, 2)
            
            # Checkbox for selection
            checkbox = QCheckBox()
            checkbox.setObjectName(f"checkbox_{i}")
            checkbox.stateChanged.connect(self._update_selected_count)
            actions_layout.addWidget(checkbox)
            
            # Preview button
            preview_button = QPushButton("Preview")
            preview_button.setObjectName(f"preview_{i}")
            preview_button.clicked.connect(lambda checked, idx=i: self._preview_result(idx))
            actions_layout.addWidget(preview_button)
            
            self.results_table.setCellWidget(i, 5, actions_widget)
        
    def _handle_search_error(self, error_message):
        """Handle search error"""
        # Update UI
        self.global_status.setText(f"Search failed: {error_message}")
        self.global_progress.setRange(0, 100)
        self.global_progress.setValue(0)
        self.search_button.setEnabled(True)
        self.search_button.setText("Search & Download")
        
        # Show error in results dialog
        self.results_stats_label.setText(f"Search failed: {error_message}")
        
        # Close dialog after a delay
        QTimer.singleShot(5000, self.results_dialog.close)
        
    def _handle_search_completed(self):
        """Handle search completion"""
        # Update UI
        self.global_status.setText("Search completed")
        self.global_progress.setRange(0, 100)
        self.global_progress.setValue(100)
        self.search_button.setEnabled(True)
        self.search_button.setText("Search & Download")
        
    def _update_selected_count(self):
        """Update selected count and enable/disable download button"""
        selected_count = 0
        for i in range(self.results_table.rowCount()):
            checkbox = self.results_table.cellWidget(i, 5).findChild(QCheckBox, f"checkbox_{i}")
            if checkbox and checkbox.isChecked():
                selected_count += 1
                
        self.download_selected_button.setEnabled(selected_count > 0)
        self.download_selected_button.setText(f"Download Selected ({selected_count})")
        
    def _preview_result(self, index):
        """Preview a search result"""
        if index < 0 or index >= len(self.search_results):
            return
            
        # Get result data
        result = self.search_results[index]
        
        # Create preview dialog
        preview_dialog = QDialog(self.results_dialog)
        preview_dialog.setWindowTitle(f"Preview: {result.get('title', 'Unknown')}")
        preview_dialog.setMinimumSize(600, 400)
        
        # Create layout
        preview_layout = QVBoxLayout(preview_dialog)
        
        # Add info
        info_layout = QFormLayout()
        info_layout.addRow("Title:", QLabel(result.get('title', 'Unknown')))
        info_layout.addRow("Subreddit:", QLabel(result.get('sub', 'Unknown')))
        info_layout.addRow("Author:", QLabel(result.get('author', 'Unknown')))
        info_layout.addRow("Score:", QLabel(result.get('upvotes', '0')))
        info_layout.addRow("Type:", QLabel(result.get('type', 'Unknown')))
        info_layout.addRow("URL:", QLabel(result.get('url', 'Unknown')))
        
        # Add NSFW warning if needed
        if result.get('nsfw', False):
            nsfw_label = QLabel("WARNING: This content is marked as NSFW")
            nsfw_label.setStyleSheet("color: red; font-weight: bold;")
            info_layout.addRow("", nsfw_label)
            
        preview_layout.addLayout(info_layout)
        
        # Add buttons
        buttons_layout = QHBoxLayout()
        download_button = QPushButton("Download")
        download_button.clicked.connect(lambda: self._download_single_result(index, preview_dialog))
        
        open_button = QPushButton("Open in Browser")
        open_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(result.get('permalink', ''))))
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(preview_dialog.close)
        
        buttons_layout.addWidget(download_button)
        buttons_layout.addWidget(open_button)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(close_button)
        preview_layout.addLayout(buttons_layout)
        
        # Show dialog
        preview_dialog.exec()
        
    def _download_single_result(self, index, dialog=None):
        """Download a single search result"""
        if index < 0 or index >= len(self.search_results):
            return
            
        # Get result data
        result = self.search_results[index]
        
        # Add to download queue
        download_ids = self.backend.add_to_download_queue([result])
        
        if download_ids and len(download_ids) > 0:
            # Add to UI queue
            for download_id in download_ids:
                self._add_to_download_queue(download_id, result)
                
            # Start download worker if not already running
            if not hasattr(self, 'download_worker') or not self.download_worker or not self.download_worker.isRunning():
                self.download_worker = DownloadWorker(self.backend, download_ids)
                self.download_worker.progress_updated.connect(self._update_download_progress)
                self.download_worker.download_completed.connect(self._download_completed)
                self.download_worker.start()
            else:
                # Add to existing worker's queue
                self.download_worker.download_ids.extend(download_ids)
                
            # Show success message
            self.statusBar().showMessage(f"Added '{result.get('title', 'Unknown')}' to download queue", 3000)
            
            # Close dialog if provided
            if dialog:
                dialog.close()
                
            # Switch to queue tab
            self.main_tabs.setCurrentIndex(1)
        else:
            QMessageBox.warning(self, "Download Error", "Failed to add post to download queue.")
            
    def _download_selected_results(self):
        """Download selected search results"""
        selected_indices = []
        for i in range(self.results_table.rowCount()):
            checkbox = self.results_table.cellWidget(i, 5).findChild(QCheckBox, f"checkbox_{i}")
            if checkbox and checkbox.isChecked():
                selected_indices.append(i)
                
        if not selected_indices:
            return
            
        # Get selected results
        selected_results = [self.search_results[i] for i in selected_indices]
        
        # Add all to download queue
        download_ids = self.backend.add_to_download_queue(selected_results)
        
        if download_ids and len(download_ids) > 0:
            # Add to UI queue
            for i, download_id in enumerate(download_ids):
                self._add_to_download_queue(download_id, selected_results[i])
                
            # Start download worker if not already running
            if not hasattr(self, 'download_worker') or not self.download_worker or not self.download_worker.isRunning():
                self.download_worker = DownloadWorker(self.backend, download_ids)
                self.download_worker.progress_updated.connect(self._update_download_progress)
                self.download_worker.download_completed.connect(self._download_completed)
                self.download_worker.start()
            else:
                # Add to existing worker's queue
                self.download_worker.download_ids.extend(download_ids)
                
            # Show success message
            self.statusBar().showMessage(f"Added {len(download_ids)} items to download queue", 3000)
            
            # Close results dialog
            self.results_dialog.close()
            
            # Switch to queue tab
            self.main_tabs.setCurrentIndex(1)
        else:
            QMessageBox.warning(self, "Download Error", "Failed to add posts to download queue.")
            
    def _download_all_results(self):
        """Download all search results"""
        if not self.search_results:
            return
            
        # Add all to download queue
        download_ids = self.backend.add_to_download_queue(self.search_results)
        
        if download_ids and len(download_ids) > 0:
            # Add to UI queue
            for i, download_id in enumerate(download_ids):
                self._add_to_download_queue(download_id, self.search_results[i])
                
            # Start download worker if not already running
            if not hasattr(self, 'download_worker') or not self.download_worker or not self.download_worker.isRunning():
                self.download_worker = DownloadWorker(self.backend, download_ids)
                self.download_worker.progress_updated.connect(self._update_download_progress)
                self.download_worker.download_completed.connect(self._download_completed)
                self.download_worker.start()
            else:
                # Add to existing worker's queue
                self.download_worker.download_ids.extend(download_ids)
                
            # Show success message
            self.statusBar().showMessage(f"Added {len(download_ids)} items to download queue", 3000)
            
            # Close results dialog
            self.results_dialog.close()
            
            # Switch to queue tab
            self.main_tabs.setCurrentIndex(1)
        else:
            QMessageBox.warning(self, "Download Error", "Failed to add posts to download queue.")
    
    def clear_history(self):
        """Clear download history"""
        # Ask for confirmation
        reply = QMessageBox.question(self, "Confirm Clear", "Are you sure you want to clear all download history?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            # Clear history table
            self.history_table.setRowCount(0)
            
            # Clear history in backend
            if self.backend:
                self.backend.clear_history()
            
            self.statusBar().showMessage("Download history cleared.", 3000)
    
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
    
    def _add_to_download_queue(self, download_id, item_data):
        """Add an item to the download queue UI"""
        if not hasattr(self, 'queue_table'):
            return
            
        # Add to our tracking dictionary
        self.download_items[download_id] = item_data
        
        # Get current row count
        row = self.queue_table.rowCount()
        self.queue_table.insertRow(row)
        
        # Title column
        title_item = QTableWidgetItem(item_data.get('title', 'Unknown'))
        title_item.setToolTip(item_data.get('title', ''))
        self.queue_table.setItem(row, 0, title_item)
        
        # Type column
        type_item = QTableWidgetItem(item_data.get('type', 'Unknown'))
        self.queue_table.setItem(row, 1, type_item)
        
        # Progress column with progress bar
        progress_widget = QWidget()
        progress_layout = QVBoxLayout(progress_widget)
        progress_layout.setContentsMargins(5, 2, 5, 2)
        progress_bar = QProgressBar()
        progress_bar.setRange(0, 100)
        progress_bar.setValue(0)
        progress_bar.setObjectName(f"progress_{download_id}")
        progress_layout.addWidget(progress_bar)
        self.queue_table.setCellWidget(row, 2, progress_widget)
        
        # Status column
        status_item = QTableWidgetItem("Queued")
        status_item.setObjectName(f"status_{download_id}")
        self.queue_table.setItem(row, 3, status_item)
        
        # Actions column with cancel button
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(5, 2, 5, 2)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setObjectName(f"cancel_{download_id}")
        cancel_button.clicked.connect(lambda: self._cancel_download(download_id))
        actions_layout.addWidget(cancel_button)
        
        self.queue_table.setCellWidget(row, 4, actions_widget)
        
        # Make sure the Queue & History tab is visible
        self.main_tabs.setCurrentIndex(1)
        
        # Return to the first tab
        self.statusBar().showMessage(f"Added '{item_data.get('title', 'Unknown')}' to download queue", 3000)
    
    def _update_download_progress(self, download_id, progress, status):
        """Update the progress of a download in the UI"""
        if not hasattr(self, 'queue_table'):
            return
            
        # Find the row with this download ID
        for row in range(self.queue_table.rowCount()):
            progress_bar = self.queue_table.cellWidget(row, 2).findChild(QProgressBar, f"progress_{download_id}")
            if progress_bar:
                # Update progress bar
                progress_bar.setValue(progress)
                
                # Update status text
                status_item = self.queue_table.item(row, 3)
                if status_item:
                    status_item.setText(status)
                break
    
    def _download_completed(self, download_id, success, message):
        """Handle download completion"""
        if not hasattr(self, 'queue_table') or not hasattr(self, 'history_table'):
            return
            
        # Find the item in our tracking dictionary
        item_data = self.download_items.get(download_id)
        if not item_data:
            return
            
        # Find the row in the queue table
        queue_row = -1
        for row in range(self.queue_table.rowCount()):
            progress_bar = self.queue_table.cellWidget(row, 2).findChild(QProgressBar, f"progress_{download_id}")
            if progress_bar:
                queue_row = row
                break
                
        if queue_row >= 0:
            # Update progress bar to 100% if successful
            if success:
                progress_bar = self.queue_table.cellWidget(queue_row, 2).findChild(QProgressBar, f"progress_{download_id}")
                if progress_bar:
                    progress_bar.setValue(100)
                    
            # Update status text
            status_item = self.queue_table.item(queue_row, 3)
            if status_item:
                status_text = "Completed" if success else "Failed"
                status_item.setText(status_text)
                
            # Remove from queue after a delay
            QTimer.singleShot(3000, lambda: self._remove_from_queue(queue_row))
            
        # Add to history
        self._add_to_history(item_data, success)
        
        # Show notification
        self.statusBar().showMessage(message, 3000)
        
        # Clean up tracking dictionary
        if download_id in self.download_items:
            del self.download_items[download_id]
    
    def _remove_from_queue(self, row):
        """Remove an item from the queue table"""
        if hasattr(self, 'queue_table') and 0 <= row < self.queue_table.rowCount():
            self.queue_table.removeRow(row)
    
    def _add_to_history(self, item_data, success):
        """Add an item to the history table"""
        if not hasattr(self, 'history_table'):
            return
            
        # Get current row count
        row = self.history_table.rowCount()
        self.history_table.insertRow(row)
        
        # Title column
        title_item = QTableWidgetItem(item_data.get('title', 'Unknown'))
        title_item.setToolTip(item_data.get('title', ''))
        self.history_table.setItem(row, 0, title_item)
        
        # Type column
        type_item = QTableWidgetItem(item_data.get('type', 'Unknown'))
        self.history_table.setItem(row, 1, type_item)
        
        # Date column
        date_item = QTableWidgetItem(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.history_table.setItem(row, 2, date_item)
        
        # Status column
        status_text = "Completed" if success else "Failed"
        status_item = QTableWidgetItem(status_text)
        self.history_table.setItem(row, 3, status_item)
        
        # Actions column with open folder button
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(5, 2, 5, 2)
        
        if success:
            folder_button = QPushButton("Open Folder")
            output_dir = item_data.get('output_dir', '')
            if output_dir:
                folder_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(str(output_dir))))
                actions_layout.addWidget(folder_button)
        
        self.history_table.setCellWidget(row, 4, actions_widget)
        
    def _cancel_download(self, download_id):
        """Cancel a download"""
        if self.backend:
            success = self.backend.cancel_download(download_id)
            
            if success:
                self.statusBar().showMessage("Download cancelled.", 3000)
                
                # Update UI
                for row in range(self.queue_table.rowCount()):
                    progress_bar = self.queue_table.cellWidget(row, 2).findChild(QProgressBar, f"progress_{download_id}")
                    if progress_bar:
                        status_item = self.queue_table.item(row, 3)
                        if status_item:
                            status_item.setText("Cancelled")
                        break

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