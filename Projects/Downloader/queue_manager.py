"""
Queue manager for Reddit Media Grabber.

Handles the download queue and its UI.
"""

import os
from typing import Dict, Any, List, Optional
from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtWidgets import (QWidget, QTableWidget, QTableWidgetItem,
                              QPushButton, QProgressBar, QMenu, QHeaderView)
from PySide6.QtGui import QIcon, QAction

class QueueManager(QObject):
    """Manages the download queue and its UI."""
    
    # Signals
    download_started = Signal(str)  # download_id
    download_paused = Signal(str)   # download_id
    download_resumed = Signal(str)  # download_id
    download_cancelled = Signal(str)  # download_id
    download_retried = Signal(str)  # download_id
    download_completed = Signal(str)  # download_id
    download_failed = Signal(str, str)  # download_id, error_message
    queue_cleared = Signal()
    
    def __init__(self, parent: Optional[QWidget] = None):
        """
        Initialize the queue manager.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.parent = parent
        self.queue_table = None
        self.downloads = {}
        self.settings = None
        
    def initialize(self, queue_table: QTableWidget, settings: Dict[str, Any]) -> None:
        """
        Initialize with queue table and settings.
        
        Args:
            queue_table: Queue table widget
            settings: Queue settings
        """
        self.queue_table = queue_table
        self.settings = settings
        
        # Set up queue table
        self._setup_queue_table()
        
    def _setup_queue_table(self) -> None:
        """Set up the queue table."""
        if not self.queue_table:
            return
            
        # Set column headers
        self.queue_table.setColumnCount(5)
        self.queue_table.setHorizontalHeaderLabels([
            "Title", "Status", "Progress", "Size", "Actions"
        ])
        
        # Set column widths
        header = self.queue_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Title
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Status
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Progress
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Size
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Actions
        
        # Enable sorting
        self.queue_table.setSortingEnabled(True)
        
        # Enable context menu
        self.queue_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.queue_table.customContextMenuRequested.connect(self._show_context_menu)
        
    def _show_context_menu(self, position) -> None:
        """
        Show context menu for queue table.
        
        Args:
            position: Mouse position
        """
        if not self.queue_table:
            return
            
        # Get selected items
        selected_items = self.queue_table.selectedItems()
        if not selected_items:
            return
            
        # Create context menu
        menu = QMenu()
        
        # Add actions
        pause_action = QAction("Pause", self.queue_table)
        pause_action.triggered.connect(self._pause_selected)
        menu.addAction(pause_action)
        
        resume_action = QAction("Resume", self.queue_table)
        resume_action.triggered.connect(self._resume_selected)
        menu.addAction(resume_action)
        
        cancel_action = QAction("Cancel", self.queue_table)
        cancel_action.triggered.connect(self._cancel_selected)
        menu.addAction(cancel_action)
        
        retry_action = QAction("Retry", self.queue_table)
        retry_action.triggered.connect(self._retry_selected)
        menu.addAction(retry_action)
        
        menu.addSeparator()
        
        clear_completed_action = QAction("Clear Completed", self.queue_table)
        clear_completed_action.triggered.connect(self.clear_completed)
        menu.addAction(clear_completed_action)
        
        clear_all_action = QAction("Clear All", self.queue_table)
        clear_all_action.triggered.connect(self.clear_all)
        menu.addAction(clear_all_action)
        
        # Show menu
        menu.exec_(self.queue_table.mapToGlobal(position))
        
    def add_download(self, download_id: str, title: str, 
                    file_size: Optional[str] = None) -> None:
        """
        Add a download to the queue.
        
        Args:
            download_id: Download ID
            title: Download title
            file_size: File size
        """
        if not self.queue_table:
            return
            
        # Create row
        row = self.queue_table.rowCount()
        self.queue_table.insertRow(row)
        
        # Set row height
        self.queue_table.setRowHeight(row, 40)
        
        # Add title
        title_item = QTableWidgetItem(title)
        title_item.setData(Qt.UserRole, download_id)
        self.queue_table.setItem(row, 0, title_item)
        
        # Add status
        status_item = QTableWidgetItem("Queued")
        self.queue_table.setItem(row, 1, status_item)
        
        # Add progress
        progress_item = QTableWidgetItem("0%")
        self.queue_table.setItem(row, 2, progress_item)
        
        # Add size
        size_item = QTableWidgetItem(file_size or "Unknown")
        self.queue_table.setItem(row, 3, size_item)
        
        # Add actions
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add buttons
        cancel_button = QPushButton()
        cancel_button.setIcon(QIcon("icons/cancel.png"))
        cancel_button.clicked.connect(lambda: self.cancel_download(download_id))
        actions_layout.addWidget(cancel_button)
        
        retry_button = QPushButton()
        retry_button.setIcon(QIcon("icons/retry.png"))
        retry_button.clicked.connect(lambda: self.retry_download(download_id))
        retry_button.hide()
        actions_layout.addWidget(retry_button)
        
        self.queue_table.setCellWidget(row, 4, actions_widget)
        
        # Store download info
        self.downloads[download_id] = {
            'row': row,
            'title': title,
            'status': "Queued",
            'progress': 0,
            'size': file_size,
            'cancel_button': cancel_button,
            'retry_button': retry_button
        }
        
        # Emit signal
        self.download_started.emit(download_id)
        
    def update_download(self, download_id: str, status: str, 
                       progress: int, error_message: Optional[str] = None) -> None:
        """
        Update download status and progress.
        
        Args:
            download_id: Download ID
            status: Download status
            progress: Progress percentage
            error_message: Error message if any
        """
        if download_id not in self.downloads:
            return
            
        download = self.downloads[download_id]
        row = download['row']
        
        # Update status
        status_item = self.queue_table.item(row, 1)
        if status_item:
            status_item.setText(status)
            
        # Update progress
        progress_item = self.queue_table.item(row, 2)
        if progress_item:
            progress_item.setText(f"{progress}%")
            
        # Update buttons
        if status == "Completed":
            download['cancel_button'].hide()
            download['retry_button'].hide()
            self.download_completed.emit(download_id)
        elif status == "Failed":
            download['cancel_button'].hide()
            download['retry_button'].show()
            self.download_failed.emit(download_id, error_message or "Unknown error")
        elif status == "Paused":
            download['cancel_button'].show()
            download['retry_button'].hide()
            self.download_paused.emit(download_id)
        elif status == "Downloading":
            download['cancel_button'].show()
            download['retry_button'].hide()
            if download['status'] == "Paused":
                self.download_resumed.emit(download_id)
                
        # Update download info
        download['status'] = status
        download['progress'] = progress
        
    def cancel_download(self, download_id: str) -> None:
        """
        Cancel a download.
        
        Args:
            download_id: Download ID
        """
        if download_id in self.downloads:
            self.download_cancelled.emit(download_id)
            
    def retry_download(self, download_id: str) -> None:
        """
        Retry a failed download.
        
        Args:
            download_id: Download ID
        """
        if download_id in self.downloads:
            self.download_retried.emit(download_id)
            
    def clear_completed(self) -> None:
        """Clear completed downloads from the queue."""
        if not self.queue_table:
            return
            
        # Remove completed downloads
        for download_id, download in list(self.downloads.items()):
            if download['status'] == "Completed":
                self.queue_table.removeRow(download['row'])
                del self.downloads[download_id]
                
        # Update row numbers
        self._update_row_numbers()
        
        # Emit signal
        self.queue_cleared.emit()
        
    def clear_all(self) -> None:
        """Clear all downloads from the queue."""
        if not self.queue_table:
            return
            
        # Remove all downloads
        self.queue_table.setRowCount(0)
        self.downloads.clear()
        
        # Emit signal
        self.queue_cleared.emit()
        
    def _update_row_numbers(self) -> None:
        """Update row numbers after removing downloads."""
        for row in range(self.queue_table.rowCount()):
            download_id = self.queue_table.item(row, 0).data(Qt.UserRole)
            if download_id in self.downloads:
                self.downloads[download_id]['row'] = row
                
    def get_download(self, download_id: str) -> Optional[Dict[str, Any]]:
        """
        Get download information.
        
        Args:
            download_id: Download ID
            
        Returns:
            Optional[Dict[str, Any]]: Download information or None
        """
        return self.downloads.get(download_id)
        
    def get_all_downloads(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all download information.
        
        Returns:
            Dict[str, Dict[str, Any]]: Dictionary of download information
        """
        return self.downloads.copy()
        
    def cleanup(self) -> None:
        """Clean up resources."""
        if self.queue_table:
            self.queue_table.clear()
            self.queue_table.setRowCount(0)
        self.downloads.clear() 