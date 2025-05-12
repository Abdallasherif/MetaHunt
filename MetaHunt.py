import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.robotparser import RobotFileParser
import pandas as pd
import time
import feedparser
import requests
import random

# === Step 1: Check robots.txt ===
rp = RobotFileParser()
rp.set_url("https://www.etsy.com/robots.txt")
rp.read()

user_agent = "*"
test_url = "https://www.etsy.com/c/jewelry"

if rp.can_fetch(user_agent, test_url):
    print("✅ Allowed to crawl:", test_url)
else:
    print("❌ Disallowed to crawl:", test_url)

# === Setup Chrome ===
chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = uc.Chrome(options=chrome_options)

# === Scraping Etsy Products with Pagination ===
url = 'https://www.etsy.com/c/jewelry'
driver.get(url)

# Wait for page to load (first 20 seconds)
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'li.wt-list-unstyled div.v2-listing-card'))
)

print("🔄 Page loaded, starting to scroll...")

# Infinite Scroll: Scroll down the page to load more products
SCROLL_PAUSES = 1  # Number of times to scroll down
product_data = []

for i in range(SCROLL_PAUSES):
    # Scroll to the bottom of the page to load more products
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Wait a few seconds for products to load
    time.sleep(random.uniform(3, 5))  # Wait for new products to load
    
    # Collect products
    products = driver.find_elements(By.CSS_SELECTOR, 'li.wt-list-unstyled div.v2-listing-card')
    print(f"🧲 Page {i+1} - Scraped {len(products)} products.")

    # Extract product details
    for product in products:
        try:
            title = product.find_element(By.CSS_SELECTOR, 'h3').text.strip()
        except:
            title = "N/A"

        try:
            price = product.find_element(By.CSS_SELECTOR, 'span.currency-value').text.strip()
        except:
            price = "N/A"

        try:
            link = product.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        except:
            link = "N/A"

        try:
            reviews = product.find_element(By.CSS_SELECTOR, 'span.wt-text-caption').text.strip()
        except:
            reviews = "N/A"

        try:
            image_url = product.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
        except:
            image_url = "N/A"

        product_data.append({
            'description': title,
            'price': price,
            'link': link,
            'reviews': reviews,
            'image_url': image_url,
        })

    # Pause between scrolls to be polite
    time.sleep(random.uniform(1, 3))

print(f"✅ Total products collected: {len(product_data)}")

df_products = pd.DataFrame(product_data)

# === Scrape RSS Feeds from Etsy Shops ===
shop_names = ["CaitlynMinimalist", "Revelmy"]  # Replace with real shop names
rss_data = []

for shop in shop_names:
    rss_url = f"https://www.etsy.com/shop/{shop}/rss"
    feed = feedparser.parse(rss_url)
    if not feed.entries:
        print(f"⚠ No RSS entries found for shop: {shop}")
        continue
    for entry in feed.entries:
        rss_data.append({
            'shop': shop,
            'title': entry.title,
            'link': entry.link,
            'published': entry.published,
            'summary': entry.summary
        })

df_rss = pd.DataFrame(rss_data)

# === Etsy Internal Public API Data ===
# Updated Etsy API request
api_url = "https://openapi.etsy.com/v2/listings/active"
params = {
    "api_key": "your_api_key",  # Add your API key here
    "category": "jewelry",  # You can add more parameters like this
    "limit": 20
}
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.etsy.com"
}

response = requests.get(api_url, headers=headers, params=params)

api_products = []
if response.status_code == 200:
    try:
        data = response.json()
        product_results = data.get('results', [])
        for item in product_results:
            api_products.append({
                'title': item.get('title', 'N/A'),
                'price': item.get('price', {}).get('value', 'N/A'),
                'currency': item.get('price', {}).get('currency_code', 'N/A'),
                'url': item.get('url', 'N/A'),
                'image': item.get('Images', [{}])[0].get('url_fullxfull', 'N/A') if item.get('Images') else 'N/A',
            })
        print("✅ Fetched public API data.")
    except Exception as e:
        print("⚠ Error parsing API response:", e)
else:
    print("❌ Failed to fetch public API data. Status:", response.status_code)


df_api = pd.DataFrame(api_products)

# === Save All DataFrames to Excel ===
with pd.ExcelWriter('EtsyData.xlsx') as writer:
    df_products.to_excel(writer, sheet_name='Product Data', index=False)
    df_rss.to_excel(writer, sheet_name='RSS Feed', index=False)
    df_api.to_excel(writer, sheet_name='API Data', index=False)

print("✅ Done. Data saved to EtsyData.xlsx")

# === Clean Shutdown ===
driver.quit()
del driver
uc.Chrome.__del__ = lambda self: None  
print("🛑 Chrome closed cleanly.")
