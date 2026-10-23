
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
