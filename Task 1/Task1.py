# Standard library imports
import time        # For delays and timing
import pandas as pd  # Data manipulation
import logging     # For logging progress and errors
# Selenium imports for browser automation
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup  # For HTML parsing


# Configuration for scraping
CONFIG = {
    'MAIN_URL': 'https://magicpin.in/india/Ahmedabad/All/Gym/',  # Target URL for gyms in Ahmedabad
    'CITY': 'Ahmedabad',
    'STATE': 'Gujarat',
    'MIN_GYMS': 80,  # Minimum gyms to scrape
    'OUTPUT_FILE': 'Task 1/ahmedabad_gyms.csv',  # Output CSV file
    'SCROLL_COUNT': 12,  # Number of scrolls to load more gyms
    'SCROLL_DELAY': 1.5,  # Delay between scrolls (seconds)
}


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


# Set up Selenium Chrome WebDriver with custom options
def setup_driver():
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1400,900')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    return webdriver.Chrome(options=options)


# ============================================
# MAIN SCRAPER FUNCTION
# ============================================


def scrape_magicpin_gyms() -> pd.DataFrame:
    """
    Main function to scrape gym listings from MagicPin for Ahmedabad.
    Steps:
    1. Load the listing page in Selenium Chrome browser
    2. Scroll multiple times to load more gyms
    3. Parse the page source with BeautifulSoup
    4. Extract gym details from each article
    5. Clean, deduplicate, and save results to CSV
    """
    driver = setup_driver()
    all_gyms = []  # List to store gym records

    try:
        # STEP 1: Load listing page
        logger.info(f'\n>>> Loading: {CONFIG["MAIN_URL"]}')
        driver.get(CONFIG['MAIN_URL'])

        # Wait for page to render
        logger.info('>>> Waiting for page to render...')
        time.sleep(3)

        # Wait for articles to appear
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, 'article'))
            )
            logger.info('✓ Articles found!')
        except:
            logger.warning('⚠ Timeout waiting for articles')

        # STEP 2: Scroll to load more gyms
        logger.info(f'\n>>> Scrolling {CONFIG["SCROLL_COUNT"]} times to load gyms...')
        for scroll_idx in range(CONFIG['SCROLL_COUNT']):
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(CONFIG['SCROLL_DELAY'])
            logger.info(f'  Scroll {scroll_idx + 1}/{CONFIG["SCROLL_COUNT"]}')

        # STEP 3: Parse gym articles
        logger.info(f'\n>>> Parsing gym articles...')
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all gym articles
        articles = soup.find_all('article', class_='store')
        logger.info(f'✓ Found {len(articles)} gym articles')

        if len(articles) == 0:
            logger.error('✗ No gym articles found!')
            return pd.DataFrame()

        # STEP 4: Extract gym info from each article
        logger.info(f'\n>>> Extracting gym details...\n')

        for idx, article in enumerate(articles, 1):
            try:
                # Get gym name from h2 or h3 tag
                name_elem = article.find(['h2', 'h3'])
                gym_name = name_elem.get_text(strip=True) if name_elem else 'N/A'

                # Get location from merchant-location div
                location_elem = article.find('div', class_='merchant-location')
                area = 'N/A'

                if location_elem:
                    # The first link contains area name
                    location_link = location_elem.find('a')
                    if location_link:
                        area = location_link.get_text(strip=True).split(',')[0].strip()

                # Address is area + city + state
                address = f'{area}, {CONFIG["CITY"]}, {CONFIG["STATE"]}' if area != 'N/A' else 'N/A'

                # Validate gym name
                if not gym_name or gym_name == 'N/A' or len(gym_name) < 2:
                    logger.info(f'[{idx:3d}] ✗ Invalid gym name')
                    continue

                # Create gym record
                gym_record = {
                    'Gym Name': gym_name,
                    'Address': address,
                    'Area': area,
                    'City': CONFIG['CITY'],
                    'State': CONFIG['STATE'],
                    'Phone Number': 'N/A',  # Not available
                    'Timings': 'N/A',       # Not available
                }

                all_gyms.append(gym_record)
                logger.info(f'[{idx:3d}] ✓ {gym_name:40} | {area}')

            except Exception as e:
                logger.info(f'[{idx:3d}] ✗ Error: {str(e)[:40]}')
                continue

        # STEP 5: Create DataFrame from collected gyms
        if not all_gyms:
            logger.error('\n✗ No valid gym data collected')
            return pd.DataFrame()

        logger.info(f'\n>>> Processing data...')
        df = pd.DataFrame(all_gyms)

        # Remove duplicate gyms by name
        df = df.drop_duplicates(subset=['Gym Name'], keep='first')
        df = df.reset_index(drop=True)

        logger.info(f'✓ Total unique gyms: {len(df)}')
        logger.info(f'✓ Unique areas: {df["Area"].nunique()}')

        # Check if minimum target met
        if len(df) >= CONFIG['MIN_GYMS']:
            logger.info(f'✓ TARGET ACHIEVED: {len(df)}/{CONFIG["MIN_GYMS"]} gyms')
        else:
            logger.warning(f'⚠ Only {len(df)} gyms (need {CONFIG["MIN_GYMS"]})')

        # Save DataFrame to CSV
        df.to_csv(CONFIG['OUTPUT_FILE'], index=False)
        logger.info(f'✓ Saved to {CONFIG["OUTPUT_FILE"]}')

        return df

    finally:
        # Always close the browser
        try:
            driver.quit()
            logger.info('>>> Browser closed')
        except:
            pass


# ============================================
# MAIN EXECUTION BLOCK
# ============================================


if __name__ == '__main__':
    # Entry point for script execution
    logger.info('\n' + '='*70)
    logger.info('MAGICPIN GYM SCRAPER - CORRECTED')
    logger.info('='*70)

    start = time.time()
    df = scrape_magicpin_gyms()
    elapsed = time.time() - start

    logger.info('\n' + '='*70)
    logger.info(f'COMPLETED IN {elapsed:.1f} SECONDS')
    logger.info('='*70)

    # Display results summary
    if not df.empty:
        print('\n' + '='*80)
        print('RESULTS')
        print('='*80)
        print(f'\nTotal gyms: {len(df)}')
        print(f'Unique areas: {df["Area"].nunique()}')

        print('\n' + '-'*80)
        print('FIRST 15 GYMS:')
        print('-'*80)
        print(df.head(15).to_string(index=False))

        print('\n' + '-'*80)
        print('TOP AREAS:')
        print('-'*80)
        print(df['Area'].value_counts().head(15).to_string())

        print('\n' + '='*80)
        print(f'✓ File: {CONFIG["OUTPUT_FILE"]}')
        print('='*80 + '\n')
    else:
        print('\n✗ No data scraped!')
