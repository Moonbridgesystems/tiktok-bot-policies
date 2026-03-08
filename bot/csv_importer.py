"""
CSV Importer for Manual Data Collection
Safe method: manually collect data and import via CSV
"""
import csv
from datetime import datetime
from typing import List, Dict
import os
from bot.analyzer import CommentAnalyzer


class CSVImporter:
    """
    Import TikTok video data from CSV files
    
    This is the safest method - manually collect data from TikTok
    and import it into the bot.
    
    CSV Format:
    video_id,video_link,thumbnail_url,views,likes,total_comments,post_time,comments
    """
    
    def __init__(self):
        """Initialize CSV importer"""
        self.analyzer = CommentAnalyzer()
        self.csv_folder = os.path.join(os.path.dirname(__file__), '..', 'import_data')
        
        # Create import folder if it doesn't exist
        if not os.path.exists(self.csv_folder):
            os.makedirs(self.csv_folder)
            print(f"📁 Created import folder: {self.csv_folder}")
    
    def import_from_csv(self, csv_file: str) -> List[Dict]:
        """
        Import videos from CSVfile
        
        Args:
            csv_file: Path to CSV file or filename in import_data folder
            
        Returns:
            List of video dictionaries
        """
        # Check if file exists
        if not os.path.isabs(csv_file):
            csv_file = os.path.join(self.csv_folder, csv_file)
        
        if not os.path.exists(csv_file):
            print(f"❌ CSV file not found: {csv_file}")
            return []
        
        videos = []
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    video_data = self._process_row(row)
                    if video_data:
                        videos.append(video_data)
            
            print(f"✅ Imported {len(videos)} videos from {os.path.basename(csv_file)}")
            
        except Exception as e:
            print(f"❌ Error importing CSV: {e}")
        
        return videos
    
    def _process_row(self, row: Dict) -> Dict:
        """Process a CSV row into video data"""
        try:
            video_id = row.get('video_id', '')
            
            # Required fields
            if not video_id or not row.get('video_link'):
                return None
            
            # Extract comments if provided
            comments_text = row.get('comments', '')
            comments = []
            if comments_text:
                # Comments can be separated by | or newlines
                comments = [c.strip() for c in comments_text.split('|') if c.strip()]
            
            # Analyze comments for product inquiries
            product_inquiry_count = self.analyzer.count_product_inquiries(comments)
            
            return {
                'video_id': video_id,
                'video_link': row.get('video_link', ''),
                'thumbnail_url': row.get('thumbnail_url', ''),
                'views': int(row.get('views', 0)),
                'likes': int(row.get('likes', 0)),
                'total_comments': int(row.get('total_comments', len(comments))),
                'product_inquiry_comments': product_inquiry_count,
                'post_time': row.get('post_time', datetime.now().isoformat()),
                'author': row.get('author', 'unknown'),
            }
            
        except Exception as e:
            print(f"❌ Error processing row: {e}")
            return None
    
    def import_all_csv_files(self) -> List[Dict]:
        """
        Import all CSV files from the import_data folder
        
        Returns:
            Combined list of videos from all CSV files
        """
        all_videos = []
        
        # Find all CSV files
        csv_files = [f for f in os.listdir(self.csv_folder) if f.endswith('.csv')]
        
        if not csv_files:
            print(f"📂 No CSV files found in {self.csv_folder}")
            print(f"💡 Create a CSV file with the format shown in csv_template.csv")
            return []
        
        print(f"\n📥 Importing from {len(csv_files)} CSV file(s)...")
        
        for csv_file in csv_files:
            videos = self.import_from_csv(csv_file)
            all_videos.extend(videos)
        
        print(f"\n✅ Total imported: {len(all_videos)} videos")
        return all_videos
    
    def create_template(self):
        """Create a CSV template file for reference"""
        template_file = os.path.join(self.csv_folder, 'csv_template.csv')
        
        try:
            with open(template_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                
                # Header
                writer.writerow([
                    'video_id',
                    'video_link',
                    'thumbnail_url',
                    'views',
                    'likes',
                    'total_comments',
                    'post_time',
                    'author',
                    'comments'
                ])
                
                # Sample data
                writer.writerow([
                    '7123456789',
                    'https://www.tiktok.com/@user/video/7123456789',
                    'https://example.com/thumbnail.jpg',
                    '50000',
                    '3000',
                    '150',
                    datetime.now().isoformat(),
                    'fashionuser',
                    'Love this!|Where can I buy this?|This is amazing!|Link please!'
                ])
                
                writer.writerow([
                    '7123456790',
                    'https://www.tiktok.com/@user2/video/7123456790',
                    'https://example.com/thumbnail2.jpg',
                    '75000',
                    '5000',
                    '200',
                    datetime.now().isoformat(),
                    'styleinfluencer',
                    'So cute!|Where is this from?|Need this outfit|w2c?'
                ])
            
            print(f"✅ Created CSV template: {template_file}")
            print(f"📝 Edit this file or create new CSV files with the same format")
            
        except Exception as e:
            print(f"❌ Error creating template: {e}")


def manual_data_entry():
    """
    Interactive manual data entry
    For adding individual videos manually
    """
    print("\n📝 Manual Video Entry")
    print("=" * 50)
    
    try:
        video_id = input("Video ID (from TikTok URL): ").strip()
        video_link = input("Video Link (full URL): ").strip()
        views = int(input("Views: ").strip() or 0)
        likes = int(input("Likes: ").strip() or 0)
        total_comments = int(input("Total Comments: ").strip() or 0)
        
        print("\nEnter comments (one per line, press Enter twice when done):")
        comments = []
        while True:
            comment = input("> ").strip()
            if not comment:
                break
            comments.append(comment)
        
        # Analyze comments
        analyzer = CommentAnalyzer()
        product_inquiry_count = analyzer.count_product_inquiries(comments)
        
        video_data = {
            'video_id': video_id,
            'video_link': video_link,
            'thumbnail_url': '',
            'views': views,
            'likes': likes,
            'total_comments': total_comments or len(comments),
            'product_inquiry_comments': product_inquiry_count,
            'post_time': datetime.now().isoformat(),
            'author': 'manual_entry',
        }
        
        print(f"\n✅ Video added with {product_inquiry_count} product inquiry comments")
        return video_data
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None
