
import pandas as pd
import matplotlib.pyplot as plt

# Load the original dataset
df = pd.read_excel("data/Online Retail.xlsx")

print("Original dataset shape:", df.shape)

# Remove duplicate rows
df = df.drop_duplicates()

# Remove rows without a product description
df = df.dropna(subset=["Description"])

# Keep positive quantities and prices
# This excludes returns and invalid price records from this sales analysis
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

# Calculate revenue for each line item
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

print("\n========== CLEANING RESULTS ==========")
print("Cleaned dataset shape:", df.shape)
print("Missing values after cleaning:")
print(df.isnull().sum())

print("\n========== SALES SUMMARY ==========")
print("Total revenue:", round(df["Revenue"].sum(), 2))
print("Total units sold:", df["Quantity"].sum())
print("Unique invoices:", df["InvoiceNo"].nunique())
print("Unique products:", df["StockCode"].nunique())
print("Countries:", df["Country"].nunique())

# Save the cleaned dataset
df.to_csv("data/cleaned_retail_sales.csv", index=False)

print("\nCleaned dataset saved successfully!")


# Monthly sales analysis
df["Month"] = df["InvoiceDate"].dt.to_period("M")

monthly_sales = df.groupby("Month")["Revenue"].sum()

print("\n========== MONTHLY SALES ==========")
print(monthly_sales.round(2))

# Create the chart
plt.figure(figsize=(12, 6))

monthly_sales.index = monthly_sales.index.astype(str)

plt.plot(
    monthly_sales.index,
    monthly_sales.values,
    marker="o"
)

plt.title("Monthly Retail Sales Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue (£)")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("monthly_sales.png", dpi=300)
plt.show()

print("\nMonthly sales chart saved as monthly_sales.png")


# Top 10 products by revenue
top_products = (
    df.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== TOP 10 PRODUCTS BY REVENUE ==========")
print(top_products.round(2))

plt.figure(figsize=(12, 7))
top_products.sort_values().plot(kind="barh")

plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue (£)")
plt.ylabel("Product")

plt.tight_layout()
plt.savefig("top_10_products.png", dpi=300)
plt.show()

print("\nTop products chart saved as top_10_products.png")


# Top 10 countries by revenue
country_sales = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== TOP 10 COUNTRIES BY REVENUE ==========")
print(country_sales.round(2))

# Create a bar chart
plt.figure(figsize=(12, 7))

country_sales.sort_values().plot(kind="barh")

plt.title("Top 10 Countries by Revenue")
plt.xlabel("Revenue (£)")
plt.ylabel("Country")

plt.tight_layout()
plt.savefig("top_10_countries.png", dpi=300)
plt.show()

print("\nCountry sales chart saved as top_10_countries.png")


# Business Insights
print("\n========== BUSINESS INSIGHTS ==========")

# Best month by revenue
best_month = monthly_sales.idxmax()
best_month_revenue = monthly_sales.max()

print(f"\nBest sales month: {best_month}")
print(f"Revenue: £{best_month_revenue:,.2f}")

# Lowest month by revenue
lowest_month = monthly_sales.idxmin()
lowest_month_revenue = monthly_sales.min()

print(f"\nLowest sales month: {lowest_month}")
print(f"Revenue: £{lowest_month_revenue:,.2f}")

# Highest revenue country
best_country = country_sales.idxmax()
best_country_revenue = country_sales.max()

print(f"\nTop country: {best_country}")
print(f"Revenue: £{best_country_revenue:,.2f}")

# Top country's revenue contribution
total_revenue = df["Revenue"].sum()
country_percentage = (best_country_revenue / total_revenue) * 100

print(f"\nTop country's share of total revenue: {country_percentage:.2f}%")


# Day-of-Week Sales Analysis
df["DayOfWeek"] = df["InvoiceDate"].dt.day_name()

daily_sales = (
    df.groupby("DayOfWeek")["Revenue"]
    .sum()
    .reindex([
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ])
)

daily_sales = daily_sales.dropna()

print("\n========== SALES BY DAY OF WEEK ==========")
print(daily_sales.round(2))
print("\nNote: No Saturday transactions were found in the cleaned dataset.")

# Find the day with the highest revenue
best_day = daily_sales.idxmax()
best_day_revenue = daily_sales.max()

print(f"\nBest sales day: {best_day}")
print(f"Revenue: £{best_day_revenue:,.2f}")

# Create a bar chart
plt.figure(figsize=(10, 6))
daily_sales.plot(kind="bar")

plt.title("Total Retail Sales by Day of the Week")
plt.xlabel("Day of the Week")
plt.ylabel("Revenue (£)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("sales_by_day_of_week.png", dpi=300)
plt.show()

print("\nDay-of-week sales chart saved as sales_by_day_of_week.png")


# Customer Analysis
print("\n========== CUSTOMER ANALYSIS ==========")

# Keep records with a known customer ID
customer_df = df.dropna(subset=["CustomerID"]).copy()

# Calculate total revenue generated by each customer
customer_sales = (
    customer_df.groupby("CustomerID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\nNumber of customers with known IDs:",
      customer_df["CustomerID"].nunique())

print("\n========== TOP 10 CUSTOMERS BY REVENUE ==========")
print(customer_sales.head(10).round(2))

# Plot the top 10 customers
top_customers = customer_sales.head(10).sort_values()

plt.figure(figsize=(10, 6))
top_customers.plot(kind="barh")

plt.title("Top 10 Customers by Revenue")
plt.xlabel("Revenue (£)")
plt.ylabel("Customer ID")
plt.tight_layout()
plt.savefig("top_10_customers.png", dpi=300)
plt.show()

print("\nCustomer chart saved as top_10_customers.png")

# Identify repeat customers
invoice_counts = (
    customer_df.groupby("CustomerID")["InvoiceNo"]
    .nunique()
)

repeat_customers = invoice_counts[invoice_counts > 1]

print("\n========== REPEAT CUSTOMER ANALYSIS ==========")
print("Customers with known IDs:",
      len(invoice_counts))
print("Repeat customers:",
      len(repeat_customers))

repeat_percentage = (
    len(repeat_customers) / len(invoice_counts) * 100
    if len(invoice_counts) > 0 else 0
)

print(f"Repeat customers (%): {repeat_percentage:.2f}%")


# Monthly Sales Growth Analysis
print("\n========== MONTHLY SALES GROWTH ==========")

monthly_growth = monthly_sales.pct_change() * 100

print("\nMonthly revenue growth (%):")
print(monthly_growth.round(2))

plt.figure(figsize=(12, 6))
monthly_growth.plot(kind="line", marker="o")
plt.title("Monthly Sales Growth Rate")
plt.xlabel("Month")
plt.ylabel("Revenue Growth (%)")
plt.axhline(y=0, linestyle="--")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("monthly_sales_growth.png", dpi=300)
plt.show()

print("\nMonthly sales growth chart saved as monthly_sales_growth.png")


# Customer Segmentation Using RFM Analysis
print("\n========== CUSTOMER SEGMENTATION (RFM) ==========")

rfm_df = df.dropna(subset=["CustomerID"]).copy()

rfm_df["InvoiceDate"] = pd.to_datetime(rfm_df["InvoiceDate"])

reference_date = rfm_df["InvoiceDate"].max() + pd.Timedelta(days=1)

rfm = rfm_df.groupby("CustomerID").agg(
    Recency=("InvoiceDate", lambda dates: (reference_date - dates.max()).days),
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("Revenue", "sum")
)

rfm["CustomerSegment"] = "Regular"

rfm.loc[
    (rfm["Frequency"] >= rfm["Frequency"].quantile(0.75)) &
    (rfm["Monetary"] >= rfm["Monetary"].quantile(0.75)),
    "CustomerSegment"
] = "High Value"

rfm.loc[
    rfm["Recency"] >= rfm["Recency"].quantile(0.75),
    "CustomerSegment"
] = "Needs Attention"

print("\nCustomer segment counts:")
print(rfm["CustomerSegment"].value_counts())

print("\nSample RFM results:")
print(rfm.head(10).round(2))

rfm.to_csv("customer_segmentation.csv")

print("\nCustomer segmentation saved as customer_segmentation.csv")
