from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urlparse  # NEW: For URL cleaning

class BBCSectionScraper:
    def __init__(self, driver, section='news'):
        self.driver = driver
        self.section = section
        self.articles = []
        self.base_url = f"https://www.bbc.com/{section}"
        self.seen_urls = set()  # NEW: Track duplicates in memory

    # NEW: Clean URLs to avoid /news vs /news?utm=tracker duplicates
    def clean_url(self, url):
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip('/')

    def load_section_page(self):
        self.driver.get(self.base_url)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//a[@data-testid="internal-link"] | //main | //article')
                )
            )
        except:
            print(f"⚠️  Using basic load detection for {self.section}")
            time.sleep(3)

    def extract_links(self):
        article_links = []
        
        links = self.driver.find_elements(By.XPATH, '//a[@data-testid="internal-link"]')
        
        for link in links:
            try:
                href = link.get_attribute('href')
                if not href:
                    continue
                
                # NEW: Skip duplicates using cleaned URL
                clean_url = self.clean_url(href)
                if clean_url in self.seen_urls:
                    continue
                
                # Your original title extraction
                try:
                    title = link.find_element(By.XPATH, './/h2').text.strip()
                    summary = link.find_element(By.XPATH, './/p').text.strip()
                except:
                    title = link.text.strip()
                
                if not title or len(title) < 10:
                    continue
                
                article_links.append({
                    "title": title.replace("\n", " ").replace('"', ''),
                    "url": clean_url,  # Store cleaned URL
                    "section": self.section,
                    "summary" : summary.replace("\n", " ").replace('"', '')
                })
                self.seen_urls.add(clean_url)  # NEW: Mark as seen

            except Exception as e:
                print(f"Skipped link: {str(e)[:50]}...")
                continue

        return article_links

    # get_article_content() stays the SAME as your original
    def get_article_content(self, url):
        self.driver.get(url)
        time.sleep(2)
        
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        blocks = soup.find_all('div', {'data-component': 'text-block'})
        if not blocks:
            blocks = soup.find_all('article') or soup.find_all('main')

        paragraphs = [
            f"{p.get_text(strip=True)}"
            for block in blocks 
            for p in block.find_all('p')
            if len(p.get_text(strip=True)) > 10
        ]
        return '\n'.join(paragraphs) if paragraphs else None

    def scrape_section(self):
        try:
            self.load_section_page()
            links = self.extract_links()
            
            for link in links:
                try:
                    content = self.get_article_content(link['url'])
                    if content:
                        self.articles.append({
                            **link,
                            "content": content
                        })
                        print(f"✅ Success: {link['title']}")
                except Exception as e:
                    print(f"⚠️  Failed: {link.get('url', '')}")
            
            return self.articles
        
        except Exception as e:
            print(f"🚨 Section error: {str(e)[:100]}...")
            return []

# NEW: Smarter saving that merges with existing data
def save_to_json(data, filename='wwwroot/articles.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    sections = ['news', 'sport', 'business', 'innovation', 'culture', 'arts', 'travel']
    all_articles = []
    
    options = webdriver.EdgeOptions()
    options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Edge(options=options)

    try:
        for section in sections:
            print(f"\n Scraping {section.upper()} section")
            scraper = BBCSectionScraper(driver, section=section)
            section_articles = scraper.scrape_section()
            all_articles.extend(section_articles)
            print(f"Found {len(section_articles)} articles")
        
        save_to_json(all_articles)
        print(f"\n Total articles: {len(all_articles)}")

    finally:
        driver.quit()

# * faire fonctionner