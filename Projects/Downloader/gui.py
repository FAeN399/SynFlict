"""
Reddit Grabber GUI
Run this file to launch the graphical interface for the Reddit Grabber application.
"""
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QTabWidget, QLabel, QLineEdit, QPushButton, QCheckBox, QProgressBar,
    QListWidget, QTableWidget, QTableWidgetItem, QGroupBox, QComboBox,
    QTextEdit, QFileDialog, QMessageBox, QSpacerItem, QSizePolicy,
    QScrollArea
)
from PySide6.QtCore import Qt, QSize, Signal, QObject, Slot
from PySide6.QtGui import QIcon, QFont

def get_icon(name):
    return QIcon()


class SearchWorker(QObject):
    """Worker object for running Reddit searches in a background thread with Qt signals."""
    
    # Define signals
    progress_updated = Signal(int, int, str)  # current, successful, status_text
    search_complete = Signal(int, int, list)  # total, successful, failed_urls
    search_error = Signal(str)  # error message
    
    def __init__(self, reddit, db, search_params, output_path):
        super().__init__()
        self.reddit = reddit
        self.db = db
        self.search_params = search_params
        self.output_path = output_path
        self.cancelled = False
    
    @Slot()
    def run_search(self):
        """Run the search in a background thread."""
        try:
            from grabber.global_search import GlobalRedditSearch
            
            # Initialize the global search handler
            search_handler = GlobalRedditSearch(self.reddit, self.db)
            
            # Define progress callback that emits a signal
            def update_progress(current, successful, status_text):
                self.progress_updated.emit(current, successful, status_text)
            
            # Perform the search
            search_results = search_handler.search(
                keywords=self.search_params["keywords"],
                media_type=self.search_params["media_type"],
                sort_by=self.search_params["sort_by"],
                time_period=self.search_params["time_period"],
                nsfw=self.search_params["nsfw"],
                limit=self.search_params["limit"]
            )
            
            # Download the results
            total, successful, failed = search_handler.download_search_results(
                search_results,
                self.output_path,
                progress_callback=update_progress
            )
            
            # Emit completion signal
            self.search_complete.emit(total, successful, failed)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.search_error.emit(str(e))

class RedditGrabberApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reddit Grabber")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(QSize(700, 500))
        font = QFont("Inter", 10)
        QApplication.setFont(font)
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.create_download_tab()
        self.create_queue_history_tab()
        self.create_settings_tab()
        self.statusBar().showMessage("Ready")

    def create_download_tab(self):
        tab_download = QWidget()
        layout = QVBoxLayout(tab_download)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        auth_group = QGroupBox("Reddit Authentication")
        auth_layout = QHBoxLayout()
        self.login_button = QPushButton("[icon] Login with Reddit")
        self.login_button.setIcon(get_icon("reddit_login"))
        self.login_button.clicked.connect(self.handle_login)
        self.auth_status_label = QLabel("Status: Not Logged In")
        self.auth_status_label.setStyleSheet("font-weight: bold;")
        auth_layout.addWidget(self.login_button)
        auth_layout.addWidget(self.auth_status_label)
        auth_layout.addStretch()
        auth_group.setLayout(auth_layout)
        layout.addWidget(auth_group)
        
        # --- Global Reddit Search ---
        global_search_group = QGroupBox("Global Reddit Search")
        global_search_layout = QGridLayout()
        
        global_search_layout.addWidget(QLabel("Search Keywords:"), 0, 0)
        self.search_keywords_input = QLineEdit()
        self.search_keywords_input.setPlaceholderText("Enter search terms (e.g., cats, landscape, etc.)")
        global_search_layout.addWidget(self.search_keywords_input, 0, 1, 1, 3)
        
        global_search_layout.addWidget(QLabel("Media Type:"), 1, 0)
        self.search_media_type = QComboBox()
        self.search_media_type.addItems(["All", "Images", "Videos", "GIFs", "Articles"])
        global_search_layout.addWidget(self.search_media_type, 1, 1)
        
        global_search_layout.addWidget(QLabel("Sort By:"), 1, 2)
        self.search_sort_by = QComboBox()
        self.search_sort_by.addItems(["Relevance", "Hot", "New", "Top", "Comments"])
        global_search_layout.addWidget(self.search_sort_by, 1, 3)
        
        global_search_layout.addWidget(QLabel("Time Period:"), 2, 0)
        self.search_time_period = QComboBox()
        self.search_time_period.addItems(["All Time", "Past Hour", "Past 24 Hours", "Past Week", "Past Month", "Past Year"])
        global_search_layout.addWidget(self.search_time_period, 2, 1)
        
        self.search_nsfw_toggle = QCheckBox("Include NSFW Content")
        global_search_layout.addWidget(self.search_nsfw_toggle, 2, 2, 1, 2)
        
        global_search_layout.addWidget(QLabel("Limit Results:"), 3, 0)
        self.search_limit_input = QLineEdit("100")
        global_search_layout.addWidget(self.search_limit_input, 3, 1)
        
        global_search_layout.addWidget(QLabel("Output Directory:"), 3, 2)
        self.search_output_dir_input = QLineEdit()
        self.search_output_dir_input.setPlaceholderText("Leave blank for default")
        self.search_output_dir_input.setReadOnly(True)
        global_search_layout.addWidget(self.search_output_dir_input, 3, 3)
        
        search_actions_layout = QHBoxLayout()
        self.search_browse_button = QPushButton("[icon] Browse...")
        self.search_browse_button.clicked.connect(lambda: self.browse_directory(self.search_output_dir_input))
        search_actions_layout.addWidget(self.search_browse_button)
        
        self.search_button = QPushButton("[icon] Search & Download")
        self.search_button.setIcon(get_icon("search"))
        self.search_button.setStyleSheet("padding: 8px; background-color: #9C27B0; color: white; border-radius: 5px;")
        
        # Add a direct action for testing button clicks
        def on_search_click():
            print("DEBUG: Search button clicked directly")
            self.search_status_label.setText("Button clicked!")
            self.handle_global_search()
            
        self.search_button.clicked.connect(on_search_click)
        search_actions_layout.addWidget(self.search_button)
        global_search_layout.addLayout(search_actions_layout, 4, 0, 1, 4)
        
        self.search_progress_bar = QProgressBar()
        self.search_progress_bar.setVisible(False)
        global_search_layout.addWidget(self.search_progress_bar, 5, 0, 1, 4)
        
        self.search_status_label = QLabel("")
        self.search_status_label.setAlignment(Qt.AlignCenter)
        global_search_layout.addWidget(self.search_status_label, 6, 0, 1, 4)
        
        global_search_group.setLayout(global_search_layout)
        layout.addWidget(global_search_group)
        
        # --- Single Post Download ---
        single_post_group = QGroupBox("Single Post Download")
        single_post_layout = QGridLayout()

        single_post_layout.addWidget(QLabel("Post URL:"), 0, 0)
        self.post_url_input = QLineEdit()
        self.post_url_input.setPlaceholderText("Enter Reddit post URL (e.g., https://www.reddit.com/r/...)")
        single_post_layout.addWidget(self.post_url_input, 0, 1, 1, 2)

        self.single_download_button = QPushButton("[icon] Download")
        self.single_download_button.clicked.connect(self.handle_single_download)
        single_post_layout.addWidget(self.single_download_button, 0, 3)

        single_post_layout.addWidget(QLabel("Output Directory:"), 1, 0)
        self.single_output_dir_input = QLineEdit()
        self.single_output_dir_input.setPlaceholderText("Leave blank for default")
        self.single_output_dir_input.setReadOnly(True)
        single_post_layout.addWidget(self.single_output_dir_input, 1, 1, 1, 2)

        self.single_browse_button = QPushButton("[icon] Browse...")
        self.single_browse_button.clicked.connect(lambda: self.browse_directory(self.single_output_dir_input))
        single_post_layout.addWidget(self.single_browse_button, 1, 3)

        self.single_status_label = QLabel("Ready")
        single_post_layout.addWidget(self.single_status_label, 2, 0, 1, 3)

        self.single_progress_bar = QProgressBar()
        self.single_progress_bar.setVisible(False)
        single_post_layout.addWidget(self.single_progress_bar, 3, 0, 1, 4)

        self.single_status_label.setAlignment(Qt.AlignCenter)
        single_post_layout.addWidget(self.single_status_label, 5, 0, 1, 3)
        single_post_group.setLayout(single_post_layout)
        layout.addWidget(single_post_group)
        
        # --- Subreddit Media Downloader ---
        subreddit_group = QGroupBox("Subreddit Media Downloader")
        subreddit_layout = QGridLayout()
        
        # Subreddit name input
        subreddit_layout.addWidget(QLabel("Subreddit:"), 0, 0)
        self.subreddit_input = QLineEdit()
        self.subreddit_input.setPlaceholderText("Enter subreddit name (without r/)") 
        subreddit_layout.addWidget(self.subreddit_input, 0, 1, 1, 3)
        
        # Sort options
        subreddit_layout.addWidget(QLabel("Sort By:"), 1, 0)
        self.subreddit_sort = QComboBox()
        self.subreddit_sort.addItems(["Hot", "New", "Top", "Rising", "Controversial"])
        subreddit_layout.addWidget(self.subreddit_sort, 1, 1)
        
        # Time filter (for Top and Controversial)
        subreddit_layout.addWidget(QLabel("Time Filter:"), 1, 2)
        self.subreddit_time_filter = QComboBox()
        self.subreddit_time_filter.addItems(["All", "Hour", "Day", "Week", "Month", "Year"])
        subreddit_layout.addWidget(self.subreddit_time_filter, 1, 3)
        
        # Media type filter
        subreddit_layout.addWidget(QLabel("Media Type:"), 2, 0)
        self.subreddit_media_type = QComboBox()
        self.subreddit_media_type.addItems(["All", "Images", "Videos", "GIFs", "Articles"])
        subreddit_layout.addWidget(self.subreddit_media_type, 2, 1)
        
        # Limit posts
        subreddit_layout.addWidget(QLabel("Limit:"), 2, 2)
        self.subreddit_limit = QLineEdit("25")
        subreddit_layout.addWidget(self.subreddit_limit, 2, 3)
        
        # NSFW option
        self.subreddit_nsfw = QCheckBox("Include NSFW Content")
        subreddit_layout.addWidget(self.subreddit_nsfw, 3, 0, 1, 2)
        
        # Output directory
        subreddit_layout.addWidget(QLabel("Output Directory:"), 4, 0)
        self.subreddit_output_dir = QLineEdit()
        self.subreddit_output_dir.setPlaceholderText("Leave blank for default")
        self.subreddit_output_dir.setReadOnly(True)
        subreddit_layout.addWidget(self.subreddit_output_dir, 4, 1, 1, 2)
        
        self.subreddit_browse_button = QPushButton("[icon] Browse...")
        self.subreddit_browse_button.clicked.connect(lambda: self.browse_directory(self.subreddit_output_dir))
        subreddit_layout.addWidget(self.subreddit_browse_button, 4, 3)
        
        # Download button
        self.subreddit_download_button = QPushButton("[icon] Download from Subreddit")
        self.subreddit_download_button.setStyleSheet("padding: 8px; background-color: #2196F3; color: white; border-radius: 5px;")
        self.subreddit_download_button.clicked.connect(self.handle_subreddit_download)
        subreddit_layout.addWidget(self.subreddit_download_button, 5, 0, 1, 4)
        
        # Status and progress
        self.subreddit_status_label = QLabel("Ready")
        subreddit_layout.addWidget(self.subreddit_status_label, 6, 0, 1, 4)
        
        self.subreddit_progress_bar = QProgressBar()
        self.subreddit_progress_bar.setVisible(False)
        subreddit_layout.addWidget(self.subreddit_progress_bar, 7, 0, 1, 4)
        
        subreddit_group.setLayout(subreddit_layout)
        layout.addWidget(subreddit_group)
        
        subreddit_sync_group = QGroupBox("Subreddit Sync")
        subreddit_sync_layout = QGridLayout()
        subreddit_sync_layout.addWidget(QLabel("Subreddit Name:"), 0, 0)
        self.subreddit_name_input = QLineEdit()
        self.subreddit_name_input.setPlaceholderText("e.g., pics, wallpapers (without r/)")
        subreddit_sync_layout.addWidget(self.subreddit_name_input, 0, 1, 1, 2)
        self.filters_button = QPushButton("[icon] Show Sync Filters")
        self.filters_button.setCheckable(True)
        self.filters_button.clicked.connect(self.toggle_filters_visibility)
        subreddit_sync_layout.addWidget(self.filters_button, 1, 0, 1, 3)
        self.filters_group = QGroupBox("Filters")
        filters_layout = QGridLayout(self.filters_group)
        filters_layout.addWidget(QLabel("Search Query:"), 0, 0)
        self.filter_query_input = QLineEdit()
        filters_layout.addWidget(self.filter_query_input, 0, 1)
        filters_layout.addWidget(QLabel("Flair:"), 1, 0)
        self.filter_flair_input = QLineEdit()
        filters_layout.addWidget(self.filter_flair_input, 1, 1)
        filters_layout.addWidget(QLabel("Min Score:"), 2, 0)
        self.filter_min_score_input = QLineEdit()
        self.filter_min_score_input.setPlaceholderText("e.g., 100")
        filters_layout.addWidget(self.filter_min_score_input, 2, 1)
        filters_layout.addWidget(QLabel("Date Range:"), 3, 0)
        self.filter_date_range_start = QLineEdit("YYYY-MM-DD")
        self.filter_date_range_end = QLineEdit("YYYY-MM-DD")
        date_range_layout = QHBoxLayout()
        date_range_layout.addWidget(self.filter_date_range_start)
        date_range_layout.addWidget(QLabel("to"))
        date_range_layout.addWidget(self.filter_date_range_end)
        filters_layout.addLayout(date_range_layout, 3, 1)
        filters_layout.addWidget(QLabel("User:"), 4, 0)
        self.filter_user_input = QLineEdit()
        self.filter_user_input.setPlaceholderText("e.g., specific_username")
        filters_layout.addWidget(self.filter_user_input, 4, 1)
        filters_layout.addWidget(QLabel("Media Type:"), 5, 0)
        self.filter_media_type_combo = QComboBox()
        self.filter_media_type_combo.addItems(["All", "Image", "Video", "GIF"])
        filters_layout.addWidget(self.filter_media_type_combo, 5, 1)
        self.filter_nsfw_toggle = QCheckBox("Include NSFW")
        filters_layout.addWidget(self.filter_nsfw_toggle, 6, 0, 1, 2)
        self.filters_group.setVisible(False)
        subreddit_sync_layout.addWidget(self.filters_group, 2, 0, 1, 3)
        subreddit_sync_layout.addWidget(QLabel("Limit Posts (0 for all):"), 3, 0)
        self.limit_posts_input = QLineEdit("100")
        subreddit_sync_layout.addWidget(self.limit_posts_input, 3, 1, 1, 2)
        subreddit_sync_layout.addWidget(QLabel("Output Directory:"), 4, 0)
        self.sync_output_dir_input = QLineEdit()
        self.sync_output_dir_input.setPlaceholderText("Leave blank for default")
        self.sync_output_dir_input.setReadOnly(True)
        subreddit_sync_layout.addWidget(self.sync_output_dir_input, 4, 1)
        self.sync_browse_button = QPushButton("[icon] Browse...")
        self.sync_browse_button.clicked.connect(lambda: self.browse_directory(self.sync_output_dir_input))
        subreddit_sync_layout.addWidget(self.sync_browse_button, 4, 2)
        self.sync_button = QPushButton("[icon] Start Subreddit Sync")
        self.sync_button.setIcon(get_icon("sync"))
        self.sync_button.setStyleSheet("padding: 8px; background-color: #2196F3; color: white; border-radius: 5px;")
        self.sync_button.clicked.connect(self.handle_subreddit_sync)
        subreddit_sync_layout.addWidget(self.sync_button, 5, 0, 1, 3)
        self.sync_progress_bar = QProgressBar()
        self.sync_progress_bar.setVisible(False)
        subreddit_sync_layout.addWidget(self.sync_progress_bar, 6, 0, 1, 3)
        self.sync_status_label = QLabel("")
        self.sync_status_label.setAlignment(Qt.AlignCenter)
        subreddit_sync_layout.addWidget(self.sync_status_label, 7, 0, 1, 3)
        subreddit_sync_group.setLayout(subreddit_sync_layout)
        layout.addWidget(subreddit_sync_group)
        layout.addStretch()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(tab_download)
        self.tabs.addTab(scroll_area, "[icon] Download")

    def toggle_filters_visibility(self):
        is_visible = self.filters_group.isVisible()
        self.filters_group.setVisible(not is_visible)
        self.filters_button.setText("[icon] Hide Sync Filters" if not is_visible else "[icon] Show Sync Filters")

    def create_queue_history_tab(self):
        tab_queue_history = QWidget()
        layout = QVBoxLayout(tab_queue_history)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        queue_group = QGroupBox("Current Downloads")
        queue_layout = QVBoxLayout()
        self.queue_table = QTableWidget()
        self.queue_table.setColumnCount(5)
        self.queue_table.setHorizontalHeaderLabels(["Item", "Size", "Progress", "Status", "Action"])
        self.queue_table.horizontalHeader().setStretchLastSection(True)
        self.queue_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.queue_table.setSelectionBehavior(QTableWidget.SelectRows)
        queue_layout.addWidget(self.queue_table)
        open_download_folder_button_queue = QPushButton("[icon] Open Download Folder")
        open_download_folder_button_queue.clicked.connect(self.open_download_folder)
        queue_layout.addWidget(open_download_folder_button_queue, alignment=Qt.AlignRight)
        queue_group.setLayout(queue_layout)
        layout.addWidget(queue_group)
        history_group = QGroupBox("Download History")
        history_layout = QVBoxLayout()
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels(["Item", "Type", "Date", "Status", "Path", "Actions"])
        self.history_table.horizontalHeader().setStretchLastSection(False)
        self.history_table.setColumnWidth(0, 200)
        self.history_table.setColumnWidth(4, 150)
        self.history_table.setColumnWidth(5, 120)
        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.history_table.setSelectionBehavior(QTableWidget.SelectRows)
        history_layout.addWidget(self.history_table)
        history_buttons_layout = QHBoxLayout()
        self.clear_history_button = QPushButton("[icon] Clear History")
        self.clear_history_button.clicked.connect(self.clear_history)
        history_buttons_layout.addWidget(self.clear_history_button)
        history_buttons_layout.addStretch()
        self.refresh_history_button = QPushButton("[icon] Refresh History")
        self.refresh_history_button.clicked.connect(self.load_history)
        history_buttons_layout.addWidget(self.refresh_history_button)
        history_layout.addLayout(history_buttons_layout)
        history_group.setLayout(history_layout)
        layout.addWidget(history_group)
        self.tabs.addTab(tab_queue_history, "[icon] Queue & History")

    def create_settings_tab(self):
        tab_settings = QWidget()
        layout = QVBoxLayout(tab_settings)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        api_group = QGroupBox("Reddit API Credentials")
        api_layout = QGridLayout()
        api_layout.addWidget(QLabel("Client ID:"), 0, 0)
        self.api_client_id_input = QLineEdit()
        api_layout.addWidget(self.api_client_id_input, 0, 1)
        api_layout.addWidget(QLabel("Client Secret:"), 1, 0)
        self.api_client_secret_input = QLineEdit()
        self.api_client_secret_input.setEchoMode(QLineEdit.Password)
        api_layout.addWidget(self.api_client_secret_input, 1, 1)
        self.save_api_creds_button = QPushButton("[icon] Save Credentials")
        self.save_api_creds_button.clicked.connect(self.save_api_credentials)
        api_layout.addWidget(self.save_api_creds_button, 2, 0, 1, 2)
        api_group.setLayout(api_layout)
        layout.addWidget(api_group)
        download_config_group = QGroupBox("Download Configuration")
        download_config_layout = QGridLayout()
        download_config_layout.addWidget(QLabel("Default Output Directory:"), 0, 0)
        self.default_output_dir_input = QLineEdit()
        self.default_output_dir_input.setReadOnly(True)
        download_config_layout.addWidget(self.default_output_dir_input, 0, 1)
        self.browse_default_dir_button = QPushButton("[icon] Browse...")
        self.browse_default_dir_button.clicked.connect(lambda: self.browse_directory(self.default_output_dir_input, True))
        download_config_layout.addWidget(self.browse_default_dir_button, 0, 2)
        self.save_download_config_button = QPushButton("[icon] Save Download Settings")
        self.save_download_config_button.clicked.connect(self.save_download_config)
        download_config_layout.addWidget(self.save_download_config_button, 1, 0, 1, 3)
        download_config_group.setLayout(download_config_layout)
        layout.addWidget(download_config_group)
        app_settings_group = QGroupBox("Application Settings")
        app_settings_layout = QGridLayout()
        app_settings_layout.addWidget(QLabel("Rate Limit (requests/min):"), 0, 0)
        self.rate_limit_input = QLineEdit("60")
        app_settings_layout.addWidget(self.rate_limit_input, 0, 1)
        app_settings_layout.addWidget(QLabel("Theme:"), 1, 0)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light Mode", "Dark Mode"])
        self.theme_combo.currentIndexChanged.connect(self.apply_theme)
        app_settings_layout.addWidget(self.theme_combo, 1, 1)
        self.save_app_settings_button = QPushButton("[icon] Save App Settings")
        self.save_app_settings_button.clicked.connect(self.save_app_settings)
        app_settings_layout.addWidget(self.save_app_settings_button, 2, 0, 1, 2)
        app_settings_group.setLayout(app_settings_layout)
        layout.addWidget(app_settings_group)
        layout.addStretch()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(tab_settings)
        self.tabs.addTab(scroll_area, "[icon] Settings")
        self.load_settings()
    def handle_login(self):
        QMessageBox.information(self, "Login", "Login functionality to be implemented.")
    def handle_logout(self):
        QMessageBox.information(self, "Logout", "Logout functionality to be implemented.")
    def browse_directory(self, line_edit_widget, is_default_setting=False):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            line_edit_widget.setText(directory)
            if is_default_setting:
                if not self.single_output_dir_input.text():
                    self.single_output_dir_input.setText(directory)
                if not self.sync_output_dir_input.text():
                    self.sync_output_dir_input.setText(directory)
    def handle_single_download(self):
        post_url = self.post_url_input.text()
        output_dir = self.single_output_dir_input.text() or self.default_output_dir_input.text()
        if not post_url:
            QMessageBox.warning(self, "Input Error", "Please enter a Reddit post URL.")
            return
        if not output_dir:
            QMessageBox.warning(self, "Configuration Error", "Please set an output directory in Settings or for this download.")
            return
        self.single_status_label.setText(f"Downloading: {post_url} to {output_dir}...")
        self.single_progress_bar.setVisible(True)
        self.single_progress_bar.setRange(0,0)
        print(f"Dry run: {self.dry_run_checkbox.isChecked()}")
    def handle_global_search(self):
        print("DEBUG: handle_global_search method called")
        # Get search parameters from UI
        try:
            import pathlib
            from PySide6.QtCore import QThread
            from grabber.search import get_reddit_client
            from grabber.database import Database
            
            # Get search parameters from UI
            keywords = self.search_keywords_input.text()
            print(f"DEBUG: Keywords entered: '{keywords}'")
            output_dir = self.search_output_dir_input.text() or self.default_output_dir_input.text()
            print(f"DEBUG: Output directory: '{output_dir}'")
            
            # Validate inputs
            if not keywords:
                print("DEBUG: No keywords entered, showing warning")
                QMessageBox.warning(self, "Input Error", "Please enter search keywords.")
                return
            if not output_dir:
                print("DEBUG: No output directory, showing warning")
                QMessageBox.warning(self, "Configuration Error", "Please set an output directory in Settings or for this search.")
                return
            
            # Try to parse the limit as an integer
            try:
                limit = int(self.search_limit_input.text())
                if limit <= 0:
                    limit = 100
            except ValueError:
                limit = 100
                self.search_limit_input.setText(str(limit))
                
            # Collect search parameters
            search_params = {
                "keywords": keywords,
                "media_type": self.search_media_type.currentText(),
                "sort_by": self.search_sort_by.currentText(),
                "time_period": self.search_time_period.currentText(),
                "nsfw": self.search_nsfw_toggle.isChecked(),
                "limit": limit
            }
            
            print(f"DEBUG: Global Reddit search: {search_params} to {output_dir}")
            self.search_status_label.setText(f"Searching Reddit for: {keywords}...")
            self.search_progress_bar.setVisible(True)
            self.search_progress_bar.setValue(0)
            self.search_progress_bar.setRange(0, 100)
            
            # Create path object for output directory
            output_path = pathlib.Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # ... rest of your code ...

    def handle_subreddit_download(self):
        # Get parameters from UI
        subreddit_name = self.subreddit_input.text().strip()
        sort_by = self.subreddit_sort.currentText().lower()
        time_filter = self.subreddit_time_filter.currentText().lower()
        media_type = self.subreddit_media_type.currentText().lower()
        nsfw_allowed = self.subreddit_nsfw.isChecked()
        
        try:
            limit = int(self.subreddit_limit.text())
        except ValueError:
            limit = 25  # Default if invalid
        
        # Output directory - use default if not specified
        output_dir = self.subreddit_output_dir.text() or self.default_output_dir_input.text() or "./downloads"
        
        if not subreddit_name:
            QMessageBox.warning(self, "Input Error", "Please enter a subreddit name.")
            return
        
        # Log parameters for debugging
        print(f"Downloading from r/{subreddit_name} - Sort: {sort_by}, Filter: {time_filter}")
        print(f"Media Type: {media_type}, NSFW: {nsfw_allowed}, Limit: {limit}")
        print(f"Output Directory: {output_dir}")
        
        # Set up progress indicators
        self.subreddit_progress_bar.setVisible(True)
        self.subreddit_progress_bar.setValue(0)
        self.subreddit_status_label.setText(f"Connecting to r/{subreddit_name}...")
        self.subreddit_download_button.setEnabled(False)
        
        try:
            # Import Reddit client and downloader
            from grabber.auth import get_reddit_instance
            from grabber.subreddit_downloader import SubredditDownloader
            from grabber.download_manager import DownloadManager
            
            # Create worker thread
            from PySide6.QtCore import QThread, QObject, Signal, Slot
            
            class SubredditWorker(QObject):
                progress_updated = Signal(int, int, str)  # current, total, status_text
                download_complete = Signal(int, int, list)  # total, successful, failed_urls
                download_error = Signal(str)  # error message
                
                def __init__(self, reddit, subreddit_name, sort_by, time_filter, media_type, limit, nsfw_allowed, output_dir):
                    super().__init__()
                    self.reddit = reddit
                    self.subreddit_name = subreddit_name
                    self.sort_by = sort_by
                    self.time_filter = time_filter
                    self.media_type = media_type
                    self.limit = limit
                    self.nsfw_allowed = nsfw_allowed
                    self.output_dir = output_dir
                
                @Slot()
                def run_download(self):
                    try:
                        # Create download manager
                        download_manager = DownloadManager()
                        
                        # Create subreddit downloader
                        downloader = SubredditDownloader(self.reddit, download_manager)
                        
                        # Define progress callback
                        def progress_callback(current, successful, status_text):
                            self.progress_updated.emit(current, successful, status_text)
                        
                        # Perform the download
                        total, successful, failed = downloader.download_from_subreddit(
                            subreddit_name=self.subreddit_name,
                            sort_by=self.sort_by,
                            time_filter=self.time_filter,
                            media_type=self.media_type,
                            limit=self.limit,
                            nsfw_allowed=self.nsfw_allowed,
                            output_dir=self.output_dir,
                            progress_callback=progress_callback
                        )
                        
                        # Signal completion
                        self.download_complete.emit(total, successful, failed)
                        
                    except Exception as e:
                        import traceback
                        traceback.print_exc()
                        self.download_error.emit(str(e))
            
            # Get authenticated Reddit instance
            reddit = get_reddit_instance(user_auth=True)
            
            # Create and set up worker
            self.subreddit_worker = SubredditWorker(
                reddit, subreddit_name, sort_by, time_filter, 
                media_type, limit, nsfw_allowed, output_dir
            )
            
            # Connect signals
            self.subreddit_worker.progress_updated.connect(
                lambda current, successful, status: self.update_subreddit_progress(current, successful, status)
            )
            self.subreddit_worker.download_complete.connect(
                lambda total, successful, failed: self.handle_subreddit_complete(total, successful, failed)
            )
            self.subreddit_worker.download_error.connect(
                lambda error: self.handle_subreddit_error(error)
            )
            
            # Start worker in a new thread
            self.subreddit_thread = QThread()
            self.subreddit_worker.moveToThread(self.subreddit_thread)
            self.subreddit_thread.started.connect(self.subreddit_worker.run_download)
            self.subreddit_thread.start()
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.subreddit_status_label.setText(f"Error: {str(e)}")
            self.subreddit_progress_bar.setVisible(False)
            self.subreddit_download_button.setEnabled(True)
    
    def update_subreddit_progress(self, current, successful, status_text):
        # Calculate percentage if we know the total
        if current > 0 and self.subreddit_limit.text():
            try:
                total = int(self.subreddit_limit.text())
                percent = min(100, int((current / total) * 100))
                self.subreddit_progress_bar.setValue(percent)
            except ValueError:
                # If limit is invalid, use indeterminate progress
                self.subreddit_progress_bar.setValue(0)
        
        # Update status text
        self.subreddit_status_label.setText(f"{status_text} ({successful} items queued)")
    
    def handle_subreddit_complete(self, total, successful, failed):
        # Enable the download button again
        self.subreddit_download_button.setEnabled(True)
        
        # Show completion message
        self.subreddit_status_label.setText(
            f"Download complete! Processed {total} posts, added {successful} to download queue."
        )
        
        # Stop the thread
        if hasattr(self, 'subreddit_thread') and self.subreddit_thread.isRunning():
            self.subreddit_thread.quit()
            self.subreddit_thread.wait()
        
        # Offer to open the download folder
        reply = QMessageBox.question(
            self, "Download Complete", 
            f"Successfully queued {successful} items for download from r/{self.subreddit_input.text()}. \n\nOpen download folder?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.open_download_folder()
    
    def handle_subreddit_error(self, error_message):
        # Enable the download button again
        self.subreddit_download_button.setEnabled(True)
        
        # Show error message
        self.subreddit_status_label.setText(f"Error: {error_message}")
        self.subreddit_progress_bar.setVisible(False)
        
        # Stop the thread
        if hasattr(self, 'subreddit_thread') and self.subreddit_thread.isRunning():
            self.subreddit_thread.quit()
            self.subreddit_thread.wait()
        
        # Show error dialog
        QMessageBox.critical(self, "Download Error", f"An error occurred during download:\n{error_message}")
    
    def handle_global_search(self):
        print("DEBUG: handle_global_search method called")
        # Get search parameters
        keywords = self.search_keywords_input.text()
        media_type = self.search_media_type.currentText()
        sort_by = self.search_sort_by.currentText()
        time_period = self.search_time_period.currentText()
        nsfw = self.search_nsfw_toggle.isChecked()
        
        try:
            limit = int(self.search_limit_input.text())
        except ValueError:
            limit = 100  # Default if invalid
        
        # Output directory - use default if not specified
        output_dir = self.search_output_dir_input.text() or self.default_output_dir_input.text() or "./downloads"
        
        if not keywords:
            QMessageBox.warning(self, "Input Error", "Please enter search keywords.")
            return
        
        print(f"DEBUG: Keywords entered: '{keywords}'")
        print(f"DEBUG: Output directory: '{output_dir}'")
        
        # Prepare search parameters
        search_params = {
            "keywords": keywords,
            "media_type": media_type,
            "sort_by": sort_by,
            "time_period": time_period,
            "nsfw": nsfw,
            "limit": limit
        }
        
        print(f"DEBUG: Global Reddit search: {search_params} to {output_dir}")
        
        # Set up progress indicators
        self.search_progress_bar.setVisible(True)
        self.search_progress_bar.setValue(0)
        self.search_status_label.setText("Starting search...")
        
        try:
            # Import Reddit client
            from grabber.auth import get_reddit_instance
            from grabber.database import get_database
            
            # Get authenticated Reddit instance
            reddit = get_reddit_instance(user_auth=True)
            db = get_database()
            
            # Create worker thread
            self.search_worker = SearchWorker(reddit, db, search_params, output_dir)
            self.search_worker.progress_updated.connect(self.update_search_progress)
            self.search_worker.search_complete.connect(self.handle_search_complete)
            self.search_worker.search_error.connect(self.handle_search_error)
            
            # Start the worker in a new thread
            from PySide6.QtCore import QThread
            self.search_thread = QThread()
            self.search_worker.moveToThread(self.search_thread)
            self.search_thread.started.connect(self.search_worker.run_search)
            self.search_thread.start()
            
            # Disable search button during search
            self.search_button.setEnabled(False)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.search_status_label.setText(f"Error: {str(e)}")
            self.search_progress_bar.setVisible(False)
            self.search_button.setEnabled(True)
            
            # Show error message
            QMessageBox.critical(
                self,
                "Search Error",
                f"An error occurred while preparing the search:\n{str(e)}"
            )
    
    @Slot(int, int, str)
    def update_search_progress(self, current, successful, status_text):
        """Update the UI with search progress information."""
        try:
            # Calculate progress percentage
            limit = int(self.search_limit_input.text())
            progress_pct = min(int((current / limit) * 100), 100)
            
            # Update progress bar and status label
            self.search_progress_bar.setValue(progress_pct)
            self.search_status_label.setText(status_text)
            
            # Add to queue display if we have downloads
            if successful > 0 and current % 5 == 0:  # Update every 5 items
                self.add_item_to_queue(
                    f"Reddit search: {self.search_keywords_input.text()}",
                    f"{successful}/{current}",
                    progress_pct,
                    "Downloading..."
                )
        except Exception as e:
            print(f"ERROR in update_search_progress: {str(e)}")
    
    @Slot(int, int, list)
    def handle_search_complete(self, total, successful, failed):
        """Handle search completion."""
        try:
            # Update UI with final results
            self.search_progress_bar.setValue(100)
            self.search_status_label.setText(
                f"Downloaded {successful} of {total} submissions. {len(failed)} failed."
            )
            
            # Add to history
            from datetime import datetime
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            output_dir = self.search_output_dir_input.text() or self.default_output_dir_input.text()
            
            self.add_item_to_history(
                f"Search: {self.search_keywords_input.text()}",
                f"{self.search_media_type.currentText()}",
                now,
                f"Completed ({successful}/{total})",
                output_dir
            )
            
            # Clean up thread and worker
            if hasattr(self, 'search_thread') and self.search_thread.isRunning():
                self.search_thread.quit()
                self.search_thread.wait()
            
            # Re-enable the search button
            self.search_button.setEnabled(True)
            
            # Show a completion message
            QMessageBox.information(
                self, 
                "Search Complete", 
                f"Downloaded {successful} of {total} submissions to {output_dir}"
            )
            
        except Exception as e:
            print(f"ERROR in handle_search_complete: {str(e)}")
            self.handle_search_error(str(e))
    
    @Slot(str)
    def handle_search_error(self, error_message):
        """Handle search errors."""
        try:
            # Update UI on error
            self.search_status_label.setText(f"Error: {error_message}")
            
            # Clean up thread and worker
            if hasattr(self, 'search_thread') and self.search_thread.isRunning():
                self.search_thread.quit()
                self.search_thread.wait()
            
            # Re-enable the search button
            self.search_button.setEnabled(True)
            
            # Show error message
            QMessageBox.critical(
                self,
                "Search Error",
                f"An error occurred during the search:\n{error_message}"
            )
            
        except Exception as e:
            print(f"ERROR in handle_search_error: {str(e)}")
            # Last resort error handling
            self.search_button.setEnabled(True)

    def handle_subreddit_sync(self):
        subreddit_name = self.subreddit_name_input.text()
        output_dir = self.sync_output_dir_input.text() or self.default_output_dir_input.text()
        if not subreddit_name:
            QMessageBox.warning(self, "Input Error", "Please enter a subreddit name.")
            return
        if not output_dir:
            QMessageBox.warning(self, "Configuration Error", "Please set an output directory in Settings or for this sync.")
            return
        filters = {
            "query": self.filter_query_input.text(),
            "flair": self.filter_flair_input.text(),
            "min_score": self.filter_min_score_input.text(),
            "date_start": self.filter_date_range_start.text(),
            "date_end": self.filter_date_range_end.text(),
            "user": self.filter_user_input.text(),
            "media_type": self.filter_media_type_combo.currentText(),
            "nsfw": self.filter_nsfw_toggle.isChecked(),
            "limit": self.limit_posts_input.text()
        }
        print(f"Syncing subreddit: {subreddit_name} with filters: {filters} to {output_dir}")
        self.sync_status_label.setText(f"Syncing subreddit: {subreddit_name}...")
        self.sync_progress_bar.setVisible(True)
        self.sync_progress_bar.setRange(0,0)
    def add_item_to_queue(self, item_name, size, progress_val, status_text):
        row_position = self.queue_table.rowCount()
        self.queue_table.insertRow(row_position)
        self.queue_table.setItem(row_position, 0, QTableWidgetItem(item_name))
        self.queue_table.setItem(row_position, 1, QTableWidgetItem(size))
        progress_bar = QProgressBar()
        progress_bar.setValue(progress_val)
        progress_bar.setTextVisible(True)
        self.queue_table.setCellWidget(row_position, 2, progress_bar)
        self.queue_table.setItem(row_position, 3, QTableWidgetItem(status_text))
        cancel_button = QPushButton("Cancel")
        self.queue_table.setCellWidget(row_position, 4, cancel_button)
        self.queue_table.resizeColumnsToContents()
    def add_item_to_history(self, item_name, item_type, date_str, status_str, path_str):
        row_position = self.history_table.rowCount()
        self.history_table.insertRow(row_position)
        self.history_table.setItem(row_position, 0, QTableWidgetItem(item_name))
        self.history_table.setItem(row_position, 1, QTableWidgetItem(item_type))
        self.history_table.setItem(row_position, 2, QTableWidgetItem(date_str))
        status_item = QTableWidgetItem(status_str)
        if status_str == "Completed":
            status_item.setForeground(Qt.darkGreen)
        elif status_str == "Failed":
            status_item.setForeground(Qt.red)
        elif "Incomplete" in status_str or "In Progress" in status_str:
            status_item.setForeground(Qt.darkYellow)
        self.history_table.setItem(row_position, 3, status_item)
        self.history_table.setItem(row_position, 4, QTableWidgetItem(path_str))
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(0,0,0,0)
        actions_layout.setSpacing(5)
        if "Incomplete" in status_str or "Failed" in status_str:
            resume_button = QPushButton("Retry")
            resume_button.setToolTip("Retry/Resume this download")
            actions_layout.addWidget(resume_button)
        open_folder_button = QPushButton("Open")
        open_folder_button.setToolTip("Open containing folder")
        actions_layout.addWidget(open_folder_button)
        actions_layout.addStretch()
        self.history_table.setCellWidget(row_position, 5, actions_widget)
        self.history_table.resizeRowsToContents()
    def open_download_folder(self):
        QMessageBox.information(self, "Open Folder", "Functionality to open download folder to be implemented.")
    def clear_history(self):
        reply = QMessageBox.question(self, "Confirm Clear", 
                                     "Are you sure you want to clear all download history?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.history_table.setRowCount(0)
            QMessageBox.information(self, "History Cleared", "Download history has been cleared.")
    def save_api_credentials(self):
        client_id = self.api_client_id_input.text()
        client_secret = self.api_client_secret_input.text()
        print(f"Saving API creds: ID={client_id}, Secret={'*' * len(client_secret)}")
        QMessageBox.information(self, "Settings", "API credentials saving to be implemented.")
    def save_download_config(self):
        default_dir = self.default_output_dir_input.text()
        print(f"Saving default output dir: {default_dir}")
        QMessageBox.information(self, "Settings", "Download configuration saving to be implemented.")
    def save_app_settings(self):
        rate_limit = self.rate_limit_input.text()
        theme = self.theme_combo.currentText()
        print(f"Saving app settings: Rate Limit={rate_limit}, Theme={theme}")
        QMessageBox.information(self, "Settings", "Application settings saving to be implemented.")
    def load_settings(self):
        if not self.default_output_dir_input.text():
            pass
        default_dir = self.default_output_dir_input.text()
        if default_dir:
            if not self.single_output_dir_input.text():
                self.single_output_dir_input.setText(default_dir)
            if not self.sync_output_dir_input.text():
                self.sync_output_dir_input.setText(default_dir)
        print("Loading settings (placeholder)...")
    def load_history(self):
        self.history_table.setRowCount(0)
        self.add_item_to_history("https://reddit.com/r/pics/example1", "Post", "2024-05-26 12:30", "Completed", "/downloads/example1.jpg")
        self.add_item_to_history("r/gifs_sync_1", "Subreddit Sync", "2024-05-25 18:00", "Incomplete (50/100)", "/downloads/gifs_sync_1")
        self.add_item_to_history("https://reddit.com/r/videos/example2", "Post", "2024-05-24 09:15", "Failed", "/downloads/temp")
        QMessageBox.information(self, "History", "History loading to be implemented. Displaying sample data.")
    def apply_theme(self, index):
        theme_name = self.theme_combo.itemText(index)
        if theme_name == "Dark Mode":
            self.setStyleSheet("""
                QWidget { background-color: #2E2E2E; color: #E0E0E0; }
                QGroupBox { border: 1px solid #555555; margin-top: 10px; }
                QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px; background-color: #2E2E2E; }
                QLineEdit, QTextEdit, QComboBox { background-color: #3C3C3C; border: 1px solid #555555; color: #E0E0E0; padding: 5px; border-radius: 3px;}
                QPushButton { background-color: #555555; color: #E0E0E0; border: 1px solid #666666; padding: 5px; border-radius: 3px;}
                QPushButton:hover { background-color: #666666; }
                QPushButton:pressed { background-color: #444444; }
                QTabWidget::pane { border: 1px solid #555555; }
                QTabBar::tab { background: #3C3C3C; color: #E0E0E0; padding: 8px; border-top-left-radius: 4px; border-top-right-radius: 4px;}
                QTabBar::tab:selected { background: #2E2E2E; font-weight: bold; }
                QProgressBar { border: 1px solid #555; border-radius: 3px; text-align: center; background-color: #3C3C3C; }
                QProgressBar::chunk { background-color: #007ACC; width: 10px; margin: 0.5px; }
                QTableWidget { background-color: #3C3C3C; border: 1px solid #555555; gridline-color: #555555; }
                QHeaderView::section { background-color: #4A4A4A; color: #E0E0E0; padding: 4px; border: 1px solid #555555; }
                QScrollArea { border: none; }
            """)
            self.download_button.setStyleSheet("padding: 8px; background-color: #006300; color: white; border-radius: 5px;")
            self.sync_button.setStyleSheet("padding: 8px; background-color: #005A9E; color: white; border-radius: 5px;")
        else:
            self.setStyleSheet("")
            self.download_button.setStyleSheet("padding: 8px; background-color: #4CAF50; color: white; border-radius: 5px;")
            self.sync_button.setStyleSheet("padding: 8px; background-color: #2196F3; color: white; border-radius: 5px;")
        QMessageBox.information(self, "Theme", f"{theme_name} applied (basic implementation).")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = RedditGrabberApp()
    main_window.show()
    sys.exit(app.exec())
