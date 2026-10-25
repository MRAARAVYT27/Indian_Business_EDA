

import pandas as pd
df=pd.read_csv("Sample - Superstore.csv")
print(df.head())
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
print(df.columns.tolist() )
print(df.info)
print(df.isnull().sum())
print(df.duplicated().sum())
print(df.dtypes)
print(df.describe())
df_clean=df.copy()



# Convert Order Date
df_clean["Order Date"] = pd.to_datetime(
    df_clean["Order Date"], errors="coerce"
)

# Convert Ship Date
df_clean["Ship Date"] = pd.to_datetime(
    df_clean["Ship Date"], errors="coerce"
)

# Verify date conversion
print("\n--- DATE DATA TYPES ---")
print(df_clean[["Order Date", "Ship Date"]].dtypes)

print("\n--- MISSING DATE VALUES ---")
print(df_clean[["Order Date", "Ship Date"]].isnull().sum())

print("\n--- CLEANED DATA PREVIEW ---")
print(df_clean.head())

print("\nOriginal rows:", len(df))
print("Working copy rows:", len(df_clean))




total_sales = df_clean["Sales"].sum()
total_profit = df_clean["Profit"].sum()
unique_orders = df_clean["Order ID"].nunique()

profit_margin = (total_profit / total_sales) * 100

print("\n--- BUSINESS KPI SUMMARY ---")
print(f"Total Sales: ${total_sales:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Unique Orders: {unique_orders:,}")
print(f"Profit Margin: {profit_margin:.2f}%")



category_summary = (
    df_clean.groupby("Category")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Units_Sold=("Quantity", "sum")
    )
    .round(2)
    .sort_values("Total_Sales", ascending=False)
)

print("\n--- CATEGORY PERFORMANCE ---")
print(category_summary)



import matplotlib.pyplot as plt

'''# Calculate total sales for each category
category_sales = df_clean.groupby("Category")["Sales"].sum()

# Sort sales from highest to lowest
category_sales = category_sales.sort_values(ascending=False)

# Create the bar chart
plt.figure(figsize=(9, 5))
category_sales.plot(kind="bar")

# Add chart labels and title
plt.title("Total Sales by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Total Sales ($)")
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()
'''



'''category_profit = (
    df_clean.groupby("Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- PROFIT BY CATEGORY ---")
print(category_profit.round(2))

# Visualize category-wise profit
plt.figure(figsize=(9, 5))
category_profit.plot(kind="bar")

plt.title("Total Profit by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Total Profit ($)")
plt.xticks(rotation=0)
plt.axhline(y=0, linewidth=1)
plt.tight_layout()

# Save chart for our project
plt.savefig("profit_by_category.png", dpi=300, bbox_inches="tight")
plt.show()'''


region_summary = (
    df_clean.groupby("Region")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Orders=("Order ID", "nunique")
    )
    .round(2)
    .sort_values("Total_Sales", ascending=False)
)

print("\n--- REGIONAL PERFORMANCE ---")
print(region_summary)

# Plot regional sales and profit
region_summary[["Total_Sales", "Total_Profit"]].plot(
    kind="bar",
    figsize=(10, 6)
)

plt.title("Regional Sales vs Profit")
plt.xlabel("Region")
plt.ylabel("Amount ($)")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("regional_sales_profit.png", dpi=300, bbox_inches="tight")
plt.show()



# Extract year and month from Order Date
df_clean["Year_Month"] = (
    df_clean["Order Date"].dt.to_period("M")
)

# Calculate monthly sales and profit
monthly_summary = (
    df_clean.groupby("Year_Month")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum")
    )
    .sort_index()
)

print("\n--- MONTHLY SALES AND PROFIT ---")
print(monthly_summary.round(2))

# Plot monthly sales trend
plt.figure(figsize=(12, 6))
monthly_summary["Total_Sales"].plot(kind="line", marker="o")

plt.title("Monthly Sales Trend")
plt.xlabel("Year and Month")
plt.ylabel("Total Sales ($)")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig("monthly_sales_trend.png", dpi=300, bbox_inches="tight")
plt.show()



product_summary = (
    df_clean.groupby("Product Name")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Units_Sold=("Quantity", "sum")
    )
    .sort_values("Total_Sales", ascending=False)
    .head(10)
)

print("\n--- TOP 10 PRODUCTS BY SALES ---")
print(product_summary.round(2))

# Visualize the top 10 products
plt.figure(figsize=(12, 7))
product_summary["Total_Sales"].sort_values().plot(kind="barh")

plt.title("Top 10 Products by Total Sales")
plt.xlabel("Total Sales ($)")
plt.ylabel("Product Name")
plt.tight_layout()

plt.savefig("top_10_products.png", dpi=300, bbox_inches="tight")
plt.show()


# STEP 12: DISCOUNT VS PROFIT ANALYSIS

# Summarize sales and profit by discount level
discount_summary = (
    df_clean.groupby("Discount")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Orders=("Order ID", "nunique")
    )
    .sort_index()
)

print("\n--- DISCOUNT VS PROFIT ---")
print(discount_summary.round(2))

# Plot discount against average profit per row
avg_profit_by_discount = df_clean.groupby("Discount")["Profit"].mean()

plt.figure(figsize=(10, 5))
avg_profit_by_discount.plot(kind="bar")

plt.title("Average Profit by Discount Level")
plt.xlabel("Discount")
plt.ylabel("Average Profit ($)")
plt.xticks(rotation=0)
plt.axhline(y=0, linewidth=1)
plt.tight_layout()

plt.savefig("discount_vs_profit.png", dpi=300, bbox_inches="tight")
plt.show()
 


customer_summary = (
    df_clean.groupby("Customer Name")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Orders=("Order ID", "nunique")
    )
    .sort_values("Total_Sales", ascending=False)
    .head(10)
)

print("\n--- TOP 10 CUSTOMERS ---")
print(customer_summary.round(2))

# Create a horizontal bar chart
plt.figure(figsize=(10, 6))
customer_summary["Total_Sales"].sort_values().plot(kind="barh")

plt.title("Top 10 Customers by Sales")
plt.xlabel("Total Sales ($)")
plt.ylabel("Customer Name")
plt.tight_layout()

plt.savefig("top_10_customers.png", dpi=300, bbox_inches="tight")
plt.show()


# STEP 14: BUSINESS INSIGHTS REPORT

# Calculate key business metrics
total_sales = df_clean["Sales"].sum()
total_profit = df_clean["Profit"].sum()
total_orders = df_clean["Order ID"].nunique()
profit_margin = (total_profit / total_sales) * 100

# Identify the leading category and region
category_sales = df_clean.groupby("Category")["Sales"].sum()
region_sales = df_clean.groupby("Region")["Sales"].sum()
region_profit = df_clean.groupby("Region")["Profit"].sum()

best_category = category_sales.idxmax()
best_region_sales = region_sales.idxmax()
best_region_profit = region_profit.idxmax()

# Create report text
report = f"""
INDIAN BUSINESS EDA - BUSINESS INSIGHTS REPORT
==============================================

DATASET: Sample Superstore

1. OVERALL PERFORMANCE
Total Sales: ${total_sales:,.2f}
Total Profit: ${total_profit:,.2f}
Unique Orders: {total_orders:,}
Overall Profit Margin: {profit_margin:.2f}%

2. CATEGORY INSIGHT
Highest-sales category: {best_category}

3. REGIONAL INSIGHTS
Highest-sales region: {best_region_sales}
Highest-profit region: {best_region_profit}

4. DATA QUALITY
Number of rows: {len(df_clean):,}
Number of columns: {len(df_clean.columns):,}
Missing Order Dates: {df_clean["Order Date"].isnull().sum()}
Missing Ship Dates: {df_clean["Ship Date"].isnull().sum()}

NOTE:
These findings describe the Sample Superstore dataset.
They should not be interpreted as findings about the entire
Indian business market.
"""

# Display report
print(report)

# Save report as a text file
with open("business_insights_report.txt", "w", encoding="utf-8") as file:
    file.write(report)

print("Report saved successfully!")


