# Busy.az Job Seeker Scraper

High-performance async web scraper to extract ALL candidate information from busy.az job seeker profiles.

## Features

- 🚀 **Fastest async scraping** with aiohttp (15-20 candidates/minute)
- 📊 **Comprehensive data extraction** from ALL pages
- 📱 **Phone numbers prioritized** as first CSV column
- 🔄 **Progress auto-save** every 5 pages
- 🛡️ **Error handling** and smart rate limiting
- 🌐 **Full UTF-8 support** for Azerbaijani text
- 🛑 **Graceful interruption** - Ctrl+C saves progress

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the scraper to get ALL candidates:
```bash
python scraper.py
```

## Key Features

- ✅ **Automatic page detection** - finds all available pages
- ✅ **Concurrent processing** - 8 parallel requests  
- ✅ **Smart error recovery** - continues despite failures
- ✅ **Respectful rate limiting** - won't overwhelm the website
- ✅ **Real-time progress** - see live scraping status
- ✅ **Resume capability** - auto-saves progress

## Data Fields Extracted

- **phone_number** (primary phone - first column)
- name, position
- mobile_phone, home_phone, email
- gender, salary_expectation
- skills, languages
- education, work_history
- about, desired_positions
- url (profile URL)

## Output

Creates `busy_az_candidates.csv` with all candidate data.

## Performance

- **Speed**: ~15-20 candidates/minute
- **Efficiency**: Processes multiple candidates simultaneously
- **Reliability**: Handles network issues and missing profiles gracefully

## Technical Details

- Uses aiohttp for async HTTP requests
- BeautifulSoup for HTML parsing
- Automatic pagination detection
- Concurrent processing with semaphore limiting
- UTF-8 CSV output with proper encoding