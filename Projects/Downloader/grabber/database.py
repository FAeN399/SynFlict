"""
SQLite database module for caching and tracking downloaded content.

Provides functionality for tracking downloaded submissions and files,
enabling de-duplication and resumable downloads.
"""

import sqlite3
import logging
import os
import time
from typing import Optional, List, Dict, Any, Tuple

logger = logging.getLogger(__name__)


class Database:
    """
    SQLite database for caching and tracking downloaded content.
    """
    
    def __init__(self, db_path: str = "grabber.db"):
        """
        Initialize the database.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        
        # Connect to the database
        self._connect()
    
    def _connect(self):
        """
        Connect to the SQLite database.
        """
        # Enable foreign keys and journal mode WAL for better concurrency
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.execute("PRAGMA journal_mode = WAL")
        
        # Use Row as row factory for easier access to columns by name
        self.conn.row_factory = sqlite3.Row
    
    def initialize(self):
        """
        Initialize the database schema.
        
        Creates the necessary tables if they don't exist.
        """
        # Create tables
        with self.conn:
            # Files table for de-duplication
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS files (
                    hash TEXT PRIMARY KEY,
                    path TEXT NOT NULL,
                    first_seen INTEGER NOT NULL
                )
            """)
            
            # Posts table for tracking downloaded submissions
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                    id TEXT PRIMARY KEY,
                    permalink TEXT NOT NULL,
                    downloaded INTEGER DEFAULT 0,
                    last_check INTEGER NOT NULL
                )
            """)
            
            logger.debug("Database schema initialized")
    
    def add_file_hash(self, file_hash: str, file_path: str) -> bool:
        """
        Add a file hash to the database.
        
        Args:
            file_hash: SHA-1 hash of the file
            file_path: Path to the file
            
        Returns:
            True if the hash was added, False if it already existed
        """
        try:
            with self.conn:
                # Check if the hash already exists
                cursor = self.conn.execute(
                    "SELECT hash FROM files WHERE hash = ?",
                    (file_hash,)
                )
                
                if cursor.fetchone():
                    logger.debug(f"File hash already exists: {file_hash}")
                    return False
                
                # Add the hash
                current_time = int(time.time())
                self.conn.execute(
                    "INSERT INTO files (hash, path, first_seen) VALUES (?, ?, ?)",
                    (file_hash, file_path, current_time)
                )
                
                logger.debug(f"Added file hash: {file_hash}, path: {file_path}")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error adding file hash: {e}")
            return False
    
    def has_file_hash(self, file_hash: str) -> bool:
        """
        Check if a file hash exists in the database.
        
        Args:
            file_hash: SHA-1 hash of the file
            
        Returns:
            True if the hash exists, False otherwise
        """
        try:
            cursor = self.conn.execute(
                "SELECT hash FROM files WHERE hash = ?",
                (file_hash,)
            )
            
            return cursor.fetchone() is not None
        except sqlite3.Error as e:
            logger.error(f"Error checking file hash: {e}")
            return False
    
    def get_file_path(self, file_hash: str) -> Optional[str]:
        """
        Get the path of a file by its hash.
        
        Args:
            file_hash: SHA-1 hash of the file
            
        Returns:
            Path to the file, or None if the hash doesn't exist
        """
        try:
            cursor = self.conn.execute(
                "SELECT path FROM files WHERE hash = ?",
                (file_hash,)
            )
            
            row = cursor.fetchone()
            return row['path'] if row else None
        except sqlite3.Error as e:
            logger.error(f"Error getting file path: {e}")
            return None
    
    def add_post(self, post_id: str, permalink: str) -> bool:
        """
        Add a post to the database.
        
        Args:
            post_id: Reddit submission ID
            permalink: Reddit permalink
            
        Returns:
            True if the post was added, False if it already existed
        """
        try:
            with self.conn:
                # Check if the post already exists
                cursor = self.conn.execute(
                    "SELECT id FROM posts WHERE id = ?",
                    (post_id,)
                )
                
                if cursor.fetchone():
                    logger.debug(f"Post already exists: {post_id}")
                    return False
                
                # Add the post
                current_time = int(time.time())
                self.conn.execute(
                    "INSERT INTO posts (id, permalink, downloaded, last_check) VALUES (?, ?, 0, ?)",
                    (post_id, permalink, current_time)
                )
                
                logger.debug(f"Added post: {post_id}, permalink: {permalink}")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error adding post: {e}")
            return False
    
    def has_post(self, post_id: str) -> bool:
        """
        Check if a post exists in the database.
        
        Args:
            post_id: Reddit submission ID
            
        Returns:
            True if the post exists, False otherwise
        """
        try:
            cursor = self.conn.execute(
                "SELECT id FROM posts WHERE id = ?",
                (post_id,)
            )
            
            return cursor.fetchone() is not None
        except sqlite3.Error as e:
            logger.error(f"Error checking post: {e}")
            return False
    
    def mark_post_downloaded(self, post_id: str) -> bool:
        """
        Mark a post as downloaded.
        
        Args:
            post_id: Reddit submission ID
            
        Returns:
            True if the post was marked as downloaded, False otherwise
        """
        try:
            with self.conn:
                current_time = int(time.time())
                self.conn.execute(
                    "UPDATE posts SET downloaded = 1, last_check = ? WHERE id = ?",
                    (current_time, post_id)
                )
                
                logger.debug(f"Marked post as downloaded: {post_id}")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error marking post as downloaded: {e}")
            return False
    
    def is_post_downloaded(self, post_id: str) -> bool:
        """
        Check if a post has been downloaded.
        
        Args:
            post_id: Reddit submission ID
            
        Returns:
            True if the post has been downloaded, False otherwise
        """
        try:
            cursor = self.conn.execute(
                "SELECT downloaded FROM posts WHERE id = ?",
                (post_id,)
            )
            
            row = cursor.fetchone()
            return row and row['downloaded'] == 1
        except sqlite3.Error as e:
            logger.error(f"Error checking if post is downloaded: {e}")
            return False
    
    def update_post_check_time(self, post_id: str) -> bool:
        """
        Update the last check time of a post.
        
        Args:
            post_id: Reddit submission ID
            
        Returns:
            True if the time was updated, False otherwise
        """
        try:
            with self.conn:
                current_time = int(time.time())
                self.conn.execute(
                    "UPDATE posts SET last_check = ? WHERE id = ?",
                    (current_time, post_id)
                )
                
                logger.debug(f"Updated post check time: {post_id}")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error updating post check time: {e}")
            return False
    
    def get_all_posts(self, downloaded_only: bool = False) -> List[Dict[str, Any]]:
        """
        Get all posts in the database.
        
        Args:
            downloaded_only: If True, only return posts that have been downloaded
            
        Returns:
            List of dictionaries containing post data
        """
        try:
            query = "SELECT id, permalink, downloaded, last_check FROM posts"
            if downloaded_only:
                query += " WHERE downloaded = 1"
            
            cursor = self.conn.execute(query)
            
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Error getting posts: {e}")
            return []
    
    def vacuum(self) -> bool:
        """
        Vacuum the database to optimize storage.
        
        Returns:
            True if the vacuum was successful, False otherwise
        """
        try:
            self.conn.execute("VACUUM")
            logger.info("Database vacuumed")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error vacuuming database: {e}")
            return False
    
    def close(self):
        """
        Close the database connection.
        """
        if self.conn:
            self.conn.close()
            self.conn = None
            logger.debug("Database connection closed")
