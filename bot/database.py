"""
Database operations for TikTok Viral Clothing Bot
"""
import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional
import config


class Database:
    """Handle all database operations"""
    
    def __init__(self, db_path: str = None):
        """Initialize database connection"""
        self.db_path = db_path or config.DATABASE_PATH
        self._ensure_data_directory()
        self._init_database()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        data_dir = os.path.dirname(self.db_path)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def _get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def _init_database(self):
        """Initialize database schema"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Create videos table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id TEXT UNIQUE NOT NULL,
                video_link TEXT NOT NULL,
                thumbnail_url TEXT,
                views INTEGER DEFAULT 0,
                likes INTEGER DEFAULT 0,
                total_comments INTEGER DEFAULT 0,
                product_inquiry_comments INTEGER DEFAULT 0,
                post_time TIMESTAMP,
                scraped_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_video(self, video_data: Dict) -> bool:
        """
        Save or update video data
        
        Args:
            video_data: Dictionary containing video information
            
        Returns:
            True if successful, False otherwise
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO videos 
                (video_id, video_link, thumbnail_url, views, likes, 
                 total_comments, product_inquiry_comments, post_time, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                video_data['video_id'],
                video_data['video_link'],
                video_data.get('thumbnail_url', ''),
                video_data.get('views', 0),
                video_data.get('likes', 0),
                video_data.get('total_comments', 0),
                video_data.get('product_inquiry_comments', 0),
                video_data.get('post_time')
            ))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error saving video: {e}")
            return False
        finally:
            conn.close()
    
    def get_all_videos(self, sort_by: str = 'product_inquiry_comments', 
                      order: str = 'DESC') -> List[Dict]:
        """
        Get all videos from database
        
        Args:
            sort_by: Column to sort by
            order: Sort order (ASC or DESC)
            
        Returns:
            List of video dictionaries
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Validate sort_by to prevent SQL injection
        valid_columns = ['product_inquiry_comments', 'views', 'likes', 
                        'total_comments', 'post_time']
        if sort_by not in valid_columns:
            sort_by = 'product_inquiry_comments'
        
        # Validate order
        order = 'DESC' if order.upper() == 'DESC' else 'ASC'
        
        query = f'''
            SELECT video_id, video_link, thumbnail_url, views, likes,
                   total_comments, product_inquiry_comments, post_time,
                   scraped_time, last_updated
            FROM videos
            ORDER BY {sort_by} {order}
        '''
        
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        videos = []
        for row in rows:
            videos.append({
                'video_id': row[0],
                'video_link': row[1],
                'thumbnail_url': row[2],
                'views': row[3],
                'likes': row[4],
                'total_comments': row[5],
                'product_inquiry_comments': row[6],
                'post_time': row[7],
                'scraped_time': row[8],
                'last_updated': row[9]
            })
        
        return videos
    
    def get_video_by_id(self, video_id: str) -> Optional[Dict]:
        """Get a specific video by ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT video_id, video_link, thumbnail_url, views, likes,
                   total_comments, product_inquiry_comments, post_time
            FROM videos
            WHERE video_id = ?
        ''', (video_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'video_id': row[0],
                'video_link': row[1],
                'thumbnail_url': row[2],
                'views': row[3],
                'likes': row[4],
                'total_comments': row[5],
                'product_inquiry_comments': row[6],
                'post_time': row[7]
            }
        return None
    
    def delete_old_videos(self, hours: int = 24):
        """Delete videos older than specified hours"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM videos
            WHERE post_time < datetime('now', '-' || ? || ' hours')
        ''', (hours,))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count
    
    def get_video_count(self) -> int:
        """Get total number of videos in database"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM videos')
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
