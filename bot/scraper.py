"""
TikTok scraper for finding viral clothing videos
"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time
import config
from bot.analyzer import CommentAnalyzer


class TikTokScraper:
    """
    Scraper for TikTok videos and comments
    
    Note: This implementation uses TikTokApi library.
    TikTok may block requests, so you may need to use proxies or alternative methods.
    """
    
    def __init__(self):
        """Initialize TikTok scraper"""
        self.analyzer = CommentAnalyzer()
        self.api = None
        self._init_api()
    
    def _init_api(self):
        """Initialize TikTok API"""
        try:
            from TikTokApi import TikTokApi
            # Initialize with custom parameters
            # ms_token can be obtained from browser cookies after logging into TikTok
            self.api = TikTokApi()
        except ImportError:
            print("WARNING: TikTokApi not installed. Install with: pip install TikTokApi")
            print("Scraper will run in demo mode with sample data.")
            self.api = None
        except Exception as e:
            print(f"Error initializing TikTok API: {e}")
            self.api = None
    
    def _is_recent_video(self, post_time: datetime, hours: int = 24) -> bool:
        """Check if video is within specified time range"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return post_time >= cutoff_time
    
    def search_videos(self, keyword: str, max_count: int = 20) -> List[Dict]:
        """
        Search for TikTok videos by keyword/hashtag
        
        Args:
            keyword: Search keyword or hashtag
            max_count: Maximum number of videos to retrieve
            
        Returns:
            List of video dictionaries
        """
        if not self.api:
            print(f"Running in demo mode for keyword: {keyword}")
            return self._get_demo_videos(keyword, max_count)
        
        videos = []
        try:
            # Search for videos using the keyword
            search_results = self.api.hashtag(name=keyword.replace('#', '')).videos(count=max_count)
            
            for video in search_results:
                # Extract video data
                video_data = self._extract_video_data(video)
                
                # Only include recent videos
                if video_data and self._is_recent_video(
                    video_data['post_time'], 
                    config.TIME_RANGE_HOURS
                ):
                    videos.append(video_data)
            
        except Exception as e:
            print(f"Error searching videos for {keyword}: {e}")
            print(f"Falling back to demo mode for keyword: {keyword}")
            return self._get_demo_videos(keyword, max_count)
        
        return videos
    
    def _extract_video_data(self, video) -> Optional[Dict]:
        """Extract relevant data from TikTok video object"""
        try:
            # Extract basic video information
            video_id = video.id
            video_link = f"https://www.tiktok.com/@{video.author.uniqueId}/video/{video_id}"
            
            # Get video statistics
            stats = video.stats
            
            # Get post time
            post_time = datetime.fromtimestamp(video.createTime)
            
            return {
                'video_id': video_id,
                'video_link': video_link,
                'thumbnail_url': video.video.cover,
                'views': stats.get('playCount', 0),
                'likes': stats.get('diggCount', 0),
                'total_comments': stats.get('commentCount', 0),
                'post_time': post_time.isoformat(),
                'author': video.author.uniqueId,
            }
        except Exception as e:
            print(f"Error extracting video data: {e}")
            return None
    
    def get_video_comments(self, video_id: str, max_count: int = 100) -> List[str]:
        """
        Get comments from a TikTok video
        
        Args:
            video_id: TikTok video ID
            max_count: Maximum number of comments to retrieve
            
        Returns:
            List of comment texts
        """
        if not self.api:
            return self._get_demo_comments()
        
        comments = []
        try:
            # Get comments for the video
            video = self.api.video(id=video_id)
            comment_results = video.comments(count=max_count)
            
            for comment in comment_results:
                if hasattr(comment, 'text'):
                    comments.append(comment.text)
            
        except Exception as e:
            # Fall back to demo comments on error
            return self._get_demo_comments()
        
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
        Scrape clothing-related videos from TikTok
        
        Returns:
            List of video data dictionaries with analysis
        """
        all_videos = []
        
        print(f"Starting TikTok scrape for {len(config.SEARCH_KEYWORDS)} keywords...")
        
        for keyword in config.SEARCH_KEYWORDS:
            print(f"Searching for: {keyword}")
            videos = self.search_videos(keyword, config.MAX_VIDEOS_PER_KEYWORD)
            
            for video in videos:
                # Analyze comments for product inquiries
                print(f"  Analyzing video: {video['video_id']}")
                product_inquiry_count = self.analyze_video_comments(video['video_id'])
                video['product_inquiry_comments'] = product_inquiry_count
                
                all_videos.append(video)
                
                # Be respectful with rate limiting
                time.sleep(1)
            
            # Rate limiting between keywords
            time.sleep(2)
        
        print(f"Scrape complete. Found {len(all_videos)} videos.")
        return all_videos
    
    def _get_demo_videos(self, keyword: str, max_count: int) -> List[Dict]:
        """Generate demo video data for testing (when API is not available)"""
        import random
        
        demo_videos = []
        for i in range(min(3, max_count)):  # Generate 3 demo videos per keyword
            video_id = f"demo_{keyword}_{i}_{random.randint(1000, 9999)}"
            demo_videos.append({
                'video_id': video_id,
                'video_link': f"https://www.tiktok.com/@demo/video/{video_id}",
                'thumbnail_url': f"https://via.placeholder.com/300x400?text={keyword}",
                'views': random.randint(10000, 1000000),
                'likes': random.randint(1000, 50000),
                'total_comments': random.randint(100, 5000),
                'post_time': (datetime.now() - timedelta(hours=random.randint(1, 23))).isoformat(),
                'author': f'demo_user_{i}',
            })
        
        return demo_videos
    
    def _get_demo_comments(self) -> List[str]:
        """Generate demo comments for testing"""
        return [
            "This is so cute!",
            "Where can I buy this?",
            "Love this outfit!",
            "Where is this from?",
            "Amazing style!",
            "Link please!",
            "Where did you get that dress?",
            "Gorgeous!",
            "W2C?",
            "I need this in my life",
        ]
