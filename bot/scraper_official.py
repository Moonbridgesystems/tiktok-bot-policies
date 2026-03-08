"""
Official TikTok API Integration
For safe, legal real-time data collection
"""
import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import config
from bot.analyzer import CommentAnalyzer


class OfficialTikTokScraper:
    """
    Uses TikTok's official API for data collection
    Requires: API credentials from https://developers.tiktok.com/
    """
    
    def __init__(self):
        """Initialize official API scraper"""
        self.analyzer = CommentAnalyzer()
        self.client_key = os.getenv('TIKTOK_CLIENT_KEY')
        self.client_secret = os.getenv('TIKTOK_CLIENT_SECRET')
        self.access_token = None
        
        if not self.client_key or not self.client_secret:
            print("⚠️  WARNING: TikTok API credentials not found!")
            print("   Set TIKTOK_CLIENT_KEY and TIKTOK_CLIENT_SECRET in .env file")
            print("   Get credentials from: https://developers.tiktok.com/")
            self.api_available = False
        else:
            self.api_available = True
            self._authenticate()
    
    def _authenticate(self):
        """Get access token using client credentials"""
        try:
            url = "https://open-api.tiktok.com/oauth/access_token/"
            
            params = {
                'client_key': self.client_key,
                'client_secret': self.client_secret,
                'grant_type': 'client_credentials'
            }
            
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            if 'access_token' in data:
                self.access_token = data['access_token']
                print("✅ Successfully authenticated with TikTok Official API")
            else:
                print("❌ Failed to get access token:", data)
                self.api_available = False
                
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            self.api_available = False
    
    def search_videos(self, keyword: str, max_count: int = 20) -> List[Dict]:
        """
        Search for videos using official API
        
        Args:
            keyword: Search keyword or hashtag
            max_count: Maximum number of videos
            
        Returns:
            List of video data dictionaries
        """
        if not self.api_available:
            print(f"⚠️  API not available, skipping: {keyword}")
            return []
        
        videos = []
        try:
            # Official API endpoint for video search
            # Note: Actual endpoint may vary based on your API access level
            url = "https://open-api.tiktok.com/video/search/"
            
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            params = {
                'keyword': keyword.replace('#', ''),
                'count': max_count,
                'max_cursor': 0
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data and 'videos' in data['data']:
                for video in data['data']['videos']:
                    video_data = self._extract_video_data(video)
                    if video_data and self._is_recent_video(video_data['post_time']):
                        videos.append(video_data)
            
            print(f"✅ Found {len(videos)} videos for {keyword}")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API request error for {keyword}: {e}")
        except Exception as e:
            print(f"❌ Error searching {keyword}: {e}")
        
        return videos
    
    def _extract_video_data(self, video: Dict) -> Optional[Dict]:
        """Extract video data from API response"""
        try:
            video_id = video.get('id')
            
            # Construct video link
            video_link = video.get('share_url') or f"https://www.tiktok.com/video/{video_id}"
            
            # Get statistics
            stats = video.get('statistics', {})
           
            # Get post time
            create_time = video.get('create_time', 0)
            post_time = datetime.fromtimestamp(create_time)
            
            return {
                'video_id': video_id,
                'video_link': video_link,
                'thumbnail_url': video.get('cover', {}).get('url_list', [''])[0],
                'views': stats.get('play_count', 0),
                'likes': stats.get('digg_count', 0),
                'total_comments': stats.get('comment_count', 0),
                'post_time': post_time.isoformat(),
                'author': video.get('author', {}).get('unique_id', 'unknown'),
            }
        except Exception as e:
            print(f"❌ Error extracting video data: {e}")
            return None
    
    def _is_recent_video(self, post_time_str: str, hours: int = 24) -> bool:
        """Check if video is within time range"""
        try:
            post_time = datetime.fromisoformat(post_time_str)
            cutoff_time = datetime.now() - timedelta(hours=hours)
            return post_time >= cutoff_time
        except:
            return True  # Include if we can't determine
    
    def get_video_comments(self, video_id: str, max_count: int = 100) -> List[str]:
        """
        Get comments from a video using official API
        
        Args:
            video_id: TikTok video ID
            max_count: Maximum comments to retrieve
            
        Returns:
            List of comment texts
        """
        if not self.api_available:
            return []
        
        comments = []
        try:
            url = f"https://open-api.tiktok.com/video/comment/list/"
            
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            params = {
                'video_id': video_id,
                'count': max_count,
                'cursor': 0
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data and 'comments' in data['data']:
                for comment in data['data']['comments']:
                    if 'text' in comment:
                        comments.append(comment['text'])
            
        except Exception as e:
            print(f"❌ Error getting comments for {video_id}: {e}")
        
        return comments
    
    def analyze_video_comments(self, video_id: str) -> int:
        """
        Get and analyze comments for product inquiries
        
        Args:
            video_id: TikTok video ID
            
        Returns:
            Number of product inquiry comments
        """
        comments = self.get_video_comments(video_id, config.MAX_COMMENTS_PER_VIDEO)
        return self.analyzer.count_product_inquiries(comments)
    
    def scrape_clothing_videos(self) -> List[Dict]:
        """
        Scrape clothing-related videos using official API
        
        Returns:
            List of video data dictionaries with analysis
        """
        if not self.api_available:
            print("\n❌ Official TikTok API not available")
            print("📖 See REALTIME_SETUP.md for configuration instructions")
            return []
        
        all_videos = []
        
        print(f"\n🔍 Starting official API scrape for {len(config.SEARCH_KEYWORDS)} keywords...")
        
        for keyword in config.SEARCH_KEYWORDS:
            print(f"\n📱 Searching: {keyword}")
            videos = self.search_videos(keyword, config.MAX_VIDEOS_PER_KEYWORD)
            
            for video in videos:
                print(f"  💬 Analyzing: {video['video_id']}")
                
                # Analyze comments for product inquiries
                product_inquiry_count = self.analyze_video_comments(video['video_id'])
                video['product_inquiry_comments'] = product_inquiry_count
                
                all_videos.append(video)
                
                # Rate limiting
                import time
                time.sleep(1)  # Be respectful with official API
        
        print(f"\n✅ Scrape complete. Found {len(all_videos)} videos.")
        return all_videos
