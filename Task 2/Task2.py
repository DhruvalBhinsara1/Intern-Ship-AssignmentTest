
# Standard library imports
import time        # For delays between requests
import random      # For randomizing delays
import pandas as pd  # Data manipulation
from bs4 import BeautifulSoup  # HTML parsing
import requests    # HTTP requests
import os          # For directory creation


# List of Amazon search URLs for different product categories
AMAZON_SEARCH_URLS = [
    'https://www.amazon.in/s?k=laptop',
    'https://www.amazon.in/s?k=mobile+phone',
    'https://www.amazon.in/s?k=headphones',
    'https://www.amazon.in/s?k=keyboard',
    'https://www.amazon.in/s?k=mouse',
    'https://www.amazon.in/s?k=monitor',
    'https://www.amazon.in/s?k=webcam',
    'https://www.amazon.in/s?k=book',
    'https://www.amazon.in/s?k=watch',
    'https://www.amazon.in/s?k=shoes',
]


# HTTP headers to mimic a real browser and avoid anti-bot detection
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.amazon.in/',
}


# Extracts a high-level category from the search query string
def extract_category_from_query(query):
    """Extract category name from search query."""
    category_map = {
        'laptop': 'Electronics',
        'mobile': 'Electronics',
        'headphones': 'Electronics',
        'keyboard': 'Electronics',
        'mouse': 'Electronics',
        'monitor': 'Electronics',
        'webcam': 'Electronics',
        'book': 'Books',
        'watch': 'Accessories',
        'shoes': 'Clothing',
    }
    for key, cat in category_map.items():
        if key in query.lower():
            return cat
    return 'General'


# Scrapes product data from a single Amazon search result page
def scrape_amazon_search(url):
    """Scrape products from Amazon search results."""
    products = []

    try:
        print(f"Fetching: {url}")
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all product containers on the page
        items = soup.select('div[data-component-type="s-search-result"]')
        if not items:
            items = soup.select('div.s-result-item[data-asin]')

        print(f"  Found {len(items)} product containers")

        # Extract query for category/subcategory
        query = url.split('k=')[-1] if 'k=' in url else 'General'
        category = extract_category_from_query(query)

        for item in items:
            try:
                asin = item.get('data-asin', '')
                if not asin:
                    continue

                # Extract product title
                h2 = item.find('h2')
                if not h2:
                    h2 = item.find('span', {'class': 'a-size-medium'})
                title = h2.get_text(strip=True) if h2 else 'N/A'

                # Skip sponsored or missing titles
                if not title or 'Sponsored' in title or title == 'N/A':
                    continue

                # Extract price
                price = 'N/A'
                price_span = item.find('span', {'class': 'a-price-whole'})
                if price_span:
                    price = price_span.get_text(strip=True)

                # Extract rating
                rating = 'N/A'
                rating_span = item.find('span', {'class': 'a-icon-alt'})
                if rating_span:
                    rating_text = rating_span.get_text(strip=True)
                    if 'stars' in rating_text:
                        rating = rating_text  # e.g., "4.1 out of 5 stars"
                else:
                    rating_span = item.find('span', {'class': 'a-icon-star-small'})
                    if rating_span:
                        rating_text = rating_span.get_text(strip=True)
                        if rating_text:
                            rating = rating_text

                # Extract number of reviews
                reviews = 'N/A'
                reviews_span = item.find('span', {'class': 'a-size-base'})
                if reviews_span:
                    reviews_text = reviews_span.get_text(strip=True)
                    if reviews_text and any(char.isdigit() for char in reviews_text):
                        reviews = reviews_text

                # Extract product URL
                link = item.find('a', {'class': 'a-link-normal'})
                product_url = 'N/A'
                if link and link.get('href'):
                    href = link['href']
                    if href.startswith('/'):
                        product_url = 'https://www.amazon.in' + href.split('?')[0]
                    else:
                        product_url = href.split('?')[0]

                # Add product to list
                if title and title != 'N/A':
                    products.append({
                        'Category': category,
                        'Subcategory': query.replace('+', ' ').upper(),
                        'Product Title': title,
                        'Price': price,
                        'Rating': rating,
                        'Reviews': reviews,
                        'Product URL': product_url
                    })

            except Exception as e:
                # Skip product if any error occurs
                continue

        print(f"  ✓ Extracted {len(products)} products\n")
        return products

    except Exception as e:
        print(f"  ✗ Error: {str(e)[:60]}\n")
        return []


if __name__ == "__main__":
    # Create output directory if it doesn't exist
    os.makedirs('Task 2/data', exist_ok=True)

    print("\n" + "="*70)
    print("AMAZON PRODUCT SCRAPER - REQUESTS METHOD")
    print("="*70 + "\n")

    all_products = []

    # Scrape each Amazon search URL
    for url in AMAZON_SEARCH_URLS:
        products = scrape_amazon_search(url)
        all_products.extend(products)
        time.sleep(random.uniform(1, 2))  # Polite delay between requests

    # Save results to CSV if any products were scraped
    if all_products:
        df = pd.DataFrame(all_products)
        df.drop_duplicates(subset=['Product URL'], inplace=True)

        # Clean and normalize data columns
        df['Price'] = df['Price'].str.replace(',', '').str.replace('₹', '').str.extract(r'(\d+\.?\d*)')[0]
        df['Rating'] = df['Rating'].str.extract(r'(\d+\.?\d*)')[0]
        df['Reviews'] = df['Reviews'].str.replace(',', '').str.extract(r'(\d+)')[0]

        df.to_csv('Task 2/data/amazon_products.csv', index=False)

        print("="*70)
        print(f"✓ SAVED: {len(df)} unique products to Task 2/data/amazon_products.csv")
        print(f"✓ Categories: {df['Category'].nunique()}")
        print(f"✓ Subcategories: {df['Subcategory'].nunique()}")
        print("="*70 + "\n")

        print(df.head(20).to_string(index=False))
    else:
        print("✗ No products scraped!")
