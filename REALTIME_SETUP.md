# 🔐 Safe Real-Time TikTok Data Collection Guide

This guide explains **safe and legal methods** to collect real TikTok data for your bot.

---

## ⚠️ IMPORTANT: Legal & Ethical Considerations

**Before proceeding:**
- ✅ Only collect publicly available data
- ✅ Respect TikTok's Terms of Service
- ✅ Use rate limiting to avoid overloading servers
- ✅ Consider using official APIs when available
- ❌ Never scrape private or restricted content
- ❌ Don't sell or misuse collected data

---

## 🎯 Recommended Methods (Safest to Less Safe)

### Method 1: Official TikTok API ⭐ RECOMMENDED
**Safety Level: ✅✅✅✅✅ (100% Safe & Legal)**

TikTok offers official APIs for developers:

#### Option A: TikTok for Developers API
- **Website**: https://developers.tiktok.com/
- **Access**: Requires application approval
- **Features**: 
  - Official video search
  - User data (public)
  - Hashtag data
  - Comments (if permitted)
- **Rate Limits**: Generous, clearly defined
- **Cost**: Free tier available

**Setup Steps:**
1. Go to https://developers.tiktok.com/
2. Create developer account
3. Apply for API access
4. Get Client Key and Client Secret
5. Configure in `.env` file (see below)

#### Option B: TikTok Research API
- **Website**: https://developers.tiktok.com/products/research-api/
- **Access**: For academic researchers
- **Features**: Enhanced data access for research
- **Requirements**: Must be affiliated with academic institution

---

### Method 2: Unofficial APIs with Rate Limiting ⚠️
**Safety Level: ✅✅✅ (Safe with precautions)**

Use unofficial libraries with proper configuration:

#### Apify TikTok Scraper (Recommended Unofficial)
- **Service**: https://apify.com/apify/tiktok-scraper
- **Safety**: Cloud-based, handles rate limiting
- **Cost**: Pay per use (~$5-50/month depending on volume)
- **Setup**: Simple API integration

#### RapidAPI TikTok APIs
- **Service**: https://rapidapi.com/hub
- **Search for**: "TikTok API"
- **Safety**: Professional APIs with rate limiting
- **Cost**: Various pricing tiers

---

### Method 3: Enhanced TikTokApi Library with Safety
**Safety Level: ✅✅ (Moderate - requires careful setup)**

Use the existing TikTokApi with safety enhancements:

**Requirements:**
- Residential proxies (not datacenter IPs)
- Realistic delays between requests
- Cookie rotation
- Browser fingerprinting

---

### Method 4: Manual Data Collection + Automation
**Safety Level: ✅✅✅✅ (Very Safe)**

Semi-automated approach:
- Use browser extension to export data
- Import CSV files into the bot
- Combines manual oversight with automation

---

## 🛠️ Implementation Guide

### Setup 1: Official TikTok API (Recommended)

#### Step 1: Get API Credentials

1. Visit https://developers.tiktok.com/
2. Create an app
3. Get your credentials:
   - Client Key
   - Client Secret

#### Step 2: Configure Environment Variables

Create a `.env` file in the project root:

```env
# TikTok Official API Credentials
TIKTOK_CLIENT_KEY=your_client_key_here
TIKTOK_CLIENT_SECRET=your_client_secret_here

# Optional: For unofficial methods
TIKTOK_PROXY_URL=http://your-proxy-server:port
TIKTOK_PROXY_USERNAME=username
TIKTOK_PROXY_PASSWORD=password

# Apify API (if using)
APIFY_API_TOKEN=your_apify_token_here

# RapidAPI (if using)
RAPIDAPI_KEY=your_rapidapi_key_here
```

#### Step 3: Use Updated Scraper

The bot now supports multiple data sources (see updated code below).

---

### Setup 2: Apify Integration (Quick & Easy)

**Advantages:**
- ✅ No technical setup needed
- ✅ Cloud-based scraping
- ✅ Legal and safe
- ✅ Handles rate limiting

**Steps:**

1. **Sign up**: https://apify.com (Free trial available)

2. **Get API Token**: 
   - Go to Settings → Integrations
   - Copy your API token

3. **Add to `.env`**:
   ```env
   APIFY_API_TOKEN=your_token_here
   ```

4. **Enable in config.py**:
   ```python
   USE_APIFY = True
   ```

**Cost Estimate:**
- Free tier: $5 credit
- Typical usage: ~$10-30/month for moderate scraping

---

### Setup 3: RapidAPI Integration

**Steps:**

1. **Visit**: https://rapidapi.com/
2. **Search**: "TikTok API"
3. **Subscribe** to an API (many have free tiers)
4. **Get API Key**
5. **Add to `.env`**:
   ```env
   RAPIDAPI_KEY=your_key_here
   RAPIDAPI_HOST=tiktok-api-host.rapidapi.com
   ```

---

### Setup 4: Safe Unofficial Scraping (Advanced)

**Requirements:**
- ✅ Residential proxies (recommended services):
  - Bright Data (https://brightdata.com)
  - Smartproxy (https://smartproxy.com)
  - Oxylabs (https://oxylabs.io)
  
**Configuration:**

```env
# Proxy Configuration
PROXY_ENABLED=true
PROXY_URL=http://your-proxy:port
PROXY_USERNAME=username
PROXY_PASSWORD=password

# Rate Limiting (requests per minute)
MAX_REQUESTS_PER_MINUTE=10
DELAY_BETWEEN_REQUESTS=6
```

**Cost Estimate:**
- Residential proxies: $50-200/month

---

## 🚀 Quick Start (Easiest Method)

### Option A: Apify (No Technical Setup)

```bash
# 1. Sign up at https://apify.com
# 2. Get API token
# 3. Create .env file:
echo APIFY_API_TOKEN=your_token > .env

# 4. Update config.py:
#    USE_APIFY = True

# 5. Run bot:
python main.py --mode once
```

### Option B: Official API (Best Long-term)

```bash
# 1. Apply at https://developers.tiktok.com/
# 2. Wait for approval (can take days/weeks)
# 3. Get credentials
# 4. Create .env file:
echo TIKTOK_CLIENT_KEY=your_key > .env
echo TIKTOK_CLIENT_SECRET=your_secret >> .env

# 5. Update config.py:
#    USE_OFFICIAL_API = True

# 6. Run bot:
python main.py --mode once
```

---

## 📊 Comparison Table

| Method | Safety | Cost/Month | Setup Time | Data Quality | Rate Limits |
|--------|--------|------------|------------|--------------|-------------|
| Official API | ⭐⭐⭐⭐⭐ | Free-$$ | 1-2 weeks | Excellent | High |
| Apify | ⭐⭐⭐⭐⭐ | $10-50 | 5 minutes | Excellent | High |
| RapidAPI | ⭐⭐⭐⭐ | $0-30 | 10 minutes | Good | Medium |
| Proxies + TikTokApi | ⭐⭐⭐ | $50-200 | 1-2 hours | Good | Low-Medium |
| Manual + CSV | ⭐⭐⭐⭐⭐ | Free | Ongoing | Excellent | None |

---

## 🔒 Safety Best Practices

### 1. Rate Limiting
```python
# Always use delays
import time
time.sleep(2)  # 2 seconds between requests

# Limit requests per hour
MAX_REQUESTS_PER_HOUR = 100
```

### 2. User Agent Rotation
```python
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
]
```

### 3. Proxy Rotation
- Use residential proxies (not datacenter)
- Rotate IPs regularly
- Use proxy pools

### 4. Error Handling
```python
# Graceful fallback
try:
    data = scrape_tiktok()
except RateLimitError:
    time.sleep(300)  # Wait 5 minutes
    data = scrape_tiktok()
```

### 5. Respect robots.txt
- Check TikTok's robots.txt: https://www.tiktok.com/robots.txt
- Don't scrape disallowed paths

---

## 🎯 Recommended Setup for This Bot

### For Small-Scale Use (< 100 videos/day)
**Best Method**: Apify or RapidAPI
- Easy setup
- Safe and legal
- Affordable

### For Medium-Scale Use (100-1000 videos/day)
**Best Method**: Official TikTok API
- Apply for developer access
- Most reliable
- Free or low cost

### For Large-Scale Use (1000+ videos/day)
**Best Method**: Official TikTok API + Paid Plan
- Enterprise API access
- Custom rate limits
- Support included

### For Research/Academic Use
**Best Method**: TikTok Research API
- Specifically designed for research
- Enhanced data access
- Free for qualified researchers

---

## 📝 Code Updates

I've updated the bot with:

1. ✅ **Environment variable support** (.env file)
2. ✅ **Apify integration** (easiest method)
3. ✅ **RapidAPI support**
4. ✅ **Official API template**
5. ✅ **Enhanced rate limiting**
6. ✅ **Proxy support**
7. ✅ **CSV import option**

See updated files:
- `bot/scraper_official.py` - Official API implementation
- `bot/scraper_apify.py` - Apify integration
- `bot/scraper_safe.py` - Safe unofficial scraping
- `bot/csv_importer.py` - Manual data import
- `config.py` - Updated configuration options

---

## 🆘 Support & Resources

### Official Documentation
- TikTok Developers: https://developers.tiktok.com/
- TikTok API Docs: https://developers.tiktok.com/doc/overview

### Alternative Services
- Apify TikTok Scraper: https://apify.com/apify/tiktok-scraper
- RapidAPI Hub: https://rapidapi.com/hub

### Proxy Providers (for safe unofficial scraping)
- Bright Data: https://brightdata.com
- Smartproxy: https://smartproxy.com
- Oxylabs: https://oxylabs.io

### Support Communities
- r/TikTokDevelopers (Reddit)
- TikTok Developer Forums
- Stack Overflow

---

## ⚡ Quick Decision Guide

**Choose your path:**

1. **"I need it working in 5 minutes"**
   → Use Apify ($10-30/month)

2. **"I want the safest, most legal method"**
   → Apply for Official TikTok API (free, takes 1-2 weeks)

3. **"I'm on a tight budget"**
   → Use RapidAPI free tier or CSV import

4. **"I need high volume data"**
   → Official API + Paid plan

5. **"I'm doing academic research"**
   → Apply for TikTok Research API

---

## 🎓 Next Steps

1. Choose a method from above
2. Follow the setup guide
3. Get API credentials
4. Create `.env` file
5. Update `config.py`
6. Run `python main.py --mode once`
7. Check dashboard at http://localhost:5000

**Need help?** Check the detailed implementation in the updated bot files!

---

**Remember**: Always respect TikTok's Terms of Service and use data responsibly! 🙏
