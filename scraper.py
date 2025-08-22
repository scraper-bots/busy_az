import requests
from bs4 import BeautifulSoup
import csv
import time
import re
from urllib.parse import urljoin, urlparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BusyAzScraper:
    def __init__(self):
        self.base_url = "https://busy.az"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def get_candidate_urls(self, page=1):
        """Extract candidate URLs from the jobseekers list page"""
        url = f"{self.base_url}/jobseekers?page={page}"
        logger.info(f"Fetching candidates from page {page}")
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            candidate_urls = []
            
            # Look for candidate profile links
            links = soup.find_all('a', href=re.compile(r'/jobseeker/\d+'))
            
            for link in links:
                href = link.get('href')
                if href:
                    full_url = urljoin(self.base_url, href)
                    if full_url not in candidate_urls:
                        candidate_urls.append(full_url)
            
            logger.info(f"Found {len(candidate_urls)} candidate URLs on page {page}")
            return candidate_urls
            
        except requests.RequestException as e:
            logger.error(f"Error fetching page {page}: {e}")
            return []
    
    def extract_candidate_data(self, candidate_url):
        """Extract all data from a candidate's profile page"""
        logger.info(f"Scraping candidate: {candidate_url}")
        
        try:
            response = self.session.get(candidate_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            data = {
                'phone_number': '',
                'home_phone': '',
                'mobile_phone': '',
                'name': '',
                'position': '',
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
            
            # Extract personal information from sidebar
            sidebar_tables = soup.find_all('table')
            for table in sidebar_tables:
                rows = table.find_all('tr')
                for row in rows:
                    th = row.find('th')
                    td = row.find('td')
                    if th and td:
                        field_name = th.get_text(strip=True).lower()
                        field_value = td.get_text(strip=True)
                        
                        if 'mobil telefon' in field_name or 'mobile phone' in field_name:
                            data['mobile_phone'] = field_value
                            if not data['phone_number']:  # Use mobile as primary phone
                                data['phone_number'] = field_value
                        elif 'ev telefonu' in field_name or 'home phone' in field_name:
                            data['home_phone'] = field_value
                            if not data['phone_number']:  # Use home phone if no mobile
                                data['phone_number'] = field_value
                        elif 'e-mail' in field_name:
                            data['email'] = field_value
                        elif 'cins' in field_name or 'gender' in field_name:
                            data['gender'] = field_value
                        elif 'maaş' in field_name or 'salary' in field_name:
                            data['salary_expectation'] = field_value
            
            # Extract skills
            skills_div = soup.find('div', class_='task-tags')
            if skills_div:
                skills = []
                for span in skills_div.find_all('span'):
                    skills.append(span.get_text(strip=True))
                data['skills'] = ', '.join(skills)
            
            # Extract languages
            language_sections = soup.find_all('div', class_='boxed-list')
            for section in language_sections:
                headline = section.find('h3')
                if headline and ('dil' in headline.get_text().lower() or 'language' in headline.get_text().lower()):
                    languages = []
                    for li in section.find_all('li'):
                        lang_text = li.get_text(strip=True)
                        if lang_text:
                            languages.append(lang_text)
                    data['languages'] = ' | '.join(languages)
                    break
            
            # Extract education
            education_sections = soup.find_all('div', class_='boxed-list')
            for section in education_sections:
                headline = section.find('h3')
                if headline and ('təhsil' in headline.get_text().lower() or 'education' in headline.get_text().lower()):
                    education_entries = []
                    for li in section.find_all('li'):
                        education_entries.append(li.get_text(strip=True))
                    data['education'] = ' | '.join(education_entries)
                    break
            
            # Extract work history
            work_sections = soup.find_all('div', class_='boxed-list')
            for section in work_sections:
                headline = section.find('h3')
                if headline and ('tarixçə' in headline.get_text().lower() or 'history' in headline.get_text().lower()):
                    work_entries = []
                    for li in section.find_all('li'):
                        work_entries.append(li.get_text(strip=True))
                    data['work_history'] = ' | '.join(work_entries)
                    break
            
            # Extract about section
            about_section = soup.find('div', class_='single-page-section')
            if about_section:
                about_p = about_section.find('p')
                if about_p:
                    data['about'] = about_p.get_text(strip=True)
            
            # Extract desired positions
            sidebar_widgets = soup.find_all('div', class_='sidebar-widget')
            for widget in sidebar_widgets:
                h3 = widget.find('h3')
                if h3 and ('ixtisas' in h3.get_text().lower() or 'profession' in h3.get_text().lower()):
                    positions = []
                    for span in widget.find_all('span'):
                        positions.append(span.get_text(strip=True))
                    data['desired_positions'] = ', '.join(positions)
                    break
            
            return data
            
        except requests.RequestException as e:
            logger.error(f"Error scraping {candidate_url}: {e}")
            return None
    
    def scrape_all_candidates(self, max_pages=None):
        """Scrape all candidates from all pages"""
        all_candidates = []
        page = 1
        
        while True:
            if max_pages and page > max_pages:
                break
                
            candidate_urls = self.get_candidate_urls(page)
            
            if not candidate_urls:
                logger.info("No more candidates found, stopping")
                break
            
            for url in candidate_urls:
                candidate_data = self.extract_candidate_data(url)
                if candidate_data:
                    all_candidates.append(candidate_data)
                
                # Rate limiting
                time.sleep(1)
            
            page += 1
            time.sleep(2)  # Longer delay between pages
        
        return all_candidates
    
    def save_to_csv(self, candidates, filename='busy_az_candidates.csv'):
        """Save candidate data to CSV file with phone number as first column"""
        if not candidates:
            logger.warning("No candidates to save")
            return
        
        fieldnames = [
            'phone_number',  # Phone number first as requested
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
            
            for candidate in candidates:
                # Ensure all fields exist
                row = {}
                for field in fieldnames:
                    row[field] = candidate.get(field, '')
                writer.writerow(row)
        
        logger.info(f"Saved {len(candidates)} candidates to {filename}")

def main():
    scraper = BusyAzScraper()
    
    # Scrape first 2 pages as a test (remove max_pages to scrape all)
    candidates = scraper.scrape_all_candidates(max_pages=2)
    
    # Save to CSV
    scraper.save_to_csv(candidates)
    
    print(f"Scraping completed! Found {len(candidates)} candidates.")
    print("Data saved to busy_az_candidates.csv")

if __name__ == "__main__":
    main()