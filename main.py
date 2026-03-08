"""
Main script for TikTok Viral Clothing Bot

This script coordinates the scraping, analysis, and storage of TikTok videos.
"""
import time
import argparse
from datetime import datetime
from bot.database import Database
import config


def get_scraper():
    """
    Get the appropriate scraper based on configuration
    
    Returns:
        Scraper instance based on DATA_SOURCE setting
    """
    data_source = config.DATA_SOURCE.lower()
    
    print(f"\n[DATA SOURCE] {data_source.upper()}")
    
    if data_source == 'official':
        print("   Using Official TikTok API")
        from bot.scraper_official import OfficialTikTokScraper
        return OfficialTikTokScraper()
    
    elif data_source == 'apify':
        print("   Using Apify Cloud Service")
        from bot.scraper_apify import ApifyTikTokScraper
        return ApifyTikTokScraper()
    
    elif data_source == 'csv':
        print("   Using CSV Import")
        from bot.csv_importer import CSVImporter
        return CSVImporter()
    
    else:  # demo or any other value
        print("   Using Demo Mode (sample data)")
        from bot.scraper import TikTokScraper
        return TikTokScraper()


def run_scrape():
    """Run a single scraping session"""
    print("=" * 60)
    print(f"TikTok Viral Clothing Bot - Scraping Session")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Initialize components
    scraper = get_scraper()
    db = Database()
    
    # Clean up old videos (older than 24 hours)
    print("\nCleaning up old videos...")
    deleted_count = db.delete_old_videos(config.TIME_RANGE_HOURS)
    print(f"Deleted {deleted_count} old videos")
    
    # Scrape new videos
    print("\nCollecting TikTok videos...")
    
    # Handle CSV import differently
    if config.DATA_SOURCE.lower() == 'csv':
        videos = scraper.import_all_csv_files()
    else:
        videos = scraper.scrape_clothing_videos()
    
    # Save videos to database
    print("\nSaving videos to database...")
    saved_count = 0
    for video in videos:
        if db.save_video(video):
            saved_count += 1
    
    print(f"\nSuccessfully saved {saved_count} videos to database")
    
    # Display summary
    print("\n" + "=" * 60)
    print("SCRAPING SUMMARY")
    print("=" * 60)
    total_videos = db.get_video_count()
    print(f"Total videos in database: {total_videos}")
    
    if videos:
        top_videos = sorted(videos, key=lambda x: x.get('product_inquiry_comments', 0), reverse=True)[:5]
        print("\nTop 5 videos by product inquiries:")
        for i, video in enumerate(top_videos, 1):
            print(f"  {i}. {video['product_inquiry_comments']} inquiries - {video['video_link']}")
    
    print("=" * 60)
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)


def run_continuous():
    """Run the bot continuously with periodic refreshes"""
    print("Starting TikTok Viral Clothing Bot in continuous mode")
    print(f"Refresh interval: {config.REFRESH_INTERVAL_MINUTES} minutes")
    print("Press Ctrl+C to stop")
    print()
    
    while True:
        try:
            run_scrape()
            
            # Wait for next refresh
            print(f"\nWaiting {config.REFRESH_INTERVAL_MINUTES} minutes until next scrape...")
            time.sleep(config.REFRESH_INTERVAL_MINUTES * 60)
            
        except KeyboardInterrupt:
            print("\n\nBot stopped by user")
            break
        except Exception as e:
            print(f"\nError during scraping: {e}")
            print(f"Retrying in {config.REFRESH_INTERVAL_MINUTES} minutes...")
            time.sleep(config.REFRESH_INTERVAL_MINUTES * 60)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='TikTok Viral Clothing Video Finder Bot')
    parser.add_argument(
        '--mode',
        choices=['once', 'continuous'],
        default='once',
        help='Run mode: once (single scrape) or continuous (periodic scraping)'
    )
    parser.add_argument(
        '--dashboard',
        action='store_true',
        help='Start the dashboard instead of running the bot'
    )
    
    args = parser.parse_args()
    
    if args.dashboard:
        # Start the dashboard
        from dashboard.app import run_dashboard
        run_dashboard()
    elif args.mode == 'once':
        # Run single scrape
        run_scrape()
    else:
        # Run continuous mode
        run_continuous()


if __name__ == '__main__':
    main()
