# Complete Plan for Data Science Internship Assignment

## Assignment Overview

**Timeline:** 2-3 days  
**Submission:** [career@honeybeedigital.com](mailto:career@honeybeedigital.com)  
**Minimum Requirement:** 80-100 entries per scraping task

---

## Task Breakdown & Implementation Plan

### **[x] Task 1: Scrape Gyms from MagicPin (Ahmedabad)**

**Objective:** Extract gym listings from MagicPin website and save as CSV with specific data format.

### **[ ] Task 2: Scrape Amazon Categories & Products**

**Objective:** Extract categories, subcategories, and product details (titles, prices, ratings, URLs)

#### Phase 1: Anti-Bot Strategy Setup (2-3 hours)

Amazon uses AWS WAF for bot detection. Implement bypass techniques:

1.  **Rotating Proxies**
    
    -   Use proxy rotation libraries: `scrapy-rotating-proxies` or manual implementation
    -   Configure residential proxies if budget allows
2.  **User-Agent Switching**
    
    -   Create list of 20+ user agents
    -   Rotate randomly between requests
    -   Use `fake-useragent` library
3.  **Stealth Browser Configuration**
    
    -   Use `undetected-chromedriver` or SeleniumBase
    -   Enable stealth mode to avoid detection
    -   Implement exponential backoff for rate limiting

#### Phase 2: Scraper Architecture (4-5 hours)

**Tool Choice:** Scrapy (for large-scale scraping) or Selenium with BeautifulSoup

**Implementation Strategy:**

1.  **Category Navigation:**
    
    -   Start from main Electronics category (as example)
    -   Recursively extract all subcategories
    -   Build category hierarchy tree
2.  **Product Extraction:**
    
    -   For each subcategory, scrape product listings
    -   Extract: product title, price, rating, product URL, category, subcategory
    -   Implement pagination handling
    -   Target 100+ products across multiple categories
3.  **Request Management:**
    
    -   Random delays (3-8 seconds) between requests
    -   Session management with cookies
    -   Rotate headers and proxies every 5-10 requests

#### Phase 3: Data Processing & Storage (2 hours)

-   Combine all scraped data into single DataFrame
-   Clean pricing data (remove currency symbols, convert to float)
-   Normalize product titles (lowercase, remove extra whitespace)
-   Remove duplicates based on product URL
-   Export to CSV with columns: Category, Subcategory, Product Title, Price, Rating, Product URL

**Estimated Time:** 8-10 hours

---

### **Task 3: OpenStreetMap Overpass API for Tourist Attractions**

**Objective:** Use Overpass API to retrieve tourist attractions for a city (monuments, parks, museums)

#### Phase 1: API Setup & Query Design (1-2 hours)

**Tool Choice:** `overpy` library (Python wrapper for Overpass API)

**Installation:**

```bash
pip install overpy
```

**City Selection:** Choose a major tourist city (e.g., Delhi, Mumbai, Jaipur)

#### Phase 2: Overpass Query Development (2-3 hours)

1.  **Design Query Structure**
    
    ```python
    import overpyapi = overpy.Overpass()query = """[out:json][timeout:500];area[name="Delhi"][admin_level=4];(  node["tourism"="museum"](area);  node["tourism"="monument"](area);  node["leisure"="park"](area);  way["tourism"="museum"](area);  way["tourism"="monument"](area);  way["leisure"="park"](area););out center;"""
    ```
    
2.  **Execute Query & Parse Results**
    
    -   Fetch nodes, ways, and relations
    -   Extract: name, type (museum/monument/park), latitude, longitude
    -   Handle missing tags gracefully

#### Phase 3: Data Extraction & CSV Creation (1 hour)

-   Parse response data into structured format
-   Create DataFrame with columns: Name, Type, Latitude, Longitude, City
-   Ensure 80-100+ entries (adjust query area if needed)
-   Export to CSV

**Estimated Time:** 4-6 hours

---

### **Task 4: Research Data Mapping (Category & Sub-Category)**

**Objective:** Analyze keywords and URLs from Google Sheets, then map to appropriate Categories and Sub-Categories

#### Phase 1: Sheet Selection & Access Setup (1 hour)

1.  Select 2 Google Sheets from provided research data link
    
2.  Set up Google Sheets API access
    
    -   Enable Google Sheets API in Google Cloud Console
    -   Create service account credentials
    -   Install: `pip install gspread oauth2client pandas`
3.  **Authentication Setup**
    
    ```python
    import gspreadfrom oauth2client.service_account import ServiceAccountCredentialsscope = ['https://spreadsheets.google.com/feeds',         'https://www.googleapis.com/auth/drive']creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)client = gspread.authorize(creds)
    ```
    

#### Phase 2: Data Analysis & Mapping Logic (3-4 hours)

**Mapping Guidelines from Assignment:**

1.  **Rule A: Locality Names/Areas**
    
    -   If URL contains locality/area names → Category: Real Estate, Sub-Category: Locality Name
2.  **Rule B: Services/Business Types**
    
    -   If URL contains services → Category: Services, Sub-Category: Specific Service
    -   Example: "homeopathy-pharmacies" → Healthcare → Homeopathy
3.  **Rule C: Keyword Intent**
    
    -   Use keyword to determine category
    -   Example: "play school near me" → Education → Play Schools

**Implementation Strategy:**

1.  Read Google Sheet into pandas DataFrame
    
2.  Create two new columns: 'Category', 'Sub-Category'
    
3.  **Automated Mapping Function:**
    
    ```python
    def map_category_subcategory(keyword, url):    # Parse URL for patterns    # Check for locality indicators    # Check for service types    # Analyze keyword intent    # Return (category, subcategory)
    ```
    
4.  Apply function to all rows
    
5.  Manual review of edge cases
    

#### Phase 3: Quality Control & Export (1-2 hours)

-   Validate all rows have categories assigned
-   Review consistency of mappings
-   Handle ambiguous cases with contextual analysis
-   Update Google Sheets with new columns
-   Export as Excel/CSV backup
-   Share via Google Drive

**Estimated Time:** 5-7 hours

---

## Overall Project Timeline

### **Day 1 (8-10 hours):**

-   ✅ Task 1: MagicPin Gym Scraping (Complete)
-   ✅ Task 3: OpenStreetMap API (Complete)
-   🔄 Task 2: Amazon Scraping (Setup + Initial Development)

### **Day 2 (8-10 hours):**

-   ✅ Task 2: Amazon Scraping (Complete + Data Cleaning)
-   🔄 Task 4: Data Mapping (Setup + Mapping Logic)

### **Day 3 (4-6 hours):**

-   ✅ Task 4: Data Mapping (Complete + Quality Control)
-   ✅ Final Review & Testing
-   ✅ Package deliverables and submit

---

## Technical Stack & Libraries

**Core Libraries:**

-   `selenium` - Browser automation for dynamic content
-   `beautifulsoup4` - HTML parsing
-   `scrapy` - Alternative framework for large-scale scraping
-   `pandas` - Data manipulation and CSV export
-   `requests` - HTTP requests
-   `overpy` - OpenStreetMap Overpass API wrapper
-   `gspread` - Google Sheets automation

**Anti-Bot Tools:**

-   `fake-useragent` - User-agent rotation
-   `scrapy-rotating-proxies` - Proxy management
-   `undetected-chromedriver` - Stealth browser

**Data Cleaning:**

-   `pandas` - Deduplication, format standardization
-   `re` (regex) - Pattern matching for data extraction

---

## Best Practices Checklist

### Web Scraping Ethics & Performance

-   ✅ Check robots.txt before scraping
-   ✅ Implement rate limiting (2-8 second delays)
-   ✅ Use rotating user-agents
-   ✅ Rotate proxies to avoid IP bans
-   ✅ Handle errors gracefully with try-except blocks
-   ✅ Implement retry logic for failed requests
-   ✅ Monitor scraper performance

### Data Quality

-   ✅ Remove duplicates using unique identifiers
-   ✅ Handle missing values appropriately
-   ✅ Standardize data formats (dates, currency, text)
-   ✅ Validate data completeness (80-100 entries minimum)
-   ✅ Clean text data (lowercase, trim whitespace)
-   ✅ Export with proper column headers

### Code Organization

-   ✅ Modular functions for each scraping task
-   ✅ Separate data collection, cleaning, and export logic
-   ✅ Error logging for debugging
-   ✅ Configuration file for API keys and credentials
-   ✅ Version control with Git (optional but recommended)

---

## Deliverables Checklist

**Task 1:**

-    `ahmedabad_gyms.csv` (80-100+ entries, 7 columns)

**Task 2:**

-    `amazon_products.csv` (80-100+ entries, 6 columns)

**Task 3:**

-    `tourist_attractions_[city_name].csv` (80-100+ entries, 5 columns)

**Task 4:**

-    Updated Google Sheet 1 with Category & Sub-Category columns
-    Updated Google Sheet 2 with Category & Sub-Category columns
-    Excel/CSV backup files (optional)

**Submission:**

-    Email all deliverables to [career@honeybeedigital.com](mailto:career@honeybeedigital.com)
-    Include brief documentation (optional but impressive)
-    Mention any challenges faced and solutions implemented

---

## Risk Mitigation Strategies

### High-Risk Areas:

1.  **Amazon Anti-Bot Detection**
    
    -   **Mitigation:** Use stealth browser, rotate proxies aggressively, implement exponential backoff
    -   **Backup:** If blocked, use smaller sample size and explain in submission
2.  **MagicPin Dynamic Content**
    
    -   **Mitigation:** Use Selenium with proper wait conditions
    -   **Backup:** Manual verification of first 10-20 entries
3.  **Google Sheets API Rate Limits**
    
    -   **Mitigation:** Batch operations, implement retry with backoff
    -   **Backup:** Work with CSV exports as intermediate format
4.  **Time Management**
    
    -   **Mitigation:** Prioritize Tasks 1 & 3 (simpler) first
    -   **Backup:** Submit partial work if needed, with clear documentation

---

## Pro Tips for Success

1.  **Start with smaller samples** (10-20 entries) to validate your scraping logic before scaling to 80-100
    
2.  **Save intermediate progress** - Export data frequently to avoid losing work
    
3.  **Document your code** - Add comments explaining complex logic
    
4.  **Test error handling** - Intentionally break things to ensure your error handling works
    
5.  **Monitor execution time** - Use logging to track how long each task takes
    
6.  **Keep credentials secure** - Use environment variables or config files, never hardcode
    
7.  **Version your outputs** - Use timestamps in filenames (e.g., `gyms_20251030.csv`)
    

---

## Additional Resources

### Web Scraping Documentation

-   Selenium Documentation: [https://selenium-python.readthedocs.io/](https://selenium-python.readthedocs.io/)
-   BeautifulSoup 4 Documentation: [https://www.crummy.com/software/BeautifulSoup/bs4/doc/](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
-   Scrapy Documentation: [https://docs.scrapy.org/](https://docs.scrapy.org/)

### API Documentation

-   Overpass API: [https://wiki.openstreetmap.org/wiki/Overpass_API](https://wiki.openstreetmap.org/wiki/Overpass_API)
-   Google Sheets API: [https://developers.google.com/sheets/api](https://developers.google.com/sheets/api)
-   Python Overpy: [https://python-overpy.readthedocs.io/](https://python-overpy.readthedocs.io/)

### Data Handling

-   Pandas Documentation: [https://pandas.pydata.org/docs/](https://pandas.pydata.org/docs/)
-   Python Regex: [https://docs.python.org/3/library/re.html](https://docs.python.org/3/library/re.html)

---

**Last Updated:** October 30, 2025  
**Status:** Ready for Implementation