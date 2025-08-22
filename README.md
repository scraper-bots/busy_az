# Busy.az Job Seeker Scraper

A Python web scraper to extract candidate information from busy.az job seeker profiles.

## Features

- 🚀 **High-performance async scraping** with aiohttp
- 📊 **Comprehensive data extraction** from candidate profiles
- 📱 **Phone numbers prioritized** as first CSV column
- 🔄 **Progress saving** - resume from interruption
- 🛡️ **Error handling** and rate limiting
- 🌐 **Full UTF-8 support** for Azerbaijani text

## Installation

```bash
pip install -r requirements.txt
```

## Available Scrapers

### 1. Basic Scraper (scraper.py)
Limited to 2 pages for testing:
```bash
python scraper.py
```

### 2. Async Scraper (async_scraper.py) 
Fast async scraping with limited pages:
```bash
python async_scraper.py
```

### 3. **Full All-Pages Scraper (scraper_all_pages.py)** ⭐
**RECOMMENDED** - Scrapes ALL available pages:
```bash
python scraper_all_pages.py
```

## Data Fields Extracted

- **phone_number** (primary phone - first column)
- name, position
- mobile_phone, home_phone, email
- gender, salary_expectation
- skills, languages
- education, work_history
- about, desired_positions
- url (profile URL)

## Features of All-Pages Scraper

- ✅ **Automatic page detection** - finds all available pages
- ✅ **Progress auto-save** every 5 pages
- ✅ **Graceful interruption** - Ctrl+C saves progress
- ✅ **Concurrent processing** - 8 parallel requests
- ✅ **Smart rate limiting** - respectful to the website
- ✅ **Error recovery** - continues despite individual failures

## Output

All scrapers save to CSV files:
- `scraper.py` → `busy_az_candidates.csv`
- `async_scraper.py` → `busy_az_candidates_async.csv` 
- `scraper_all_pages.py` → `busy_az_all_candidates.csv`

## Performance

- **Basic**: ~2-3 candidates/minute
- **Async**: ~10-15 candidates/minute  
- **All-Pages**: ~15-20 candidates/minute with full error handling

## Notes

- Phone numbers extracted from mobile/home phone fields
- Handles missing profiles (404 errors) gracefully
- UTF-8 encoding preserves Azerbaijani characters
- Respects website with appropriate delays
- Can be interrupted and resumed safely