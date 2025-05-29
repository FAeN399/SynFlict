"""
Shortcut manager for Reddit Media Grabber.

Handles keyboard shortcuts and their actions.
"""

from typing import Dict, Any, Callable, Optional
from PySide6.QtCore import QObject
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QWidget

class ShortcutManager(QObject):
    """Manages keyboard shortcuts."""
    
    def __init__(self, parent: Optional[QWidget] = None):
        """
        Initialize the shortcut manager.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.parent = parent
        self.shortcuts = {}
        self.settings = None
        
    def initialize(self, settings: Dict[str, Any]) -> None:
        """
        Initialize with settings.
        
        Args:
            settings: Shortcut settings
        """
        self.settings = settings
        
        # Create shortcuts if enabled
        if self.settings.get('enable_keyboard_shortcuts', True):
            self._setup_shortcuts()
            
    def _setup_shortcuts(self) -> None:
        """Set up keyboard shortcuts."""
        # Clear existing shortcuts
        self._clear_shortcuts()
        
        # Add shortcuts from settings
        for action, key_sequence in self.settings.items():
            if action.startswith('shortcut_'):
                self.add_shortcut(
                    action.replace('shortcut_', ''),
                    key_sequence,
                    self._get_action_handler(action)
                )
                
    def _clear_shortcuts(self) -> None:
        """Clear all shortcuts."""
        for shortcut in self.shortcuts.values():
            shortcut.deleteLater()
        self.shortcuts.clear()
        
    def _get_action_handler(self, action: str) -> Callable:
        """
        Get the handler function for an action.
        
        Args:
            action: Action name
            
        Returns:
            Callable: Handler function
        """
        # Map action names to handler functions
        handlers = {
            'shortcut_pause_resume': self.parent.toggle_download,
            'shortcut_cancel': self.parent.cancel_download,
            'shortcut_retry': self.parent.retry_download,
            'shortcut_clear_completed': self.parent.clear_completed,
            'shortcut_clear_all': self.parent.clear_all,
            'shortcut_show_settings': self.parent.show_settings,
            'shortcut_exit': self.parent.close,
            'shortcut_minimize': self.parent.showMinimized,
            'shortcut_maximize': self.parent.showMaximized,
            'shortcut_restore': self.parent.showNormal,
            'shortcut_new_download': self.parent.new_download,
            'shortcut_open_download_dir': self.parent.open_download_dir,
            'shortcut_copy_url': self.parent.copy_url,
            'shortcut_paste_url': self.parent.paste_url,
            'shortcut_select_all': self.parent.select_all,
            'shortcut_deselect_all': self.parent.deselect_all,
            'shortcut_delete_selected': self.parent.delete_selected,
            'shortcut_show_preview': self.parent.show_preview,
            'shortcut_show_history': self.parent.show_history,
            'shortcut_show_queue': self.parent.show_queue,
            'shortcut_show_stats': self.parent.show_stats,
            'shortcut_show_help': self.parent.show_help,
            'shortcut_show_about': self.parent.show_about
        }
        
        return handlers.get(action, lambda: None)
        
    def add_shortcut(self, name: str, key_sequence: str, 
                    handler: Callable) -> None:
        """
        Add a keyboard shortcut.
        
        Args:
            name: Shortcut name
            key_sequence: Key sequence string
            handler: Handler function
        """
        if not self.parent:
            return
            
        # Create shortcut
        shortcut = QShortcut(QKeySequence(key_sequence), self.parent)
        shortcut.activated.connect(handler)
        
        # Store shortcut
        self.shortcuts[name] = shortcut
        
    def remove_shortcut(self, name: str) -> None:
        """
        Remove a keyboard shortcut.
        
        Args:
            name: Shortcut name
        """
        if name in self.shortcuts:
            self.shortcuts[name].deleteLater()
            del self.shortcuts[name]
            
    def update_shortcut(self, name: str, key_sequence: str) -> None:
        """
        Update a keyboard shortcut.
        
        Args:
            name: Shortcut name
            key_sequence: New key sequence
        """
        if name in self.shortcuts:
            self.shortcuts[name].setKey(QKeySequence(key_sequence))
            
    def get_shortcut(self, name: str) -> Optional[QShortcut]:
        """
        Get a keyboard shortcut.
        
        Args:
            name: Shortcut name
            
        Returns:
            Optional[QShortcut]: Shortcut object or None
        """
        return self.shortcuts.get(name)
        
    def get_all_shortcuts(self) -> Dict[str, QShortcut]:
        """
        Get all keyboard shortcuts.
        
        Returns:
            Dict[str, QShortcut]: Dictionary of shortcuts
        """
        return self.shortcuts.copy()
        
    def cleanup(self) -> None:
        """Clean up resources."""
        self._clear_shortcuts() 