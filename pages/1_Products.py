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
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv("amazon_clean.csv")
    for col in [
        "discounted_price",
        "actual_price",
        "discount_percentage",
        "rating",
        "rating_count"
    ]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


df = load_data()

# ============================================================
# Top 5 most expensive products
# ============================================================
top_price_products = (
    df.dropna(subset=["discounted_price"])
      .nlargest(5, "discounted_price")
      .copy()
)

top_price_products["product_name"] = (
    top_price_products["product_name"].fillna("").astype(str)
)
top_price_products["short_name"] = top_price_products["product_name"].apply(
    lambda x: x[:35] + "..." if len(x) > 35 else x
)
top_price_products = top_price_products.sort_values(
    "discounted_price", ascending=True
)

fig_top = px.bar(
    top_price_products,
    x="discounted_price",
    y="short_name",
    orientation="h",
    color="short_name",
    color_discrete_sequence=px.colors.qualitative.Pastel,
    text_auto=".2s"
)

fig_top.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#8B92A5", size=12),
    margin=dict(l=10, r=25, t=15, b=55),
    height=350,
    autosize=True,
    showlegend=False,
    dragmode="pan",
    xaxis=dict(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.05)",
        zeroline=False,
        title="Price (₹)",
        title_standoff=18,
        fixedrange=False,
        automargin=True
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        title="",
        tickfont=dict(size=12, color="white"),
        side="left",
        fixedrange=False,
        automargin=True
    ),
    uirevision="top-price-products"
)

fig_top.update_traces(
    marker_line_width=0,
    textposition="outside",
    textfont=dict(color="white", size=12),
    cliponaxis=True
)

# Show Plotly.js once in the iframe; the second chart reuses it.
plot_config = {
    "displayModeBar": True,
    "displaylogo": False,
    "responsive": True,
    "scrollZoom": False,
    "doubleClick": "reset",
    "modeBarButtonsToRemove": ["select2d", "lasso2d"]
}

top_html = pio.to_html(
    fig_top,
    full_html=False,
    include_plotlyjs="cdn",
    config=plot_config
)


# ============================================================
# Donut chart: top 5 categories by average discount
# ============================================================
cat_discount = (
    df.groupby("main_category", dropna=True)["discount_percentage"]
      .mean()
      .sort_values(ascending=False)
      .head(5)
      .reset_index()
)

fig_donut = px.pie(
    cat_discount,
    names="main_category",
    values="discount_percentage",
    hole=0.6,
    color_discrete_sequence=px.colors.sequential.Purples_r
)

fig_donut.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#FFFFFF", size=14),
    margin=dict(l=10, r=10, t=30, b=15),
    height=350,
    autosize=True,
    showlegend=True,
    legend=dict(font=dict(color="#8B92A5", size=12)),
    uirevision="category-discount-donut"
)

fig_donut.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

donut_html = pio.to_html(
    fig_donut,
    full_html=False,
    include_plotlyjs=False,
    config=plot_config
)


# ============================================================
# Top 5 rated products
# ============================================================
top_5_products = (
    df.dropna(subset=["rating"])
      .nlargest(5, "rating")
)

list_html = ""
for _, row in top_5_products.iterrows():
    product_name = str(row.get("product_name", "") or "")
    name = product_name[:40] + "..." if len(product_name) > 40 else product_name
    rating = float(row["rating"])
    rating_width = max(0, min(100, (rating / 5) * 100))

    list_html += f"""
    <div class="channel-item">
        <div class="channel-header">
            <span>{name}</span>
            <span>{rating:.1f} ⭐</span>
        </div>
        <div class="progress-bg">
            <div class="progress-bar"
                 style="width: {rating_width}%; background: #6C5CE7;">
            </div>
        </div>
    </div>
    """


# ============================================================
# HTML page
# ============================================================
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        /* Keep the CSS reset away from Plotly's internal chart elements. */
        * {{ box-sizing: border-box; }}

        body {{
            background-color: #0B0E14;
            color: #FFFFFF;
            padding: 30px;
            margin: 0;
            font-family: 'Inter', sans-serif;
        }}

        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            gap: 16px;
        }}
        .header h1 {{
            font-size: 28px;
            color: #FFFFFF;
            margin: 0 0 5px 0;
        }}
        .header p {{
            font-size: 14px;
            color: #8B92A5;
            margin: 0;
        }}

        .header-buttons button {{
            background: transparent;
            border: 1px solid #2A303C;
            color: #FFFFFF;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            margin-left: 10px;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
        }}
        .header-buttons button.primary {{
            background: linear-gradient(90deg, #6C5CE7, #8E7CFF);
            border: none;
        }}

        .row {{
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
            gap: 20px;
            margin-bottom: 20px;
        }}
        .chart-card, .list-card {{
            min-width: 0;
            background: #151A25;
            border: 1px solid #1F2633;
            border-radius: 16px;
            padding: 24px;
            overflow: hidden;
        }}
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        .card-header h3 {{
            margin: 0;
            font-size: 18px;
            color: #FFFFFF;
        }}
        .card-header p {{
            margin: 5px 0 0 0;
            font-size: 13px;
            color: #8B92A5;
        }}

        .plotly-graph-div {{
            width: 100% !important;
            max-width: 100% !important;
        }}

        .channel-item {{ margin-bottom: 20px; }}
        .channel-header {{
            display: flex;
            justify-content: space-between;
            gap: 12px;
            font-size: 14px;
            margin-bottom: 8px;
            color: #FFFFFF;
        }}
        .channel-header span:first-child {{
            overflow-wrap: anywhere;
        }}
        .progress-bg {{
            background: #2A303C;
            height: 6px;
            border-radius: 4px;
            overflow: hidden;
        }}
        .progress-bar {{ height: 100%; border-radius: 4px; }}

        @media (max-width: 760px) {{
            body {{ padding: 16px; }}
            .header {{
                align-items: flex-start;
                flex-direction: column;
            }}
            .header-buttons button {{
                margin: 0 8px 8px 0;
            }}
            .row {{ grid-template-columns: minmax(0, 1fr); }}
            .chart-card, .list-card {{ padding: 16px; }}
        }}
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

    <div class="chart-card" style="margin-bottom: 20px;">
        <div class="card-header">
            <div>
                <h3>Top 5 Most Expensive Products</h3>
                <p>أعلى 5 منتجات من حيث السعر</p>
            </div>
        </div>
        <div style="width: 100%; min-width: 0;">
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
            <div style="width: 100%; min-width: 0;">
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

components.html(html_content, height=1250, scrolling=False)
