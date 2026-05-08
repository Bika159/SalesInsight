# 📊 Project Documentation: Superstore Sales Data Pipeline
## Academic Submission - Big Biological Data University Project

---

## 🇬🇧 English Version: Technical Documentation

### 1. Project Overview
This project implements a complete **ETL (Extract, Transform, Load)** pipeline designed for large-scale sales data analysis. It demonstrates the integration of Python for data processing, Snowflake as a cloud data warehouse, and Streamlit for professional business intelligence.

### 2. The Data Pipeline
*   **Data Source (`train.csv`)**: A dataset containing ~9,800 rows and 18 columns of retail transactions.
*   **Extraction**: Data is ingested from CSV files using the `Pandas` library.
*   **Transformation (`project.py`)**: 
    *   **Data Cleaning**: Handled missing postal codes and standardized date formats.
    *   **Feature Engineering**: Created new analytical columns: `Order Year`, `Order Month`, and `Shipping Days` (calculating the delta between order and ship dates).
*   **Loading**: The cleaned data is efficiently loaded into **Snowflake** using bulk insertion (`executemany`) for optimal performance.

### 3. Business Intelligence Dashboard (`dashboard.py`)
The final stage provides an interactive environment for stakeholders to monitor KPIs:
*   **Real-time Filtering**: Users can drill down by Region, Category, and Year.
*   **Advanced Analytics**: Includes monthly trends, product performance, and logistical efficiency (shipping speed).
*   **Strategic Insights**: Automated summary highlighting the top market leaders and peak performance periods.

---

## 🇪🇬 النسخة العربية: شرح المشروع

### 1. نظرة عامة على المشروع
المشروع عبارة عن **Data Pipeline** كاملة (خط إنتاج بيانات) لتحليل مبيعات متجر ضخم (Superstore). المشروع بيطبق مفاهيم الـ **ETL** وهي سحب البيانات، معالجتها، ثم تخزينها بشكل احترافي.

### 2. مراحل معالجة البيانات
*   **مصدر البيانات (`train.csv`)**: ملف يحتوي على حوالي 9800 عملية بيع بمختلف تفاصيلها.
*   **المعالجة (`project.py`)**: 
    *   **تنظيف البيانات**: صلحنا القيم الناقصة (مثل الـ Postal Code) وحولنا التواريخ لصيغة يفهمها الكمبيوتر.
    *   **هندسة البيانات**: استخرجنا معلومات جديدة ومفيدة زي (سنة الأوردر، شهر الأوردر، وعدد أيام الشحن) عشان نسهل التحليل.
*   **التخزين**: البيانات النظيفة بتترفع على مخزن بيانات سحابي (**Snowflake**) وده بيسمح بتخزين كميات ضخمة من البيانات والوصول ليها بسرعة.

### 3. لوحة التحكم والتحليل (`dashboard.py`)
دي المرحلة النهائية اللي بتعرض النتائج للدكتور أو صاحب العمل:
*   **الفلاتر (Filters)**: بتسمح لك تختار منطقة معينة (Region) أو نوع منتج (Category) أو سنة محددة، وكل الرسومات بتتحدث فوراً.
*   **التحليلات**: بتعرض إجمالي المبيعات، أفضل 10 مدن، والمنتجات الأكثر مبيعاً، ومعدل سرعة الشحن.
*   **الملخص التنفيذي**: جزء ذكي بيطلع أهم النتائج أوتوماتيكياً زي "أكتر مدينة مبيعات" و "أسرع وسيلة شحن".

---
**Prepared for Academic Review | 2026**
