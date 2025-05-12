# 🕵️‍♂️ MetaHunt – Intelligent Web Crawler & Analyzer

MetaHunt is a full-stack intelligent web crawler and data analysis dashboard that extracts, analyzes, and visualizes eCommerce product data from [Etsy](https://www.etsy.com). It combines crawling, RSS feed parsing, public API consumption, and data visualization in one seamless pipeline — all packed into a beautiful Streamlit interface.

---

## 🚀 Features

- ✅ **Smart Crawling** with `undetected_chromedriver` and `Selenium`
- 📜 **robots.txt Respect** via `urllib.robotparser`
- 📰 **Live RSS Feed Parsing** from Etsy Shops
- 🔌 **Public API Integration** (Etsy Open API)
- 📊 **Interactive Dashboards** with `Streamlit` + `Plotly`
- 🗺️ **Auto-Generated Visual Sitemaps** using `Graphviz`
- 📁 **Excel Export** of all collected data

---

## 📂 Project Structure
MetaHunt/
│
├── MetaHunt.py # Main web crawler logic using Selenium
├── Streamlit.py # Dashboard application
├── EtsyData.xlsx # Output: collected & cleaned product data
├── README.md # You're reading it 😉
└── requirements.txt # Dependencies



---

## 🧠 Tech Stack

| Tool/Library        | Purpose                         |
|---------------------|----------------------------------|
| `undetected_chromedriver` | Stealth web automation |
| `selenium`          | Dynamic web interaction         |
| `feedparser`        | Etsy shop RSS parsing           |
| `pandas`            | Data wrangling & storage        |
| `plotly`            | Rich interactive charts         |
| `streamlit`         | Lightweight dashboard UI        |
| `graphviz`          | Sitemap visualization           |
| `requests`          | API calls                       |

---

## 📦 Installation

> ⚠ Ensure [Chrome](https://www.google.com/chrome/) is installed and matches your ChromeDriver version.

# Clone the repo
git clone https://github.com/yourusername/MetaHunt.git
cd MetaHunt

# Install dependencies
pip install -r requirements.txt

## ▶️ Run the Crawler
python crawler.py
- This will:
- Respect robots.txt rules
- Extract product data from Etsy's Jewelry section
- Parse latest items from shop RSS feeds
- Fetch selected data using Etsy's public API
- Save all data to EtsyData.xlsx

## 🤖 Crawlability Score Formula
score = (allowed / (allowed + disallowed)) * 70 + (sitemaps / (sitemaps + 1000)) * 30


## 🙌 Authors
Abdalla Sherif Omar – Lead Developer & Analyst
Salma Kurdi
Zeyad Atef
Ahmed Sharaf
