# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.io as pio

st.set_page_config(page_title="Products", page_icon="📦", layout="wide")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container { padding: 0 !important; max-width: 100% !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('amazon_clean.csv')
    for col in ['discounted_price', 'actual_price', 'discount_percentage', 'rating', 'rating_count']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

df = load_data()

# ============================================================
# تعديل الشارت العلوي (أعلى 5 منتجات من حيث السعر)
# ============================================================
top_price_products = df.sort_values('discounted_price', ascending=False).head(5)
top_price_products['short_name'] = top_price_products['product_name'].apply(lambda x: x[:35] + "..." if len(x) > 35 else x)
top_price_products = top_price_products.sort_values('discounted_price', ascending=True)

fig_top = px.bar(top_price_products, x='discounted_price', y='short_name', orientation='h', 
                 color='short_name', color_discrete_sequence=px.colors.qualitative.Pastel,
                 text_auto='.2s')

# التعديلات هنا
fig_top.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#8B92A5', size=12),
    margin=dict(l=10, r=20, t=10, b=50), # المسافة السفلية اترفعت شوية (b=50)
    height=350, showlegend=False, 
    xaxis=dict(
        showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False, 
        title="Price (₹)", title_standoff=25 # رفعنا العنوان بعيد عن الأرقام
    ),
    yaxis=dict(
        showgrid=False, zeroline=False, title="", 
        tickfont=dict(size=12, color='white'), side='left'
    )
)
fig_top.update_traces(marker_line_width=0, textposition='outside', textfont=dict(color='white', size=12))
top_html = pio.to_html(fig_top, full_html=False, config={'displayModeBar': False})


# ============================================================
# الشكل الدائري
# ============================================================
cat_discount = df.groupby('main_category')['discount_percentage'].mean().sort_values(ascending=False).head(5).reset_index()
fig_donut = px.pie(cat_discount, names='main_category', values='discount_percentage', hole=0.6, 
                   color_discrete_sequence=px.colors.sequential.Purples_r)
fig_donut.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#FFFFFF', size=14),
    margin=dict(l=10, r=10, t=30, b=10), height=350, showlegend=True,
    legend=dict(font=dict(color='#8B92A5', size=12))
)
fig_donut.update_traces(textposition='inside', textinfo='percent+label')
donut_html = pio.to_html(fig_donut, full_html=False, config={'displayModeBar': False})


# قائمة أعلى 5 منتجات تقييماً
top_5_products = df.sort_values('rating', ascending=False).head(5)
list_html = ""
for _, row in top_5_products.iterrows():
    name = row['product_name'][:40] + "..." if len(row['product_name']) > 40 else row['product_name']
    list_html += f"""
    <div class="channel-item">
        <div class="channel-header"><span>{name}</span><span>{row['rating']} ⭐</span></div>
        <div class="progress-bg"><div class="progress-bar" style="width: {(row['rating']/5)*100}%; background: #6C5CE7;"></div></div>
    </div>
    """

# ============================================================
# بناء صفحة HTML
# ============================================================
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        * {{ font-family: 'Inter', sans-serif; box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ background-color: #0B0E14; color: #FFFFFF; padding: 30px; }}

        .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }}
        .header h1 {{ font-size: 28px; color: #FFFFFF; margin-bottom: 5px; }}
        .header p {{ font-size: 14px; color: #8B92A5; }}
        .header-buttons button {{
            background: transparent; border: 1px solid #2A303C; color: #FFFFFF;
            padding: 10px 20px; border-radius: 8px; cursor: pointer; margin-left: 10px;
            display: inline-flex; align-items: center; gap: 8px; font-size: 14px;
        }}
        .header-buttons button.primary {{ background: linear-gradient(90deg, #6C5CE7, #8E7CFF); border: none; }}

        .row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }}
        .chart-card, .list-card {{ background: #151A25; border: 1px solid #1F2633; border-radius: 16px; padding: 24px; }}
        .card-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }}
        .card-header h3 {{ margin: 0; font-size: 18px; color: #FFFFFF; }}
        .card-header p {{ margin: 5px 0 0 0; font-size: 13px; color: #8B92A5; }}

        .channel-item {{ margin-bottom: 20px; }}
        .channel-header {{ display: flex; justify-content: space-between; font-size: 14px; margin-bottom: 8px; color: #FFFFFF; }}
        .progress-bg {{ background: #2A303C; height: 6px; border-radius: 4px; overflow: hidden; }}
        .progress-bar {{ height: 100%; border-radius: 4px; }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>Products & Performance</h1>
            <p>تحليل أداء المنتجات والتقييمات.</p>
        </div>
        <div class="header-buttons">
            <button>🔄 Sync Data</button>
            <button class="primary">📥 Export Data</button>
        </div>
    </div>

    <div class="chart-card">
        <div class="card-header">
            <div>
                <h3>Top 5 Most Expensive Products</h3>
                <p>أعلى 5 منتجات من حيث السعر</p>
            </div>
        </div>
        <div style="width: 100%;">
            {top_html}
        </div>
    </div>

    <div class="row">
        <div class="chart-card">
            <div class="card-header">
                <div>
                    <h3>Top 5 Categories by Avg Discount</h3>
                    <p>نسبة الفئات في متوسط الخصم</p>
                </div>
            </div>
            <div style="width: 100%;">
                {donut_html}
            </div>
        </div>

        <div class="list-card">
            <div class="card-header">
                <div>
                    <h3>Top Rated Products</h3>
                    <p>أعلى 5 منتجات في التقييم</p>
                </div>
            </div>
            {list_html}
        </div>
    </div>
</body>
</html>
"""

components.html(html_content, height=1100, scrolling=True)