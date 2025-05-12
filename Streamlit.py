import streamlit as st
import pandas as pd
import plotly.express as px
import graphviz

# ========== Load Data ========== 
df = pd.read_excel("EtsyData.xlsx", sheet_name="Product Data")  # Load data from the Excel file
df_rss = pd.read_excel("EtsyData.xlsx", sheet_name="RSS Feed")

# ========== Crawlability Score Calculation ========== 
allowed = 87
disallowed = 1423
sitemaps = 461

crawlability_score = (allowed / (allowed + disallowed)) * 70 + (sitemaps / (sitemaps + 1000)) * 30
crawlability_score = round(crawlability_score, 2)

recommendations = [
    "Use Selenium or Puppeteer for dynamic content.",
    "Avoid crawling during peak hours to reduce detection.",
    "Respect robots.txt and rate limits.",
]

# ========== Streamlit App ========== 
st.set_page_config(page_title="MetaHunt Dashboard", layout="wide")

# Styling for Streamlit
st.markdown("""
    <style>
        .header {
            color: #ff6f61;
            font-size: 2rem;
            font-weight: bold;
        }
        .subheader {
            font-size: 1.2rem;
            color: #6c757d;
        }
        .metric {
            font-size: 2rem;
            font-weight: bold;
        }
        .st-progress {
            height: 10px;
            border-radius: 5px;
        }
        .st-dataframe {
            border-radius: 8px;
        }
        .recommendation {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 15px 20px;
            margin: 10px 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
            font-size: 1rem;
            color: black;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .recommendation:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Title of the App
st.title("📊 MetaHunt – Crawl & Data Analysis Dashboard")

# ========== Crawlability Score ========== 
st.header("🚦 Crawlability Score", anchor="crawlability")
st.metric(label="Crawlability", value=f"{crawlability_score} / 100", delta=None, delta_color="normal")
st.progress(crawlability_score / 100)

# ========== Extracted Data ========== 
st.header("🛍️ Top Extracted Products")
st.subheader("Displaying top 10 extracted products")
st.dataframe(df.head(10), use_container_width=True)

# Optional: Visualize top prices
if 'price' in df.columns:
    try:
        df['price'] = df['price'].replace({'\$': '', ',': ''}, regex=True)  # Clean the price data
        df['price'] = pd.to_numeric(df['price'], errors='coerce')  # Convert to numeric
        fig = px.bar(df.head(10), x='description', y='price', title="Top Product Prices", color='description', color_continuous_scale="Viridis")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"Error plotting price data: {e}")


# ========== RSS Feeds from Etsy Shops ========== 
st.header("📰 Etsy Shop RSS Feed")

if df_rss.empty:
    st.warning("No RSS entries found.")
else:
    st.subheader("Recent Feed Items from Etsy Shops")
    selected_shop = st.selectbox("Select a shop to view latest RSS items:", df_rss['shop'].unique())

    filtered_rss = df_rss[df_rss['shop'] == selected_shop]
    filtered_rss = filtered_rss.sort_values(by="published", ascending=False)  # Sort by latest
    
    # Limit to top 10 entries
    top_10_rss = filtered_rss.head(10)
    
    # Display the table
    st.table(top_10_rss[['title', 'published', 'shop', 'link']])  # Display selected columns in the table

    


# ========== Recommendations ========== 
st.header("🧠 Crawling Recommendations")
for rec in recommendations:
    st.markdown(f"<div class='recommendation'>{rec}</div>", unsafe_allow_html=True)

# ========== Visual Sitemap ========== 
st.header("🗺️ Visual Sitemap (Mocked)")
dot = graphviz.Digraph(format="png", engine="dot")

dot.node("Home", "Homepage")
dot.node("Cat1", "Jewelry Category")
dot.node("P1", "Product 1")
dot.node("P2", "Product 2")
dot.edges([("Home", "Cat1"), ("Cat1", "P1"), ("Cat1", "P2")])

# Display the sitemap as an image
st.graphviz_chart(dot)

st.caption("🧩 Sitemap generated for demonstration.")


# to Run the Code
# streamlit run d:/Studio/MSA/Spring25/IR/MetaHunt/Streamlit.py
