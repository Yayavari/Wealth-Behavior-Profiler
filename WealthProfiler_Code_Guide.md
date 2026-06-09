# 💰 Wealth Behavior Profiler — Code Reference Guide
### Plain English explanations of every code block

---

> **How to use this:** Every time we write a new block of code in the project, its explanation gets added here. Before any interview, read through this and you'll be able to walk anyone through the entire project confidently.

---

## 📦 BLOCK 1 — Importing Libraries

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
print("All libraries loaded!")
```

### What it does in plain English:
Think of this like opening your toolbox before starting work.
- **pandas** — lets you work with data like a spreadsheet (rows, columns, filters)
- **numpy** — does math behind the scenes (averages, calculations)
- **matplotlib** — draws basic charts and graphs
- **seaborn** — draws prettier, more advanced charts
- **sklearn KMeans** — the machine learning tool we'll use to group spending behaviors
- **print** — just confirms everything loaded without errors

### Why we did it:
Python doesn't automatically know you want to use these tools. You have to explicitly "import" them at the start of every project.

---

## 📂 BLOCK 2 — Loading the Dataset

```python
budget = pd.read_csv("Budget.csv")
transactions = pd.read_csv("personal_transactions.csv")

print("Budget shape:", budget.shape)
print("Transactions shape:", transactions.shape)
```

### What it does in plain English:
- **pd.read_csv** — opens a CSV file and loads it into Python as a table
- **budget** — stores the budget data (19 rows, 2 columns)
- **transactions** — stores all spending records (806 rows, 6 columns)
- **.shape** — tells you how many rows and columns are in each table

### What we found:
- Budget table: 19 categories with their planned budgets
- Transactions table: 806 individual spending records over 21 months

### Why we did it:
Before doing any analysis, you need to load your data into Python so you can work with it.

---

## 👀 BLOCK 3 — Peeking at the Data

```python
print("=== BUDGET ===")
print(budget.head())

print("\n=== TRANSACTIONS ===")
print(transactions.head())

print("=== BUDGET COLUMNS ===")
print(budget.dtypes)

print("\n=== TRANSACTIONS COLUMNS ===")
print(transactions.dtypes)
```

### What it does in plain English:
- **.head()** — shows the first 5 rows of the table, like previewing a spreadsheet
- **.dtypes** — tells you what type of data is in each column (number, text, date, etc.)

### What we found:
- Transactions has: Date, Description, Amount, Transaction Type, Category, Account Name
- Budget has: Category, Budget amount
- Dates were stored as text (str) — we later converted them to proper date format

### Why we did it:
A good analyst always looks at the raw data first before touching it. You need to know what you're working with before you can analyze it.

---

## 🔍 BLOCK 4 — Checking Data Quality

```python
print("=== MISSING VALUES ===")
print("Budget:\n", budget.isnull().sum())
print("\nTransactions:\n", transactions.isnull().sum())

transactions['Date'] = pd.to_datetime(transactions['Date'])
print("\nEarliest date:", transactions['Date'].min())
print("Latest date:", transactions['Date'].max())

print("\nTransaction Categories:\n", transactions['Category'].unique())
```

### What it does in plain English:
- **.isnull().sum()** — counts how many empty/blank values exist in each column
- **pd.to_datetime()** — converts the Date column from plain text into a proper date format Python can understand
- **.min() / .max()** — finds the earliest and latest dates
- **.unique()** — lists every unique category name that exists in the data

### What we found:
- Zero missing values in both tables — perfectly clean data
- Data covers 21 months: January 2018 to September 2019
- 22 unique spending categories exist

### Why we did it:
Missing or broken data will cause wrong analysis. Checking data quality is always Step 1 of any real analyst project.

---

## 📊 BLOCK 5 — Budget vs Actual Spending Analysis

```python
spending = transactions[transactions['Transaction Type'] == 'debit']

actual_spending = spending.groupby('Category')['Amount'].sum().reset_index()
actual_spending.columns = ['Category', 'Total Spent']

comparison = pd.merge(actual_spending, budget, on='Category', how='left')
comparison['Budget'] = comparison['Budget'].fillna(0)
comparison = comparison.sort_values('Total Spent', ascending=False)
```

### What it does in plain English:
- **transactions[...== 'debit']** — filters to keep only spending rows (removes income/credits)
- **.groupby('Category')** — groups all transactions by their category (like a pivot table in Excel)
- **['Amount'].sum()** — adds up all amounts within each category
- **pd.merge()** — joins the spending table with the budget table on the Category column (like VLOOKUP in Excel)
- **.fillna(0)** — replaces any blank budget values with 0
- **.sort_values()** — sorts the table from highest to lowest spending

### What we found:
- 16 out of 17 categories were over budget
- Total spent: $96,083 over 21 months (~$4,575/month)
- Biggest overspend: Home Improvement ($250 budget vs $19,092 spent)

### Why we did it:
Comparing planned vs actual spending is the core of any financial analysis. This tells us where the money is really going.

---

## 📈 BLOCK 6 — Budget vs Actual Chart (All Categories)

```python
fig, ax = plt.subplots(figsize=(14, 6))

bars1 = ax.bar([i - width/2 for i in x], comparison_filtered['Budget'], 
               width, label='Budget', color='steelblue')
bars2 = ax.bar([i + width/2 for i in x], comparison_filtered['Total Spent'], 
               width, label='Total Spent', color='coral')

ax.set_title('Budget vs Actual Spending by Category')
plt.savefig('budget_vs_actual.png')
plt.show()
```

### What it does in plain English:
- **plt.subplots()** — creates a blank chart canvas
- **ax.bar()** — draws a bar chart; we draw two sets of bars side by side (budget in blue, actual in orange)
- **figsize=(14,6)** — sets the chart size (width=14, height=6 inches)
- **rotation=45** — tilts the category labels so they don't overlap
- **plt.savefig()** — saves the chart as a PNG image file
- **plt.show()** — displays the chart on screen

### What we found visually:
Mortgage and Home Improvement towers dwarfed every other category, making it hard to see smaller categories.

### Why we did it:
Charts communicate insights faster than numbers. A business stakeholder can understand a bar chart in seconds vs reading a table for minutes.

---

## 📉 BLOCK 7 — Budget vs Actual Chart (Excluding Housing)

```python
comparison_small = comparison_filtered[
    ~comparison_filtered['Category'].isin(['Mortgage & Rent', 'Home Improvement'])
].copy()
```

### What it does in plain English:
- **~** — means "NOT" (exclude these categories)
- **.isin([...])** — checks if a value is in a given list
- **.copy()** — creates a fresh copy so we don't accidentally change the original data

### Why we did it:
Mortgage and Home Improvement were so large they made all other categories look flat. Removing them revealed clear overspending patterns in lifestyle categories like Groceries, Restaurants, and Alcohol.

---

## 🔑 BLOCK 8 — Key Insights Summary

```python
print(f"Total spent overall: ${spending['Amount'].sum():,.2f}")
print(f"Total transactions: {len(transactions)}")
overspent = comparison_filtered[comparison_filtered['Total Spent'] > comparison_filtered['Budget']]
print(f"Categories over budget: {len(overspent)} out of {len(comparison_filtered)}")
```

### What it does in plain English:
- **f"..."** — f-string: lets you insert variable values directly inside text
- **:,.2f** — formatting: adds commas and shows 2 decimal places (e.g. $96,083.78)
- **len()** — counts how many rows are in a table
- The last line filters only rows where actual spending exceeded the budget, then counts them

### What we found:
- $96,083.78 total spent
- 806 total transactions
- 16 out of 17 categories over budget

### Why we did it:
Summary statistics turn raw data into a story. These 3 numbers alone tell a powerful narrative about this person's financial behavior.

---

## 📅 BLOCK 9 — Monthly Spending Trend

```python
spending['Month'] = spending['Date'].dt.to_period('M')
monthly_spending = spending.groupby('Month')['Amount'].sum().reset_index()
monthly_spending['Month'] = monthly_spending['Month'].astype(str)
```

### What it does in plain English:
- **.dt.to_period('M')** — extracts just the year and month from a full date (e.g. 2018-01-15 becomes 2018-01)
- **.groupby('Month')** — groups all transactions by month
- **['Amount'].sum()** — adds up all spending within each month
- **.astype(str)** — converts the month format to plain text so it displays nicely on charts

### What we found:
- Highest spending month: June 2019 — $11,999
- Lowest spending month: August 2018 — $2,396
- Two clear spike months suggesting large one-off purchases

### Why we did it:
Monthly trends reveal behavioral patterns over time — whether someone is consistently overspending or has occasional large purchases. This is a key input for clustering.

---

## 🏷️ BLOCK 10 — Building Features for Clustering

```python
monthly_features = spending.groupby('Month').agg(
    total_spent=('Amount', 'sum'),
    transaction_count=('Amount', 'count'),
    avg_transaction=('Amount', 'mean'),
    max_transaction=('Amount', 'max'),
    unique_categories=('Category', 'nunique')
).reset_index()
```

### What it does in plain English:
- **.agg()** — aggregates (summarizes) multiple calculations at once for each month
- **total_spent** — total money spent that month
- **transaction_count** — how many purchases were made
- **avg_transaction** — average purchase size
- **max_transaction** — the single biggest purchase that month
- **unique_categories** — how many different spending categories were used
- **.reset_index()** — converts the grouped result back into a regular table

### Why we did it:
K-Means needs numbers to work with — it can't cluster raw transactions. We summarized each month into 5 key behavioral metrics. Think of it like creating a "monthly report card" for the spending data.

---

## ⚖️ BLOCK 11 — Normalizing Data with StandardScaler

```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

### What it does in plain English:
- **StandardScaler** — rescales all numbers so they're on the same scale
- Without this, total_spent ($11,000) would completely overpower transaction_count (35) just because the numbers are bigger
- After scaling, every feature gets equal importance in the clustering
- Think of it like converting miles and kilometers to the same unit before comparing distances

### Why we did it:
K-Means measures distance between data points. If one feature has much larger numbers than others, it will dominate the clustering unfairly. Scaling levels the playing field.

---

## 📐 BLOCK 12 — Elbow Method (Finding Best K)

```python
inertia = []
for k in range(2, 8):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)
```

### What it does in plain English:
- **inertia** — measures how tightly grouped the clusters are (lower = better)
- We test K=2 through K=7 and record the inertia for each
- **random_state=42** — sets a fixed starting point so results are reproducible every time
- We then plot these values and look for the "elbow" — the point where improvement slows down

### What we found:
- The elbow was clearly at K=3 — adding more clusters after 3 gave diminishing returns
- This means 3 spending personas is the optimal number for this dataset

### Why we did it:
K-Means requires you to tell it how many clusters to create. The elbow method is the standard analyst technique to find that number objectively rather than guessing.

---

## 🧠 BLOCK 13 — Running K-Means Clustering

```python
kmeans = KMeans(n_clusters=3, random_state=42)
monthly_features['Cluster'] = kmeans.fit_predict(X_scaled)
```

### What it does in plain English:
- **KMeans(n_clusters=3)** — creates a K-Means model that will find 3 groups
- **.fit_predict()** — trains the model AND assigns each month to a cluster in one step
- The result is a new column called 'Cluster' with values 0, 1, or 2 for each month
- K-Means works by placing 3 center points, assigning each month to its nearest center, then moving centers until they stabilize

### What we found:
- Cluster 2: 2 months (May 2018, Jun 2019) — massive spending spikes
- Cluster 0: 6 months — lower transaction counts, mixed spending
- Cluster 1: 13 months — the majority, steady everyday spending

### Why we did it:
Clustering groups similar months together automatically without us manually defining rules. It lets the data tell us the natural patterns rather than us imposing them.

---

## 🎭 BLOCK 14 — Naming the Personas

```python
persona_map = {
    2: 'High Spender 🚨',
    1: 'Steady Spender 📊',
    0: 'Cautious Spender 😴'
}
monthly_features['Persona'] = monthly_features['Cluster'].map(persona_map)
```

### What it does in plain English:
- **persona_map** — a dictionary that translates cluster numbers (0, 1, 2) into human-readable names
- **.map()** — replaces each cluster number with its corresponding persona name
- We chose names based on what the data showed: Cluster 2 had the highest spending, Cluster 1 was average, Cluster 0 was most conservative

### Why we did it:
Numbers like "Cluster 0" mean nothing to a business stakeholder. Naming clusters turns a technical ML output into a business-friendly insight that anyone can understand and act on.

---

## 💯 BLOCK 15 — Financial Health Score

```python
def health_score(row):
    score = 100
    if row['total_spent'] > 5000:
        score -= 30
    elif row['total_spent'] > 3500:
        score -= 15
    if row['max_transaction'] > 5000:
        score -= 25
    elif row['max_transaction'] > 2000:
        score -= 10
    if 25 <= row['transaction_count'] <= 35:
        score += 10
    if row['unique_categories'] >= 15:
        score += 5
    return max(0, min(100, score))

monthly_features['Health Score'] = monthly_features.apply(health_score, axis=1)
```

### What it does in plain English:
- **def health_score(row)** — creates a custom function that takes one month's data and returns a score
- We start at 100 and add/subtract points based on spending behavior rules
- **score -= 30** — penalizes months with very high total spending
- **score += 10** — rewards months with a healthy number of transactions (not too many, not too few)
- **max(0, min(100, score))** — makes sure the score never goes below 0 or above 100
- **.apply(health_score, axis=1)** — runs this function on every row (every month) automatically

### What we found:
- 19 out of 21 months scored above 70 (the health threshold)
- Only May 2018 and Jun 2019 scored 60 — the two High Spender months
- Overall this person is financially healthy with occasional large purchase spikes

### Why we did it:
This is the most unique part of the project. Turning raw cluster data into an actionable score is what separates an analyst from someone who just runs code. It's a business deliverable — something a financial advisor could actually show a client.

---

*// Streamlit Dashboard blocks will be added next //*
