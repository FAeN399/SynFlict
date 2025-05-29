"""
Preview manager for Reddit Media Grabber.

Handles file previews and thumbnails.
"""

import os
import mimetypes
from typing import Dict, Any, Optional, Tuple
from PySide6.QtCore import QObject, Signal, Qt, QSize
from PySide6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout,
                              QPushButton, QScrollArea)
from PySide6.QtGui import QPixmap, QImage, QIcon
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget

class PreviewManager(QObject):
    """Manages file previews and thumbnails."""
    
    # Signals
    preview_ready = Signal(str, QPixmap)  # file_path, thumbnail
    preview_error = Signal(str, str)  # file_path, error_message
    
    def __init__(self, parent: Optional[QWidget] = None):
        """
        Initialize the preview manager.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.parent = parent
        self.settings = None
        self.thumbnail_cache = {}
        self.media_player = None
        self.audio_output = None
        self.video_widget = None
        
    def initialize(self, settings: Dict[str, Any]) -> None:
        """
        Initialize with settings.
        
        Args:
            settings: Preview settings
        """
        self.settings = settings
        
        # Set up media player if enabled
        if self.settings.get('enable_preview', True):
            self._setup_media_player()
            
    def _setup_media_player(self) -> None:
        """Set up media player for audio/video previews."""
        if not self.media_player:
            self.media_player = QMediaPlayer()
            self.audio_output = QAudioOutput()
            self.media_player.setAudioOutput(self.audio_output)
            
            # Create video widget
            self.video_widget = QVideoWidget()
            self.media_player.setVideoOutput(self.video_widget)
            
    def get_preview_widget(self, file_path: str) -> Optional[QWidget]:
        """
        Get a preview widget for a file.
        
        Args:
            file_path: Path to file
            
        Returns:
            Optional[QWidget]: Preview widget or None
        """
        if not os.path.exists(file_path):
            return None
            
        # Get file type
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            return None
            
        # Create preview based on type
        if mime_type.startswith('image/'):
            return self._create_image_preview(file_path)
        elif mime_type.startswith('video/'):
            return self._create_video_preview(file_path)
        elif mime_type.startswith('audio/'):
            return self._create_audio_preview(file_path)
        else:
            return self._create_file_info_preview(file_path)
            
    def _create_image_preview(self, file_path: str) -> QWidget:
        """
        Create an image preview widget.
        
        Args:
            file_path: Path to image file
            
        Returns:
            QWidget: Image preview widget
        """
        # Create widget
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Create image label
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        
        # Load image
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            # Scale image to fit
            max_size = QSize(800, 600)
            pixmap = pixmap.scaled(
                max_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            image_label.setPixmap(pixmap)
            
            # Add to layout
            layout.addWidget(image_label)
            
            # Create scroll area
            scroll = QScrollArea()
            scroll.setWidget(image_label)
            scroll.setWidgetResizable(True)
            layout.addWidget(scroll)
            
        return widget
        
    def _create_video_preview(self, file_path: str) -> QWidget:
        """
        Create a video preview widget.
        
        Args:
            file_path: Path to video file
            
        Returns:
            QWidget: Video preview widget
        """
        if not self.media_player or not self.video_widget:
            return None
            
        # Create widget
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Add video widget
        layout.addWidget(self.video_widget)
        
        # Create controls
        controls = QWidget()
        controls_layout = QHBoxLayout(controls)
        
        # Add play button
        play_button = QPushButton()
        play_button.setIcon(QIcon("icons/play.png"))
        play_button.clicked.connect(self.media_player.play)
        controls_layout.addWidget(play_button)
        
        # Add pause button
        pause_button = QPushButton()
        pause_button.setIcon(QIcon("icons/pause.png"))
        pause_button.clicked.connect(self.media_player.pause)
        controls_layout.addWidget(pause_button)
        
        # Add stop button
        stop_button = QPushButton()
        stop_button.setIcon(QIcon("icons/stop.png"))
        stop_button.clicked.connect(self.media_player.stop)
        controls_layout.addWidget(stop_button)
        
        # Add controls to layout
        layout.addWidget(controls)
        
        # Set media
        self.media_player.setSource(file_path)
        
        return widget
        
    def _create_audio_preview(self, file_path: str) -> QWidget:
        """
        Create an audio preview widget.
        
        Args:
            file_path: Path to audio file
            
        Returns:
            QWidget: Audio preview widget
        """
        if not self.media_player or not self.audio_output:
            return None
            
        # Create widget
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Create controls
        controls = QWidget()
        controls_layout = QHBoxLayout(controls)
        
        # Add play button
        play_button = QPushButton()
        play_button.setIcon(QIcon("icons/play.png"))
        play_button.clicked.connect(self.media_player.play)
        controls_layout.addWidget(play_button)
        
        # Add pause button
        pause_button = QPushButton()
        pause_button.setIcon(QIcon("icons/pause.png"))
        pause_button.clicked.connect(self.media_player.pause)
        controls_layout.addWidget(pause_button)
        
        # Add stop button
        stop_button = QPushButton()
        stop_button.setIcon(QIcon("icons/stop.png"))
        stop_button.clicked.connect(self.media_player.stop)
        controls_layout.addWidget(stop_button)
        
        # Add controls to layout
        layout.addWidget(controls)
        
        # Set media
        self.media_player.setSource(file_path)
        
        return widget
        
    def _create_file_info_preview(self, file_path: str) -> QWidget:
        """
        Create a file info preview widget.
        
        Args:
            file_path: Path to file
            
        Returns:
            QWidget: File info preview widget
        """
        # Create widget
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Get file info
        file_info = os.stat(file_path)
        
        # Create info label
        info_label = QLabel()
        info_label.setText(
            f"Name: {os.path.basename(file_path)}\n"
            f"Size: {self._format_size(file_info.st_size)}\n"
            f"Type: {mimetypes.guess_type(file_path)[0] or 'Unknown'}\n"
            f"Created: {self._format_time(file_info.st_ctime)}\n"
            f"Modified: {self._format_time(file_info.st_mtime)}"
        )
        
        # Add to layout
        layout.addWidget(info_label)
        
        return widget
        
    def _format_size(self, size: int) -> str:
        """
        Format file size.
        
        Args:
            size: Size in bytes
            
        Returns:
            str: Formatted size
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} PB"
        
    def _format_time(self, timestamp: float) -> str:
        """
        Format timestamp.
        
        Args:
            timestamp: Unix timestamp
            
        Returns:
            str: Formatted time
        """
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        
    def get_thumbnail(self, file_path: str, 
                     size: QSize = QSize(100, 100)) -> Optional[QPixmap]:
        """
        Get a thumbnail for a file.
        
        Args:
            file_path: Path to file
            size: Thumbnail size
            
        Returns:
            Optional[QPixmap]: Thumbnail or None
        """
        # Check cache
        cache_key = f"{file_path}_{size.width()}_{size.height()}"
        if cache_key in self.thumbnail_cache:
            return self.thumbnail_cache[cache_key]
            
        if not os.path.exists(file_path):
            return None
            
        # Get file type
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            return None
            
        # Create thumbnail based on type
        if mime_type.startswith('image/'):
            thumbnail = self._create_image_thumbnail(file_path, size)
        elif mime_type.startswith('video/'):
            thumbnail = self._create_video_thumbnail(file_path, size)
        elif mime_type.startswith('audio/'):
            thumbnail = self._create_audio_thumbnail(file_path, size)
        else:
            thumbnail = self._create_file_thumbnail(file_path, size)
            
        # Cache thumbnail
        if thumbnail:
            self.thumbnail_cache[cache_key] = thumbnail
            
        return thumbnail
        
    def _create_image_thumbnail(self, file_path: str, 
                               size: QSize) -> Optional[QPixmap]:
        """
        Create an image thumbnail.
        
        Args:
            file_path: Path to image file
            size: Thumbnail size
            
        Returns:
            Optional[QPixmap]: Thumbnail or None
        """
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            return pixmap.scaled(
                size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        return None
        
    def _create_video_thumbnail(self, file_path: str, 
                               size: QSize) -> Optional[QPixmap]:
        """
        Create a video thumbnail.
        
        Args:
            file_path: Path to video file
            size: Thumbnail size
            
        Returns:
            Optional[QPixmap]: Thumbnail or None
        """
        # TODO: Implement video thumbnail generation
        return None
        
    def _create_audio_thumbnail(self, file_path: str, 
                               size: QSize) -> Optional[QPixmap]:
        """
        Create an audio thumbnail.
        
        Args:
            file_path: Path to audio file
            size: Thumbnail size
            
        Returns:
            Optional[QPixmap]: Thumbnail or None
        """
        # Create default audio icon
        pixmap = QPixmap("icons/audio.png")
        if not pixmap.isNull():
            return pixmap.scaled(
                size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        return None
        
    def _create_file_thumbnail(self, file_path: str, 
                              size: QSize) -> Optional[QPixmap]:
        """
        Create a file thumbnail.
        
        Args:
            file_path: Path to file
            size: Thumbnail size
            
        Returns:
            Optional[QPixmap]: Thumbnail or None
        """
        # Create default file icon
        pixmap = QPixmap("icons/file.png")
        if not pixmap.isNull():
            return pixmap.scaled(
                size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        return None
        
    def clear_cache(self) -> None:
        """Clear thumbnail cache."""
        self.thumbnail_cache.clear()
        
    def cleanup(self) -> None:
        """Clean up resources."""
        if self.media_player:
            self.media_player.stop()
            self.media_player.deleteLater()
            self.media_player = None
            
        if self.audio_output:
            self.audio_output.deleteLater()
            self.audio_output = None
            
        if self.video_widget:
            self.video_widget.deleteLater()
            self.video_widget = None
            
        self.clear_cache() 