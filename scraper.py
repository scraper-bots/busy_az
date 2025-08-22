import asyncio
import aiohttp
from bs4 import BeautifulSoup
import csv
import re
from urllib.parse import urljoin
import logging
from typing import List, Dict, Optional
import time
import signal
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BusyAzFullScraper:
    def __init__(self, max_concurrent=8):
        self.base_url = "https://busy.az"
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.scraped_candidates = []
        self.total_candidates = 0
        self.current_page = 1
        
    async def create_session(self):
        """Create aiohttp session with proper headers and timeouts"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        connector = aiohttp.TCPConnector(
            limit=20, 
            limit_per_host=8,
            ttl_dns_cache=300,
            use_dns_cache=True
        )
        
        return aiohttp.ClientSession(
            headers=headers, 
            connector=connector, 
            timeout=timeout
        )
    
    async def get_total_pages(self, session: aiohttp.ClientSession) -> int:
        """Determine the total number of pages available"""
        url = f"{self.base_url}/jobseekers?page=1"
        
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Look for pagination elements
                    pagination = soup.find('ul', class_='pagination')
                    if pagination:
                        page_links = pagination.find_all('a')
                        max_page = 1
                        
                        for link in page_links:
                            href = link.get('href', '')
                            page_match = re.search(r'page=(\d+)', href)
                            if page_match:
                                page_num = int(page_match.group(1))
                                max_page = max(max_page, page_num)
                        
                        logger.info(f"Found {max_page} total pages")
                        return max_page
                    
                    # If no pagination found, try to detect by testing pages
                    logger.info("No pagination found, will detect pages dynamically")
                    return 999  # Will be detected during scraping
                    
        except Exception as e:
            logger.error(f"Error detecting total pages: {e}")
            return 999  # Fallback to dynamic detection
    
    async def get_candidate_urls_from_page(self, session: aiohttp.ClientSession, page: int) -> List[str]:
        """Extract candidate URLs from a single page"""
        url = f"{self.base_url}/jobseekers?page={page}"
        
        async with self.semaphore:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        candidate_urls = []
                        links = soup.find_all('a', href=re.compile(r'/jobseeker/\d+'))
                        
                        for link in links:
                            href = link.get('href')
                            if href:
                                full_url = urljoin(self.base_url, href)
                                if full_url not in candidate_urls:
                                    candidate_urls.append(full_url)
                        
                        if candidate_urls:
                            logger.info(f"Page {page}: Found {len(candidate_urls)} candidates")
                        else:
                            logger.warning(f"Page {page}: No candidates found")
                        
                        return candidate_urls
                    else:
                        logger.warning(f"Page {page}: HTTP {response.status}")
                        return []
                        
            except Exception as e:
                logger.error(f"Error fetching page {page}: {e}")
                return []
    
    async def extract_candidate_data(self, session: aiohttp.ClientSession, candidate_url: str) -> Optional[Dict]:
        """Extract all data from a candidate's profile page"""
        
        async with self.semaphore:
            try:
                async with session.get(candidate_url) as response:
                    if response.status != 200:
                        if response.status != 404:  # 404s are expected for some profiles
                            logger.warning(f"Candidate {candidate_url}: HTTP {response.status}")
                        return None
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    data = {
                        'phone_number': '',
                        'name': '',
                        'position': '',
                        'mobile_phone': '',
                        'home_phone': '',
                        'email': '',
                        'gender': '',
                        'salary_expectation': '',
                        'skills': '',
                        'languages': '',
                        'education': '',
                        'work_history': '',
                        'about': '',
                        'desired_positions': '',
                        'url': candidate_url
                    }
                    
                    # Extract name
                    name_elem = soup.find('h3')
                    if name_elem:
                        data['name'] = name_elem.get_text(strip=True)
                    
                    # Extract position
                    position_elem = soup.find('p', class_='header-under-name')
                    if position_elem:
                        data['position'] = position_elem.get_text(strip=True)
                    
                    # Extract personal information from sidebar tables
                    tables = soup.find_all('table')
                    for table in tables:
                        rows = table.find_all('tr')
                        for row in rows:
                            th = row.find('th')
                            td = row.find('td')
                            if th and td:
                                field_name = th.get_text(strip=True).lower()
                                field_value = td.get_text(strip=True)
                                
                                if 'mobil telefon' in field_name:
                                    data['mobile_phone'] = field_value
                                    if not data['phone_number']:
                                        data['phone_number'] = field_value
                                elif 'ev telefonu' in field_name:
                                    data['home_phone'] = field_value
                                    if not data['phone_number']:
                                        data['phone_number'] = field_value
                                elif 'e-mail' in field_name:
                                    data['email'] = field_value
                                elif 'cins' in field_name:
                                    data['gender'] = field_value
                                elif 'maaş' in field_name:
                                    data['salary_expectation'] = field_value
                    
                    # Extract skills and desired positions from sidebar
                    sidebar_widgets = soup.find_all('div', class_='sidebar-widget')
                    for widget in sidebar_widgets:
                        h3 = widget.find('h3')
                        if h3:
                            h3_text = h3.get_text().lower()
                            task_tags = widget.find('div', class_='task-tags')
                            if task_tags:
                                if 'bilik' in h3_text or 'bacarıq' in h3_text:
                                    skills = [span.get_text(strip=True) for span in task_tags.find_all('span')]
                                    data['skills'] = ', '.join(skills)
                                elif 'ixtisas' in h3_text and 'istədiyi' in h3_text:
                                    positions = [span.get_text(strip=True) for span in task_tags.find_all('span')]
                                    data['desired_positions'] = ', '.join(positions)
                    
                    # Extract languages, education, work history from boxed lists
                    boxed_lists = soup.find_all('div', class_='boxed-list')
                    for boxed_list in boxed_lists:
                        headline = boxed_list.find('h3')
                        if headline:
                            headline_text = headline.get_text().lower()
                            
                            if 'dil' in headline_text:
                                lang_items = boxed_list.find_all('li')
                                languages = [li.get_text(strip=True) for li in lang_items if li.get_text(strip=True)]
                                data['languages'] = ' | '.join(languages)
                            
                            elif 'təhsil' in headline_text:
                                edu_items = boxed_list.find_all('li')
                                education = [li.get_text(strip=True) for li in edu_items if li.get_text(strip=True)]
                                data['education'] = ' | '.join(education)
                            
                            elif 'tarixçə' in headline_text:
                                work_items = boxed_list.find_all('li')
                                work_history = [li.get_text(strip=True) for li in work_items if li.get_text(strip=True)]
                                data['work_history'] = ' | '.join(work_history)
                    
                    # Extract about section
                    about_section = soup.find('div', class_='single-page-section')
                    if about_section:
                        about_p = about_section.find('p')
                        if about_p:
                            data['about'] = about_p.get_text(strip=True)
                    
                    return data
                    
            except asyncio.TimeoutError:
                logger.warning(f"Timeout scraping {candidate_url}")
                return None
            except Exception as e:
                logger.error(f"Error scraping {candidate_url}: {e}")
                return None
    
    async def scrape_candidates_batch(self, session: aiohttp.ClientSession, urls: List[str]) -> List[Dict]:
        """Scrape multiple candidates concurrently"""
        tasks = [self.extract_candidate_data(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        candidates = []
        for result in results:
            if isinstance(result, dict) and result:
                candidates.append(result)
            elif isinstance(result, Exception):
                logger.error(f"Candidate batch error: {result}")
        
        return candidates
    
    def save_progress(self, filename: str = 'busy_az_candidates.csv'):
        """Save current progress to CSV"""
        if not self.scraped_candidates:
            return
            
        fieldnames = [
            'phone_number',
            'name',
            'position',
            'mobile_phone',
            'home_phone',
            'email',
            'gender',
            'salary_expectation',
            'skills',
            'languages',
            'education',
            'work_history',
            'about',
            'desired_positions',
            'url'
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for candidate in self.scraped_candidates:
                row = {}
                for field in fieldnames:
                    row[field] = candidate.get(field, '')
                writer.writerow(row)
        
        logger.info(f"💾 Progress saved: {len(self.scraped_candidates)} candidates to {filename}")
    
    async def scrape_all_pages(self) -> List[Dict]:
        """Scrape ALL pages from busy.az"""
        start_time = time.time()
        
        async with await self.create_session() as session:
            logger.info("🚀 Starting full scraping of ALL pages...")
            
            # Get total pages
            total_pages = await self.get_total_pages(session)
            
            page = 1
            consecutive_empty_pages = 0
            max_empty_pages = 3  # Stop after 3 consecutive empty pages
            
            while page <= total_pages and consecutive_empty_pages < max_empty_pages:
                try:
                    # Get candidate URLs from current page
                    candidate_urls = await self.get_candidate_urls_from_page(session, page)
                    
                    if not candidate_urls:
                        consecutive_empty_pages += 1
                        logger.warning(f"📄 Page {page}: No candidates found ({consecutive_empty_pages}/{max_empty_pages} empty)")
                        page += 1
                        continue
                    else:
                        consecutive_empty_pages = 0
                    
                    # Scrape candidates in batches
                    batch_size = 15
                    page_candidates = []
                    
                    for i in range(0, len(candidate_urls), batch_size):
                        batch_urls = candidate_urls[i:i + batch_size]
                        batch_candidates = await self.scrape_candidates_batch(session, batch_urls)
                        page_candidates.extend(batch_candidates)
                        
                        # Short delay between batches
                        await asyncio.sleep(0.8)
                    
                    self.scraped_candidates.extend(page_candidates)
                    
                    logger.info(f"✅ Page {page}: Scraped {len(page_candidates)} candidates (Total: {len(self.scraped_candidates)})")
                    
                    # Save progress every 5 pages
                    if page % 5 == 0:
                        self.save_progress()
                    
                    page += 1
                    
                    # Longer delay between pages
                    await asyncio.sleep(1.5)
                    
                except KeyboardInterrupt:
                    logger.info("🛑 Interrupted by user, saving progress...")
                    self.save_progress()
                    break
                except Exception as e:
                    logger.error(f"❌ Error on page {page}: {e}")
                    page += 1
                    await asyncio.sleep(2.0)
        
        # Final save
        self.save_progress()
        
        elapsed = time.time() - start_time
        logger.info(f"🎉 Full scraping completed in {elapsed:.2f} seconds")
        logger.info(f"📊 Total candidates scraped: {len(self.scraped_candidates)}")
        
        return self.scraped_candidates

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🛑 Received interrupt signal. Saving progress and exiting...")
    sys.exit(0)

async def main():
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    scraper = BusyAzFullScraper(max_concurrent=8)
    
    try:
        candidates = await scraper.scrape_all_pages()
        
        print(f"\n🎉 Scraping completed successfully!")
        print(f"📊 Total candidates found: {len(candidates)}")
        print(f"📁 Data saved to: busy_az_candidates.csv")
        
        # Show sample of data
        if candidates:
            print(f"\n📋 Sample candidate:")
            sample = candidates[0]
            print(f"   Name: {sample.get('name', 'N/A')}")
            print(f"   Phone: {sample.get('phone_number', 'N/A')}")
            print(f"   Position: {sample.get('position', 'N/A')}")
        
    except KeyboardInterrupt:
        print("\n🛑 Scraping interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during scraping: {e}")

if __name__ == "__main__":
    asyncio.run(main())