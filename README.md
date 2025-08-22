# Busy.az Job Seeker Scraper

A Python web scraper to extract candidate information from busy.az job seeker profiles.

## Features

- Scrapes candidate list from https://busy.az/jobseekers
- Extracts detailed information from individual candidate profiles
- Exports data to CSV with phone number as the first column
- Includes rate limiting and error handling
- Extracts: phone numbers, personal details, skills, education, work history, and more

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the scraper:
```bash
python scraper.py
```

2. The scraper will:
   - Fetch candidate URLs from the jobseekers page
   - Visit each candidate's profile page
   - Extract all available information
   - Save data to `busy_az_candidates.csv`

## Data Fields Extracted

- **phone_number** (primary phone - first column)
- name
- position
- mobile_phone
- home_phone
- email
- gender
- salary_expectation
- skills
- languages
- education
- work_history
- about
- desired_positions
- url (profile URL)

## Configuration

- Modify `max_pages` in `main()` to limit scraping to specific number of pages
- Remove `max_pages` parameter to scrape all available pages
- Adjust `time.sleep()` values to change rate limiting

## Notes

- The scraper includes rate limiting (1-2 second delays) to be respectful to the website
- Error handling is included for network issues and parsing errors
- Uses proper User-Agent headers to avoid blocking
- All text is preserved in UTF-8 encoding for Azerbaijani characters