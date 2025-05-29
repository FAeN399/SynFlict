"""
History manager for Reddit Media Grabber.

Handles download history and its UI.
"""

import os
import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtWidgets import (QWidget, QTableWidget, QTableWidgetItem,
                              QMenu, QHeaderView)
from PySide6.QtGui import QIcon, QAction

class HistoryManager(QObject):
    """Manages download history and its UI."""
    
    # Signals
    history_cleared = Signal()
    history_item_removed = Signal(str)  # download_id
    
    def __init__(self, parent: Optional[QWidget] = None):
        """
        Initialize the history manager.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.parent = parent
        self.history_table = None
        self.history_file = "download_history.json"
        self.history = {}
        self.settings = None
        
    def initialize(self, history_table: QTableWidget, settings: Dict[str, Any]) -> None:
        """
        Initialize with history table and settings.
        
        Args:
            history_table: History table widget
            settings: History settings
        """
        self.history_table = history_table
        self.settings = settings
        
        # Set up history table
        self._setup_history_table()
        
        # Load history
        self.load_history()
        
    def _setup_history_table(self) -> None:
        """Set up the history table."""
        if not self.history_table:
            return
            
        # Set column headers
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels([
            "Title", "Status", "Size", "Date", "Source", "Actions"
        ])
        
        # Set column widths
        header = self.history_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Title
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Status
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Size
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Date
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Source
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Actions
        
        # Enable sorting
        self.history_table.setSortingEnabled(True)
        
        # Enable context menu
        self.history_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.history_table.customContextMenuRequested.connect(self._show_context_menu)
        
    def _show_context_menu(self, position) -> None:
        """
        Show context menu for history table.
        
        Args:
            position: Mouse position
        """
        if not self.history_table:
            return
            
        # Get selected items
        selected_items = self.history_table.selectedItems()
        if not selected_items:
            return
            
        # Create context menu
        menu = QMenu()
        
        # Add actions
        open_file_action = QAction("Open File", self.history_table)
        open_file_action.triggered.connect(self._open_selected_file)
        menu.addAction(open_file_action)
        
        open_folder_action = QAction("Open Folder", self.history_table)
        open_folder_action.triggered.connect(self._open_selected_folder)
        menu.addAction(open_folder_action)
        
        copy_url_action = QAction("Copy URL", self.history_table)
        copy_url_action.triggered.connect(self._copy_selected_url)
        menu.addAction(copy_url_action)
        
        menu.addSeparator()
        
        remove_action = QAction("Remove from History", self.history_table)
        remove_action.triggered.connect(self._remove_selected)
        menu.addAction(remove_action)
        
        clear_history_action = QAction("Clear History", self.history_table)
        clear_history_action.triggered.connect(self.clear_history)
        menu.addAction(clear_history_action)
        
        # Show menu
        menu.exec_(self.history_table.mapToGlobal(position))
        
    def add_to_history(self, download_id: str, title: str, status: str,
                      file_size: Optional[str], source: str,
                      file_path: Optional[str] = None) -> None:
        """
        Add a download to history.
        
        Args:
            download_id: Download ID
            title: Download title
            status: Download status
            file_size: File size
            source: Download source
            file_path: Path to downloaded file
        """
        if not self.history_table:
            return
            
        # Create row
        row = self.history_table.rowCount()
        self.history_table.insertRow(row)
        
        # Set row height
        self.history_table.setRowHeight(row, 40)
        
        # Add title
        title_item = QTableWidgetItem(title)
        title_item.setData(Qt.UserRole, download_id)
        self.history_table.setItem(row, 0, title_item)
        
        # Add status
        status_item = QTableWidgetItem(status)
        self.history_table.setItem(row, 1, status_item)
        
        # Add size
        size_item = QTableWidgetItem(file_size or "Unknown")
        self.history_table.setItem(row, 2, size_item)
        
        # Add date
        date_item = QTableWidgetItem(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self.history_table.setItem(row, 3, date_item)
        
        # Add source
        source_item = QTableWidgetItem(source)
        self.history_table.setItem(row, 4, source_item)
        
        # Add actions
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add buttons
        open_button = QPushButton()
        open_button.setIcon(QIcon("icons/open.png"))
        open_button.clicked.connect(lambda: self._open_file(download_id))
        actions_layout.addWidget(open_button)
        
        remove_button = QPushButton()
        remove_button.setIcon(QIcon("icons/remove.png"))
        remove_button.clicked.connect(lambda: self.remove_from_history(download_id))
        actions_layout.addWidget(remove_button)
        
        self.history_table.setCellWidget(row, 5, actions_widget)
        
        # Store history info
        self.history[download_id] = {
            'row': row,
            'title': title,
            'status': status,
            'size': file_size,
            'date': date_item.text(),
            'source': source,
            'file_path': file_path,
            'open_button': open_button,
            'remove_button': remove_button
        }
        
        # Save history
        self.save_history()
        
    def remove_from_history(self, download_id: str) -> None:
        """
        Remove a download from history.
        
        Args:
            download_id: Download ID
        """
        if download_id not in self.history:
            return
            
        # Remove row
        row = self.history[download_id]['row']
        self.history_table.removeRow(row)
        
        # Remove from history
        del self.history[download_id]
        
        # Update row numbers
        self._update_row_numbers()
        
        # Save history
        self.save_history()
        
        # Emit signal
        self.history_item_removed.emit(download_id)
        
    def clear_history(self) -> None:
        """Clear all history."""
        if not self.history_table:
            return
            
        # Remove all rows
        self.history_table.setRowCount(0)
        
        # Clear history
        self.history.clear()
        
        # Save history
        self.save_history()
        
        # Emit signal
        self.history_cleared.emit()
        
    def _update_row_numbers(self) -> None:
        """Update row numbers after removing items."""
        for row in range(self.history_table.rowCount()):
            download_id = self.history_table.item(row, 0).data(Qt.UserRole)
            if download_id in self.history:
                self.history[download_id]['row'] = row
                
    def _open_file(self, download_id: str) -> None:
        """
        Open a downloaded file.
        
        Args:
            download_id: Download ID
        """
        if download_id not in self.history:
            return
            
        file_path = self.history[download_id]['file_path']
        if file_path and os.path.exists(file_path):
            os.startfile(file_path)
            
    def _open_selected_file(self) -> None:
        """Open selected file."""
        selected_items = self.history_table.selectedItems()
        if not selected_items:
            return
            
        download_id = selected_items[0].data(Qt.UserRole)
        self._open_file(download_id)
        
    def _open_selected_folder(self) -> None:
        """Open selected folder."""
        selected_items = self.history_table.selectedItems()
        if not selected_items:
            return
            
        download_id = selected_items[0].data(Qt.UserRole)
        if download_id in self.history:
            file_path = self.history[download_id]['file_path']
            if file_path and os.path.exists(file_path):
                os.startfile(os.path.dirname(file_path))
                
    def _copy_selected_url(self) -> None:
        """Copy selected URL."""
        selected_items = self.history_table.selectedItems()
        if not selected_items:
            return
            
        download_id = selected_items[0].data(Qt.UserRole)
        if download_id in self.history:
            source = self.history[download_id]['source']
            QApplication.clipboard().setText(source)
            
    def _remove_selected(self) -> None:
        """Remove selected items."""
        selected_items = self.history_table.selectedItems()
        if not selected_items:
            return
            
        download_id = selected_items[0].data(Qt.UserRole)
        self.remove_from_history(download_id)
        
    def load_history(self) -> None:
        """Load history from file."""
        if not os.path.exists(self.history_file):
            return
            
        try:
            with open(self.history_file, 'r') as f:
                history_data = json.load(f)
                
            # Add items to table
            for download_id, data in history_data.items():
                self.add_to_history(
                    download_id,
                    data['title'],
                    data['status'],
                    data['size'],
                    data['source'],
                    data['file_path']
                )
        except Exception as e:
            print(f"Error loading history: {e}")
            
    def save_history(self) -> None:
        """Save history to file."""
        try:
            # Convert history to serializable format
            history_data = {}
            for download_id, data in self.history.items():
                history_data[download_id] = {
                    'title': data['title'],
                    'status': data['status'],
                    'size': data['size'],
                    'date': data['date'],
                    'source': data['source'],
                    'file_path': data['file_path']
                }
                
            # Save to file
            with open(self.history_file, 'w') as f:
                json.dump(history_data, f, indent=4)
        except Exception as e:
            print(f"Error saving history: {e}")
            
    def get_history_item(self, download_id: str) -> Optional[Dict[str, Any]]:
        """
        Get history item information.
        
        Args:
            download_id: Download ID
            
        Returns:
            Optional[Dict[str, Any]]: History item information or None
        """
        return self.history.get(download_id)
        
    def get_all_history(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all history information.
        
        Returns:
            Dict[str, Dict[str, Any]]: Dictionary of history information
        """
        return self.history.copy()
        
    def cleanup(self) -> None:
        """Clean up resources."""
        if self.history_table:
            self.history_table.clear()
            self.history_table.setRowCount(0)
        self.history.clear() 