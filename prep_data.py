import pandas as pd
import time
import re

file_name = "amazon.csv"
output_name = "amazon_clean.csv"

print("⏳ جاري قراءة البيانات...")
start = time.time()
df = pd.read_csv(file_name)
print(f"✅ تم قراءة {len(df):,} صف.")

print("🧹 جاري تنظيف البيانات...")

# 1. تنظيف الأسعار (شيل علامة العملة والفواصل)
def clean_price(price_str):
    if pd.isna(price_str):
        return None
    # شيل أي حاجة مش رقم أو نقطة
    clean_str = re.sub(r'[^\d.]', '', str(price_str))
    try:
        return float(clean_str)
    except ValueError:
        return None

df['discounted_price'] = df['discounted_price'].apply(clean_price)
df['actual_price'] = df['actual_price'].apply(clean_price)

# 2. تنظيف نسبة الخصم
df['discount_percentage'] = df['discount_percentage'].astype(str).str.replace('%', '', regex=False)
df['discount_percentage'] = pd.to_numeric(df['discount_percentage'], errors='coerce')

# 3. تنظيف عدد التقييمات
df['rating_count'] = df['rating_count'].astype(str).str.replace(',', '', regex=False)
df['rating_count'] = pd.to_numeric(df['rating_count'], errors='coerce')

# 4. تنظيف التقييم (rating) وتحويله لرقم
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

# 5. فصل الفئة الرئيسية (عشان عشان الداشبورد يكون مرتب)
df['main_category'] = df['category'].astype(str).str.split('|').str[0]

# 6. حذف الأعمدة اللي مش محتاجينها في التحليل (زي اللينكات والوصف الطويل)
cols_to_drop = ['img_link', 'product_link', 'about_product', 'review_content', 'user_id', 'review_id']
df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])

# 7. حذف الصفوف اللي فيها قيم ناقصة في الأعمدة المهمة
df = df.dropna(subset=['discounted_price', 'actual_price', 'rating'])

print(f"📊 عدد الصفوف بعد التنظيف: {len(df):,}")

# حفظ الملف
df.to_csv(output_name, index=False)
print(f"✅ تم حفظ الملف: {output_name}")
print(f"⏱️ استغرقت العملية: {time.time() - start:.1f} ثانية.")