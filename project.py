import pandas as pd
import snowflake.connector
import os
import sys

# Ensure UTF-8 encoding for console output (important for Windows)
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# ============================================
# الخطوة 1: قراءة الداتا من Kaggle
# ============================================
print("📥 بنقرا الداتا...")
if not os.path.exists("train.csv"):
    print("❌ Error: train.csv not found! Please make sure the file is in the same directory.")
    exit()
df = pd.read_csv("train.csv")
print(f"✅ الداتا اتقرأت — {df.shape[0]} صف و {df.shape[1]} عمود")

# ============================================
# الخطوة 2: Transformation — تنظيف الداتا
# ============================================
print("\n🔧 بننظف الداتا...")

# صلح القيم الفاضية في Postal Code
df['Postal Code'] = df['Postal Code'].fillna(0).astype(int)

# حول التواريخ لـ datetime
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
df['Ship Date']  = pd.to_datetime(df['Ship Date'],  dayfirst=True)

# قرب الأرقام لـ خانتين عشريتين
df['Sales'] = df['Sales'].round(2)

# أضف أعمدة جديدة مفيدة
df['Order Year']    = df['Order Date'].dt.year
df['Order Month']   = df['Order Date'].dt.month
df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days

# شيل أعمدة مش محتاجينها
df = df.drop(columns=['Row ID', 'Country'])

print(f"✅ الداتا اتنظفت — مفيش قيم فاضية")
print(f"   أعمدة جديدة اتضافت: Order Year, Order Month, Shipping Days")

# احفظ الداتا النظيفة
df.to_csv("clean_data.csv", index=False)
print("✅ اتحفظت في clean_data.csv")

# حول التواريخ لـ نصوص عشان Snowflake ميزعلش
df['Order Date'] = df['Order Date'].dt.strftime('%Y-%m-%d')
df['Ship Date']  = df['Ship Date'].dt.strftime('%Y-%m-%d')

# ============================================
# الخطوة 3: Loading — ارفع على Snowflake
# ============================================
print("\n☁️ بنتصل بـ Snowflake...")

# ← غير البيانات دي ببياناتك الشخصية
SNOWFLAKE_CONFIG = {
    "user":     "AHMED123",
    "password": "AhmedAli123###",
    "account":  "dvudgep-bm48830",
    "warehouse":"COMPUTE_WH",
    "database": "SALES_DB",
    "schema":   "PUBLIC"
}

conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
cur  = conn.cursor()

# اعمل الـ Database والـ Table
cur.execute("CREATE DATABASE IF NOT EXISTS SALES_DB")
cur.execute("USE DATABASE SALES_DB")
cur.execute("""
    CREATE TABLE IF NOT EXISTS SALES_DATA (
        ORDER_ID       VARCHAR(50),
        ORDER_DATE     DATE,
        SHIP_DATE      DATE,
        SHIP_MODE      VARCHAR(50),
        CUSTOMER_ID    VARCHAR(50),
        CUSTOMER_NAME  VARCHAR(100),
        SEGMENT        VARCHAR(50),
        CITY           VARCHAR(100),
        STATE          VARCHAR(100),
        POSTAL_CODE    INT,
        REGION         VARCHAR(50),
        PRODUCT_ID     VARCHAR(50),
        CATEGORY       VARCHAR(50),
        SUB_CATEGORY   VARCHAR(50),
        PRODUCT_NAME   VARCHAR(300),
        SALES          FLOAT,
        ORDER_YEAR     INT,
        ORDER_MONTH    INT,
        SHIPPING_DAYS  INT
    )
""")

# امسح الداتا القديمة عشان متبقاش متكررة
cur.execute("TRUNCATE TABLE IF EXISTS SALES_DATA")

# ارفع الداتا دفعة واحدة (أسرع بكتير)
print("🚀 بنرفع الداتا لـ Snowflake...")
data = [tuple(row) for row in df.values]
cur.executemany("""
    INSERT INTO SALES_DATA VALUES (
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s
    )
""", data)

conn.commit()
cur.close()
conn.close()
print("✅ الداتا اترفعت على Snowflake!")
