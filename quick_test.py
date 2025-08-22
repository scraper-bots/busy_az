import requests
from bs4 import BeautifulSoup
import csv
import time
import re
from urllib.parse import urljoin
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def quick_test():
    """Quick test to scrape just a few candidates"""
    base_url = "https://busy.az"
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    # Get first page
    url = f"{base_url}/jobseekers?page=1"
    print(f"Fetching: {url}")
    
    try:
        response = session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find candidate links
        links = soup.find_all('a', href=re.compile(r'/jobseeker/\d+'))
        candidate_urls = []
        
        for link in links[:5]:  # Only test first 5 candidates
            href = link.get('href')
            if href:
                full_url = urljoin(base_url, href)
                if full_url not in candidate_urls:
                    candidate_urls.append(full_url)
        
        print(f"Found {len(candidate_urls)} candidate URLs")
        
        candidates = []
        
        for url in candidate_urls:
            print(f"Scraping: {url}")
            
            try:
                response = session.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                data = {'url': url, 'phone_number': '', 'name': '', 'position': ''}
                
                # Extract name
                name_elem = soup.find('h3')
                if name_elem:
                    data['name'] = name_elem.get_text(strip=True)
                
                # Extract position
                position_elem = soup.find('p', class_='header-under-name')
                if position_elem:
                    data['position'] = position_elem.get_text(strip=True)
                
                # Extract phone from table
                tables = soup.find_all('table')
                for table in tables:
                    rows = table.find_all('tr')
                    for row in rows:
                        th = row.find('th')
                        td = row.find('td')
                        if th and td:
                            field_name = th.get_text(strip=True).lower()
                            field_value = td.get_text(strip=True)
                            
                            if 'telefon' in field_name or 'phone' in field_name:
                                data['phone_number'] = field_value
                                break
                
                candidates.append(data)
                print(f"  - Name: {data['name']}")
                print(f"  - Position: {data['position']}")
                print(f"  - Phone: {data['phone_number']}")
                print()
                
                time.sleep(0.5)  # Shorter delay for testing
                
            except Exception as e:
                print(f"Error scraping {url}: {e}")
                continue
        
        # Save to CSV
        if candidates:
            with open('test_candidates.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['phone_number', 'name', 'position', 'url']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(candidates)
            
            print(f"Saved {len(candidates)} candidates to test_candidates.csv")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    quick_test()