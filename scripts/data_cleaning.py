import pandas as pd
import os

df = pd.read_excel(r"C:\Users\ADMIN\Desktop\AutomobileSalesProject\automobile_salesdata.xlsx")
print(df.shape)
print(df.head())
print(df.info())
print(df.describe())

# Handle missing Values
df.columns = df.columns.str.strip().str.upper()

# Remove completely empty rows
df.dropna(how='all', inplace=True)

# Fill missing postal codes or addresses with placeholders
df['POSTALCODE'] = df['POSTALCODE'].fillna('Unknown')
df['ADDRESSLINE1'] = df['ADDRESSLINE1'].fillna('N/A')

# Create Temporal Features_ Month, Quarter, Year
df['ORDER_YEAR'] = df['ORDERDATE'].dt.year
df['ORDER_MONTH'] = df['ORDERDATE'].dt.month
df['ORDER_QUARTER'] = df['ORDERDATE'].dt.to_period('Q')

# Refine Monetary Fields
df['SALES'] = pd.to_numeric(df['SALES'], errors='coerce')
df['PRICEEACH'] = pd.to_numeric(df['PRICEEACH'], errors='coerce')
df['QUANTITYORDERED'] = pd.to_numeric(df['QUANTITYORDERED'], errors='coerce')

# Calculate total cost and profit margin
df['PROFIT'] = (df['PRICEEACH'] - (df['MSRP'] * 0.8)) * df['QUANTITYORDERED']
df['COST'] = df['QUANTITYORDERED'] * df['PRICEEACH'] * 0.8
df['PROFIT_MARGIN'] = (df['PROFIT'] / df['SALES']).round(2)

#Detect and handle outliers in SALES
Q1 = df['SALES'].quantile(0.25)
Q3 = df['SALES'].quantile(0.75)
IQR = Q3 - Q1

# Filter out extreme outliers
df = df[(df['SALES'] >= (Q1 - 1.5 * IQR)) & (df['SALES'] <= (Q3 + 1.5 * IQR))]

# Drop rows missing essential transaction info
df.dropna(subset=['ORDERNUMBER', 'CUSTOMERNAME', 'ORDERDATE', 'SALES'], inplace=True)

# Fill missing postal codes or addresses with placeholders
df['POSTALCODE'] = df['POSTALCODE'].fillna('Unknown')
df['ADDRESSLINE1'] = df['ADDRESSLINE1'].fillna('N/A')

# Convert date fields
df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'], errors='coerce')

# Calculate profit
df['PROFIT'] = df['SALES'] - (df['QUANTITYORDERED'] * df['PRICEEACH'] * 0.8)

# Identify repeat vs one-time customers
df['CUSTOMER_TYPE'] = df.duplicated(subset=['CUSTOMERNAME'], keep=False).map({True: 'Repeat', False: 'One-Time'})
# Convert date fields
df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'], errors='coerce')

# Calculate profit
df['PROFIT'] = df['SALES'] - (df['QUANTITYORDERED'] * df['PRICEEACH'] * 0.8)

# Identify repeat vs one-time customers
df['CUSTOMER_TYPE'] = df.duplicated(subset=['CUSTOMERNAME'], keep=False).map({True: 'Repeat', False: 'One-Time'})

# Customer Segmentation Prep
# Total orders per customer
customer_orders = df.groupby('CUSTOMERNAME')['ORDERNUMBER'].nunique().rename('TOTAL_ORDERS')
df = df.merge(customer_orders, on='CUSTOMERNAME', how='left')

# Average order value per customer
customer_avg = df.groupby('CUSTOMERNAME')['SALES'].mean().rename('AVG_ORDER_VALUE')
df = df.merge(customer_avg, on='CUSTOMERNAME', how='left')

# Normalize and Categorize Data
# Standardize text fields
df['COUNTRY'] = df['COUNTRY'].str.strip().str.title()
df['CITY'] = df['CITY'].str.strip().str.title()
df['PRODUCTLINE'] = df['PRODUCTLINE'].str.strip().str.title()

#Add Calculated Fields  
# Profit per unit
df['PROFIT_PER_UNIT'] = (df['PROFIT'] / df['QUANTITYORDERED']).round(2)

# Days since previous order for same customer
df = df.sort_values(['CUSTOMERNAME', 'ORDERDATE'])
df['DAYS_SINCE_LASTORDER'] = df.groupby('CUSTOMERNAME')['ORDERDATE'].diff().dt.days

# Segment deal size (like in Excel)
df['DEALSIZE_SEGMENT'] = pd.cut(df['SALES'], 
                                bins=[0, 3000, 7000, 15000, float('inf')], 
                                labels=['Small', 'Medium', 'Large', 'Enterprise'])

#Save cleaned data to new Excel file
df.to_csv('automobile_sales_final.csv', index=False)
print("✅ Data cleaning and enrichment complete — saved to data_cleaned/automobile_sales_final.csv")


