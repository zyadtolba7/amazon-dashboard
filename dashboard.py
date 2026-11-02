# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.io as pio

st.set_page_config(page_title="Amazon Sales Dashboard", page_icon="📦", layout="wide")

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

total_products = len(df)
avg_price = df['discounted_price'].mean()
avg_rating = df['rating'].mean()
avg_discount = df['discount_percentage'].mean()

# تجهيز داتا الشارت
cat_counts = df['main_category'].value_counts().head(7).reset_index()
cat_counts.columns = ['Category', 'Count']

fig = px.bar(cat_counts, x='Category', y='Count', 
             color='Count', color_continuous_scale='Purples',
             text_auto=True)

# التعديلات عشان الكتابة تبان
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
    font=dict(color='#8B92A5', size=12), # تصغير الخط شوية
    margin=dict(l=10, r=10, t=20, b=50), # زيادة المسافة من تحت (b)
    height=350, # تكبير الارتفاع
    showlegend=False, coloraxis_showscale=False,
    xaxis=dict(showgrid=False, zeroline=False, title="", tickangle=-15), # لف الأسماء شوية
    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False, title="Products Count")
)
fig.update_traces(marker_line_width=0, textposition='outside', textfont=dict(color='white', size=14))

chart_html = pio.to_html(fig, full_html=False, config={'displayModeBar': False})

top_cats = df['main_category'].value_counts().head(3)
cat1, cat2, cat3 = top_cats.index[0], top_cats.index[1], top_cats.index[2]
pct1 = int((top_cats.iloc[0] / total_products) * 100)
pct2 = int((top_cats.iloc[1] / total_products) * 100)
pct3 = int((top_cats.iloc[2] / total_products) * 100)

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

        .kpi-row {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }}
        .kpi-card {{ background: #151A25; border: 1px solid #1F2633; border-radius: 16px; padding: 24px; }}
        .kpi-title {{ font-size: 14px; color: #8B92A5; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }}
        .kpi-value {{ font-size: 32px; font-weight: 700; margin-bottom: 15px; }}
        .kpi-trend {{ font-size: 13px; display: flex; align-items: center; gap: 5px; }}
        .trend-up {{ color: #00D2A0; }}
        .trend-down {{ color: #FF5C5C; }}
        .kpi-icon {{
            width: 32px; height: 32px; border-radius: 8px;
            display: flex; justify-content: center; align-items: center;
            background: rgba(108, 92, 231, 0.1); color: #6C5CE7;
        }}

        .bottom-row {{ display: grid; grid-template-columns: 2fr 1fr; gap: 20px; }}
        .chart-card, .list-card {{ background: #151A25; border: 1px solid #1F2633; border-radius: 16px; padding: 24px; }}
        .card-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }}
        .card-header h3 {{ margin: 0; font-size: 18px; color: #FFFFFF; }}
        .card-header p {{ margin: 5px 0 0 0; font-size: 13px; color: #8B92A5; }}
        .live-badge {{ font-size: 12px; color: #6C5CE7; border: 1px solid rgba(108, 92, 231, 0.3); padding: 4px 10px; border-radius: 20px; }}

        .channel-item {{ margin-bottom: 25px; }}
        .channel-header {{ display: flex; justify-content: space-between; font-size: 14px; margin-bottom: 8px; color: #FFFFFF; }}
        .progress-bg {{ background: #2A303C; height: 6px; border-radius: 4px; overflow: hidden; }}
        .progress-bar {{ height: 100%; border-radius: 4px; }}
        
        .btn-full {{ width: 100%; background: #1F2633; color: white; border: none; padding: 12px; border-radius: 8px; margin-top: 20px; cursor: pointer; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>Amazon Products Dashboard</h1>
            <p>Live metrics, real data analytics, and product performance.</p>
        </div>
        <div class="header-buttons">
            <button>🔄 Sync Data</button>
            <button class="primary">📥 Export Report (CSV)</button>
        </div>
    </div>

    <div class="kpi-row">
        <div class="kpi-card">
            <div class="kpi-title">Total Products <div class="kpi-icon">📦</div></div>
            <div class="kpi-value">{total_products:,}</div>
            <div class="kpi-trend"><span class="trend-up">▲ Live</span> from dataset</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Avg Rating <div class="kpi-icon">⭐</div></div>
            <div class="kpi-value">{avg_rating:.2f} / 5.0</div>
            <div class="kpi-trend"><span class="trend-up">▲ Good</span> overall rating</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Avg Price <div class="kpi-icon">$</div></div>
            <div class="kpi-value">₹{avg_price:,.0f}</div>
            <div class="kpi-trend"><span class="trend-down">▼ Discount</span> applied</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Avg Discount <div class="kpi-icon">⚡</div></div>
            <div class="kpi-value">{avg_discount:.1f}%</div>
            <div class="kpi-trend"><span class="trend-up">▲ +High</span> savings</div>
        </div>
    </div>

    <div class="bottom-row">
        <div class="chart-card">
            <div class="card-header">
                <div>
                    <h3>Top Categories by Product Count</h3>
                    <p>عدد المنتجات في كل فئة</p>
                </div>
                <div class="live-badge">● Live Sync</div>
            </div>
            <div style="width: 100%;">
                {chart_html}
            </div>
        </div>

        <div class="list-card">
            <div class="card-header">
                <div>
                    <h3>Top Categories</h3>
                    <p>Products breakdown</p>
                </div>
            </div>
            
            <div class="channel-item">
                <div class="channel-header"><span>{cat1}</span><span>{pct1}%</span></div>
                <div class="progress-bg"><div class="progress-bar" style="width: {pct1}%; background: #6C5CE7;"></div></div>
            </div>
            <div class="channel-item">
                <div class="channel-header"><span>{cat2}</span><span>{pct2}%</span></div>
                <div class="progress-bg"><div class="progress-bar" style="width: {pct2}%; background: #A29BFE;"></div></div>
            </div>
            <div class="channel-item">
                <div class="channel-header"><span>{cat3}</span><span>{pct3}%</span></div>
                <div class="progress-bg"><div class="progress-bar" style="width: {pct3}%; background: #00D2A0;"></div></div>
            </div>
            
            <button class="btn-full">Detailed Attribution</button>
        </div>
    </div>
</body>
</html>
"""

components.html(html_content, height=850, scrolling=True)