import pandas as pd
import os

file_name = "amazon.csv"

if os.path.exists(file_name):
    print("جاري قراءة أول 1000 صف...\n")
    df = pd.read_csv(file_name, nrows=1000)
    
    print("================ أسماء الأعمدة ================")
    print(df.columns.tolist())
    
    print("\n================ أول 5 صفوف ================")
    print(df.head())
    
    print("\n================ أنواع البيانات ================")
    print(df.dtypes)
    
    print("\n================ القيم الناقصة ================")
    print(df.isnull().sum())
else:
    print("مش لاقي الملف amazon.csv في الفولدر ده.")