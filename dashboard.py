# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import io

st.set_page_config(page_title="Amazon Dashboard", page_icon="📦", layout="wide")

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

# الفلاتر
st.sidebar.title("Filters")
all_cats = sorted(df['main_category'].dropna().unique().tolist())
selected_cats = st.sidebar.multiselect("Product Category", options=all_cats, default=all_cats)

filtered_df = df[df['main_category'].isin(selected_cats)] if selected_cats else df

# الأزرار
st.title("📦 Amazon Products Dashboard")
st.markdown("Live metrics, real data analytics, and product performance.")

col_btn1, col_btn2, _ = st.columns([1, 1, 4])
with col_btn1:
    if st.button("🔄 Sync Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
with col_btn2:
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Export CSV", data=csv, file_name='amazon_data_export.csv', mime='text/csv', use_container_width=True)

st.markdown("---")

# الأرقام
total_products = len(filtered_df)
avg_rating = filtered_df['rating'].mean()
avg_price = filtered_df['discounted_price'].mean()
avg_discount = filtered_df['discount_percentage'].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Products", f"{total_products:,}")
col2.metric("Avg Rating", f"{avg_rating:.2f} ⭐")
col3.metric("Avg Price", f"₹{avg_price:,.0f}")
col4.metric("Avg Discount", f"{avg_discount:.1f}%")

st.markdown("---")
st.subheader("Top Categories by Product Count")

# تجهيز الداتا
cat_counts = filtered_df['main_category'].value_counts().head(7).reset_index()
cat_counts.columns = ['Category', 'Count']

# ============================================================
# رسم الشارت بـ HTML/CSS (أعمدة رأسية زي اللي في الصورة)
# ============================================================
max_count = cat_counts['Count'].max()

bars_html = ""
for _, row in cat_counts.iterrows():
    name = row['Category']
    count = row['Count']
    
    # حساب طول العمود كنسبة من أعلى رقم
    height_pct = (count / max_count) * 100
    
    # حساب مكان الرقم (فوق العمود بشوية)
    number_position = height_pct + 5

    bars_html += f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: flex-end; height: 300px; flex: 1; margin: 0 5px;">
        <div style="position: relative; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: flex-end;">
            <!-- الرقم فوق -->
            <div style="position: absolute; bottom: {number_position}%; width: 100%; text-align: center; color: white; font-weight: bold; font-size: 14px;">
                {count}
            </div>
            <!-- العمود -->
            <div style="width: 100%; height: {height_pct}%; background: linear-gradient(180deg, #8E7CFF, #6C5CE7); border-radius: 4px 4px 0 0; transition: 0.3s;">
            </div>
        </div>
        <!-- اسم الفئة (مقطوع عشان ميبوظش الشكل) -->
        <div style="margin-top: 10px; color: #8B92A5; font-size: 12px; text-align: center; word-wrap: break-word; width: 100%; height: 40px; overflow: hidden;">
            {name}
        </div>
    </div>
    """

chart_html = f"""
<div style="display: flex; justify-content: space-between; align-items: flex-end; padding: 20px; background-color: #151A25; border: 1px solid #1F2633; border-radius: 16px; margin-top: 20px; height: 400px;">
    {bars_html}
</div>
"""

components.html(chart_html, height=450, scrolling=False)