"""
Configuration settings for TikTok Viral Clothing Bot
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database settings
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'videos.db')

# ========================================
# DATA SOURCE SELECTION
# ========================================
# Choose which scraper to use:
# - 'official': Official TikTok API (safest, requires approval)
# - 'apify': Apify cloud service (easy, paid)
# - 'csv': Manual CSV import (safest, manual work)
# - 'demo': Demo mode with sample data (for testing)

DATA_SOURCE = os.getenv('DATA_SOURCE', 'demo')

# TikTok scraping settings
SEARCH_KEYWORDS = [
    '#fashion',
    '#clothing',
    '#outfit',
    '#ootd',
    '#style',
    '#fashiontiktok',
    '#clothinghaul',
]

# Time range (hours)
TIME_RANGE_HOURS = 24

# Product inquiry phrases to detect in comments
INQUIRY_PHRASES = [
    'where does this',
    'where can i buy',
    'where is this from',
    'where did you get',
    'where to buy',
    'where can i get',
    'link to',
    'w2c',  # common abbreviation for "where to cop"
    'where to cop',
    'what brand',
    'where from',
]

# Scraping limits
MAX_VIDEOS_PER_KEYWORD = 20
MAX_COMMENTS_PER_VIDEO = 100

# Dashboard settings
DASHBOARD_HOST = '0.0.0.0'
DASHBOARD_PORT = 5000

# Refresh interval (minutes)
REFRESH_INTERVAL_MINUTES = 30

# ========================================
# RATE LIMITING (for safety)
# ========================================
MAX_REQUESTS_PER_MINUTE = int(os.getenv('MAX_REQUESTS_PER_MINUTE', 10))
DELAY_BETWEEN_REQUESTS = int(os.getenv('DELAY_BETWEEN_REQUESTS', 6))

# ========================================
# PROXY SETTINGS (optional, for safer scraping)
# ========================================
PROXY_ENABLED = os.getenv('PROXY_ENABLED', 'false').lower() == 'true'
PROXY_URL = os.getenv('PROXY_URL', '')
PROXY_USERNAME = os.getenv('PROXY_USERNAME', '')
PROXY_PASSWORD = os.getenv('PROXY_PASSWORD', '')
