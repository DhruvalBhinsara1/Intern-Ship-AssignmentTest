### Task 1: Scraping Gyms from MagicPin (Ahmedabad)

1. I explored the MagicPin gym listing page to understand how gym data is presented and which elements to target.
2. I used Selenium to open the page and scrolled several times to make sure all gyms were loaded and visible for extraction.
3. I parsed the page source with BeautifulSoup and focused on <article> tags with the 'store' class to reliably find each gym entry.
4. For each gym, I grabbed the name from heading tags and the area from the 'merchant-location' section, which gave the most accurate location info.
5. I built the address using the area, city, and state, and set phone/timings as 'N/A' since these details weren't available in the listings.
6. I cleaned the data by removing duplicates and saved the final results to 'Task 1/ahmedabad_gyms.csv' in the format requested.

**Data Format:**
- Gym Name
- Address
- Area
- City
- State
- Phone Number (optional)
- Timings (optional)