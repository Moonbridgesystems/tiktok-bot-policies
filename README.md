# 🎯 TikTok Viral Clothing Video Finder

A Python bot that discovers viral TikTok videos related to clothing from the last 24 hours and identifies videos where people are asking about where to buy the clothing items. Features a simple web dashboard to view and analyze results.

## 📋 Features

- **Video Discovery**: Finds TikTok videos posted within the last 24 hours using fashion-related hashtags
- **Comment Analysis**: Detects product inquiry comments (e.g., "where can I buy this?")
- **Ranking System**: Ranks videos by product inquiry engagement
- **Web Dashboard**: Simple, beautiful interface to view and sort results
- **Auto-Refresh**: Periodic scanning for new viral content
- **SQLite Database**: Lightweight data storage

## 🏗️ Project Structure

```
TikTok Viral Clothing bot/
├── bot/
│   ├── __init__.py
│   ├── scraper.py          # TikTok scraping logic
│   ├── analyzer.py         # Comment analysis
│   └── database.py         # Database operations
├── dashboard/
│   ├── __init__.py
│   ├── app.py              # Flask application
│   └── templates/
│       └── index.html      # Dashboard UI
├── data/
│   └── videos.db           # SQLite database (auto-created)
├── config.py               # Configuration settings
├── main.py                 # Main bot script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download

Navigate to the project directory:
```bash
cd "C:\Users\Asif Computer\Desktop\TikTok Viral Clothing bot"
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Playwright (for TikTokApi)

```bash
playwright install
```

## ⚙️ Configuration

Edit `config.py` to customize settings:

- **SEARCH_KEYWORDS**: Hashtags to search for (default: #fashion, #clothing, etc.)
- **TIME_RANGE_HOURS**: How far back to search (default: 24 hours)
- **INQUIRY_PHRASES**: Phrases to detect in comments
- **MAX_VIDEOS_PER_KEYWORD**: Maximum videos per hashtag search
- **REFRESH_INTERVAL_MINUTES**: How often to refresh data (default: 30 minutes)

## 📊 Usage

### Option 1: Run Bot Once

Run a single scraping session:

```bash
python main.py --mode once
```

### Option 2: Run Bot Continuously

Run with automatic periodic refreshes:

```bash
python main.py --mode continuous
```

This will scrape new videos every 30 minutes (configurable in `config.py`).

### Option 3: Start Dashboard Only

Launch the web dashboard without running the bot:

```bash
python main.py --dashboard
```

Or directly:

```bash
python dashboard/app.py
```

Then open your browser to: **http://localhost:5000**

### Recommended Workflow

**Terminal 1** - Run the bot continuously:
```bash
python main.py --mode continuous
```

**Terminal 2** - Run the dashboard:
```bash
python main.py --dashboard
```

Then visit **http://localhost:5000** to view the dashboard.

## 🎨 Dashboard Features

The dashboard displays:

- **Video Thumbnail**: Visual preview of the TikTok video
- **Video Link**: Clickable link to open the video on TikTok
- **Views**: Number of views
- **Likes**: Number of likes
- **Total Comments**: Total comment count
- **Product Inquiry Comments**: Number of comments asking about the product
- **Inquiry Rate**: Percentage of comments that are product inquiries
- **Post Time**: When the video was posted

### Sorting Options

Click the buttons to sort by:
- 🔥 **Product Inquiries** (default) - Videos with most product questions
- 👁️ **Views** - Most viewed videos
- ❤️ **Likes** - Most liked videos

### Auto-Refresh

The dashboard automatically refreshes every 60 seconds to show the latest data.

## 🔧 Troubleshooting

### TikTok API Issues

TikTok actively blocks automated scraping. If you encounter issues:

1. **Demo Mode**: The bot includes demo data generation for testing
2. **Rate Limiting**: Increase delays between requests in `scraper.py`
3. **Proxies**: Consider using proxy services (requires additional configuration)
4. **Alternative Methods**: You may need to use Selenium with browser automation

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'TikTokApi'`
- **Solution**: Run `pip install -r requirements.txt`

**Issue**: `Playwright not installed`
- **Solution**: Run `playwright install`

**Issue**: No videos appearing on dashboard
- **Solution**: Make sure you've run the bot first (`python main.py --mode once`)

**Issue**: Dashboard not loading
- **Solution**: Check if port 5000 is already in use. Change `DASHBOARD_PORT` in `config.py`

## 📝 How It Works

1. **Scraping**: The bot searches TikTok for videos using fashion-related hashtags from the last 24 hours
2. **Data Collection**: For each video, it collects:
   - Video link and thumbnail
   - Views, likes, comment count
   - Post timestamp
3. **Comment Analysis**: It fetches comments and searches for product inquiry phrases like:
   - "where can I buy this"
   - "where is this from"
   - "w2c" (where to cop)
4. **Storage**: Data is saved to a SQLite database
5. **Dashboard**: Flask serves a web interface to view and sort the results
6. **Cleanup**: Videos older than 24 hours are automatically removed

## 🎯 Product Inquiry Detection

The bot detects these common phrases in comments:

- "where does this"
- "where can i buy"
- "where is this from"
- "where did you get"
- "where to buy"
- "link to"
- "w2c" (where to cop)
- "where to cop"
- "what brand"
- "where from"

You can customize these in `config.py` by editing the `INQUIRY_PHRASES` list.

## 🔐 Important Notes

### TikTok Terms of Service

- This bot is for educational and research purposes
- TikTok may block or rate-limit automated access
- Consider using official TikTok API if available for your use case
- Respect TikTok's robots.txt and terms of service

### Data Privacy

- The bot only collects publicly available data
- No user authentication or personal data is stored
- Only video IDs, public metrics, and public comments are collected

## 📦 Database Schema

The SQLite database contains one table:

**videos** table:
- `id`: Auto-incrementing primary key
- `video_id`: Unique TikTok video identifier
- `video_link`: Full URL to the video
- `thumbnail_url`: URL to video thumbnail image
- `views`: View count
- `likes`: Like count
- `total_comments`: Total number of comments
- `product_inquiry_comments`: Number of product inquiry comments
- `post_time`: When the video was posted
- `scraped_time`: When the bot found this video
- `last_updated`: Last update timestamp

## 🛠️ Customization

### Add More Keywords

Edit `config.py`:

```python
SEARCH_KEYWORDS = [
    '#fashion',
    '#clothing',
    '#yourhashtag',  # Add your custom hashtags
]
```

### Change Inquiry Phrases

Edit `config.py`:

```python
INQUIRY_PHRASES = [
    'where can i buy',
    'your custom phrase',  # Add custom phrases
]
```

### Adjust Scraping Limits

Edit `config.py`:

```python
MAX_VIDEOS_PER_KEYWORD = 50  # Increase or decrease
MAX_COMMENTS_PER_VIDEO = 200  # Increase or decrease
```

## 🚀 Advanced Usage

### Running on a Server

To run on a server (accessible from other devices):

1. Edit `config.py`:
```python
DASHBOARD_HOST = '0.0.0.0'  # Listen on all interfaces
DASHBOARD_PORT = 5000
```

2. Start the dashboard:
```bash
python main.py --dashboard
```

3. Access from other devices: `http://YOUR_SERVER_IP:5000`

### Automated Scheduling

Use Task Scheduler (Windows) or cron (Linux/Mac) to run the bot automatically:

**Windows Task Scheduler**:
- Create a new task
- Set trigger (e.g., every hour)
- Action: `python "C:\Users\Asif Computer\Desktop\TikTok Viral Clothing bot\main.py" --mode once`

**Linux/Mac Cron**:
```bash
# Run every hour
0 * * * * cd /path/to/bot && python main.py --mode once
```

## 📈 Performance Tips

1. **Rate Limiting**: Add delays between requests to avoid being blocked
2. **Proxy Rotation**: Use rotating proxies for large-scale scraping
3. **Database Optimization**: Add indexes for faster queries on large datasets
4. **Concurrent Scraping**: Implement threading for faster data collection
5. **Caching**: Cache thumbnails locally to reduce bandwidth

## 🤝 Contributing

This is a simple educational project. Feel free to:

- Add new features
- Improve the scraping logic
- Enhance the dashboard UI
- Add export functionality (CSV, JSON)
- Implement better error handling

## 📄 License

This project is provided as-is for educational purposes. Use responsibly and in accordance with TikTok's terms of service.

## ⚠️ Disclaimer

This tool is for educational and research purposes only. The authors are not responsible for any misuse or violation of TikTok's terms of service. Always respect the platform's rules and regulations.

---

**Happy Scraping! 🎉**

For questions or issues, check the troubleshooting section above.
