import pandas as pd
import matplotlib.pyplot as plt

# قراءة الداتا
df = pd.read_csv('amazon_clean.csv')

# تجهيز الداتا
cat_counts = df['main_category'].value_counts().head(7).reset_index()
cat_counts.columns = ['Category', 'Count']

# إعدادات الخلفية السودة
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 5))

# رسم الشارت
colors = plt.cm.Purples([i/len(cat_counts) for i in range(len(cat_counts))])
bars = ax.barh(cat_counts['Category'], cat_counts['Count'], color=colors)

# إضافة الأرقام على الأعمدة
for bar in bars:
    width = bar.get_width()
    ax.text(width + 5, bar.get_y() + bar.get_height()/2, 
            f'{int(width)}', va='center', ha='left', color='white')

# تنسيق الشكل
ax.set_title('Top Categories by Product Count', color='white', fontsize=16)
ax.set_xlabel('Number of Products', color='gray')
ax.spines['bottom'].set_color('#333')
ax.spines['left'].set_color('#333')
ax.tick_params(axis='x', colors='gray')
ax.tick_params(axis='y', colors='white')

# حفظ الصورة
plt.tight_layout()
plt.savefig("test_chart_mpl.png", dpi=150)
print("✅ تم إنشاء الصورة test_chart_mpl.png بنجاح! افتحها.")