"""
Apify Integration for Safe TikTok Scraping
Easy, cloud-based, legal data collection
"""
import os
import requests
import time
from datetime import datetime, timedelta
from typing import List, Dict
import config
from bot.analyzer import CommentAnalyzer


class ApifyTikTokScraper:
    """
    Uses Apify's cloud service for safe TikTok scraping
    Requires: API token from https://apify.com
    
    Advantages:
    - No proxy setup needed
    - Handles rate limiting automatically
    - Legal and safe
    - Easy to use
    """
    
    def __init__(self):
        """Initialize Apify scraper"""
        self.analyzer = CommentAnalyzer()
        self.api_token = os.getenv('APIFY_API_TOKEN')
        self.base_url = "https://api.apify.com/v2"
        
        if not self.api_token:
            print("⚠️  WARNING: Apify API token not found!")
            print("   Set APIFY_API_TOKEN in .env file")
            print("   Get token from: https://console.apify.com/account/integrations")
            self.api_available = False
        else:
            self.api_available = True
            print("✅ Apify API configured")
    
    def search_videos(self, keyword: str, max_count: int = 20) -> List[Dict]:
        """
        Search for TikTok videos using Apify
        
        Args:
            keyword: Search keyword or hashtag
            max_count: Maximum number of videos
            
        Returns:
            List of video dictionaries
        """
        if not self.api_available:
            print(f"⚠️  Apify not available, skipping: {keyword}")
            return []
        
        videos = []
        try:
            # Apify TikTok Scraper actor ID
            actor_id = "apify/tiktok-scraper"
            
            # Prepare scraper input
            scraper_input = {
                "hashtags": [keyword.replace('#', '')],
                "resultsPerPage": max_count,
                "shouldDownloadVideos": False,
                "shouldDownloadCovers": True,
                "shouldDownloadSubtitles": False,
            }
            
            # Start the scraper
            print(f"🚀 Starting Apify scraper for: {keyword}")
            run_url = f"{self.base_url}/acts/{actor_id}/runs?token={self.api_token}"
            
            response = requests.post(run_url, json=scraper_input)
            response.raise_for_status()
            
            run_data = response.json()
            run_id = run_data['data']['id']
            
            # Wait for results
            print(f"⏳ Waiting for results...")
            dataset_id = self._wait_for_run(run_id)
            
            if dataset_id:
                # Get results
                videos = self._get_dataset_items(dataset_id)
                print(f"✅ Found {len(videos)} videos for {keyword}")
            
        except Exception as e:
            print(f"❌ Apify error for {keyword}: {e}")
        
        return videos
    
    def _wait_for_run(self, run_id: str, max_wait: int = 300) -> str:
        """Wait for Apify run to complete"""
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            try:
                url = f"{self.base_url}/actor-runs/{run_id}?token={self.api_token}"
                response = requests.get(url)
                response.raise_for_status()
                
                data = response.json()
                status = data['data']['status']
                
                if status == 'SUCCEEDED':
                    return data['data']['defaultDatasetId']
                elif status in ['FAILED', 'ABORTED', 'TIMED-OUT']:
                    print(f"❌ Run {status}")
                    return None
                
                # Still running
                time.sleep(5)
                
            except Exception as e:
                print(f"❌ Error checking run status: {e}")
                return None
        
        print(f"⏱️  Timeout waiting for run")
        return None
    
    def _get_dataset_items(self, dataset_id: str) -> List[Dict]:
        """Get items from Apify dataset"""
        try:
            url = f"{self.base_url}/datasets/{dataset_id}/items?token={self.api_token}"
            response = requests.get(url)
            response.raise_for_status()
            
            items = response.json()
            videos = []
            
            for item in items:
                video_data = self._extract_video_data(item)
                if video_data and self._is_recent_video(video_data['post_time']):
                    videos.append(video_data)
            
            return videos
            
        except Exception as e:
            print(f"❌ Error getting dataset: {e}")
            return []
    
    def _extract_video_data(self, item: Dict) -> Dict:
        """Extract video data from Apify result"""
        try:
            return {
                'video_id': item.get('id', ''),
                'video_link': item.get('webVideoUrl', ''),
                'thumbnail_url': item.get('videoMeta', {}).get('coverUrl', ''),
                'views': item.get('playCount', 0),
                'likes': item.get('diggCount', 0),
                'total_comments': item.get('commentCount', 0),
                'post_time': datetime.fromtimestamp(item.get('createTime', 0)).isoformat(),
                'author': item.get('authorMeta', {}).get('name', 'unknown'),
            }
        except Exception as e:
            print(f"❌ Error extracting video data: {e}")
            return None
    
    def _is_recent_video(self, post_time_str: str, hours: int = 24) -> bool:
        """Check if video is recent"""
        try:
            post_time = datetime.fromisoformat(post_time_str)
            cutoff_time = datetime.now() - timedelta(hours=hours)
            return post_time >= cutoff_time
        except:
            return True
    
    def get_video_comments(self, video_id: str, max_count: int = 100) -> List[str]:
        """
        Get comments from a video
        Note: Apify scraper can get comments, but may require separate run
        """
        # For simplicity, return empty list
        # In production, you'd run another Apify actor to get comments
        return []
    
    def analyze_video_comments(self, video_id: str) -> int:
        """Analyze comments (placeholder for Apify)"""
        # Apify can scrape comments, but requires additional setup
        # For now, return 0 or implement comment scraping
        return 0
    
    def scrape_clothing_videos(self) -> List[Dict]:
        """
        Scrape clothing videos using Apify
        
        Returns:
            List of video data dictionaries
        """
        if not self.api_available:
            print("\n❌ Apify API not configured")
            print("📖 See REALTIME_SETUP.md for setup instructions")
            return []
        
        all_videos = []
        
        print(f"\n🔍 Starting Apify scrape for {len(config.SEARCH_KEYWORDS)} keywords...")
        print(f"💰 Note: Apify usage will be billed to your account")
        
        for keyword in config.SEARCH_KEYWORDS:
            videos = self.search_videos(keyword, config.MAX_VIDEOS_PER_KEYWORD)
            
            # Since Apify doesn't easily get comments, estimate product inquiries
            for video in videos:
                # Simple estimation based on comment ratio
                # In production, you'd run a separate comment scraper
                estimated_inquiries = int(video['total_comments'] * 0.05)  # ~5% inquiry rate
                video['product_inquiry_comments'] = estimated_inquiries
            
            all_videos.extend(videos)
        
        print(f"\n✅ Apify scrape complete. Found {len(all_videos)} videos.")
        return all_videos
