code docs/data_cleaning_explained.md
# 🧼 Data Cleaning and Enrichment Pipeline — Automobile Sales Dataset

## Overview
This document explains the full **data cleaning and enrichment process** applied to the Automobile Sales dataset.  
It transforms raw transactional data into an **analytics-ready format** for business intelligence, dashboards, and modeling.

---

## 🧱 1. Handle Missing or Invalid Values
- **Remove empty rows** and rows missing key fields like `ORDERNUMBER`, `CUSTOMERNAME`, or `ORDERDATE`.
- **Fill missing categorical values** (like addresses or postal codes) with placeholders.

✅ *Purpose:* Ensures data integrity before analysis.

---

## 📆 2. Temporal Features
Extracted:
- `ORDER_YEAR`
- `ORDER_MONTH`
- `ORDER_QUARTER`

✅ *Purpose:* Enables time-based grouping and trend visualization.

---

## 💰 3. Monetary Consistency and Metrics
Converted numeric columns and computed:
- `COST = QUANTITYORDERED × PRICEEACH × 0.8`
- `PROFIT_MARGIN = PROFIT / SALES`

✅ *Purpose:* Builds financial KPIs for profitability tracking.

---

## 🧠 4. Outlier Detection (IQR Method)
Filtered sales values outside 1.5 × IQR from the 25th–75th percentile.

✅ *Purpose:* Prevents extreme outliers from skewing analysis.

---

## 👥 5. Customer Segmentation Prep
Calculated per customer:
- `TOTAL_ORDERS`
- `AVG_ORDER_VALUE`

✅ *Purpose:* Supports CLV and customer retention insights.

---

## 🌍 6. Normalize Categorical Data
Standardized text fields like:
- `COUNTRY`, `CITY`, `PRODUCTLINE`

✅ *Purpose:* Avoids duplication errors during aggregation.

---

## 📊 7. Derived Analytical Fields
Added:
- `PROFIT_PER_UNIT`
- `DAYS_SINCE_LASTORDER`
- `DEALSIZE_SEGMENT` (Small, Medium, Large, Enterprise)

✅ *Purpose:* Enables behavioral and profitability segmentation.

---

## 🧾 8. Save Final Dataset
```python
df.to_csv('data_cleaned/automobile_sales_final.csv', index=False)


🗃️ Next Steps

Move to SQL Phase:

Load automobile_sales_final.csv into a SQL database (e.g., MySQL or PostgreSQL).

Begin query-based validation and relational modeling.

Dashboarding Phase (After SQL):

Import cleaned data into Power BI, Looker, or IBM Cognos for KPI visualization.