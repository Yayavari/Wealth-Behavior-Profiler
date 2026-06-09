# 💰 Personal Wealth Behavior Profiler

> Behavioral analysis of personal spending patterns using unsupervised machine learning (K-Means Clustering)

---

## 📌 Project Overview

This project analyzes 21 months of real personal finance transaction data to uncover spending behavior patterns, classify months into financial personas, and generate a monthly financial health score.

Built as a portfolio project targeting **Data Analyst** and **Business Analyst** roles.

---

## 🎯 Key Features

- **Budget vs Actual Analysis** — identifies overspending across 17 categories
- **Monthly Trend Analysis** — tracks spending behavior over 21 months
- **K-Means Clustering** — groups months into 3 distinct spending personas
- **Financial Health Scoring** — custom scoring model (0–100) per month
- **Interactive Dashboard** — live Streamlit web app with 4 charts + data tables

---

## 🧠 Spending Personas Identified

| Persona | Months | Avg Monthly Spend | Avg Health Score |
|---|---|---|---|
| 🚨 High Spender | 2 | $11,695 | 60 |
| 📊 Steady Spender | 13 | $3,930 | 94 |
| 😴 Cautious Spender | 6 | $3,599 | 94 |

---

## 📊 Dashboard Preview

The Streamlit dashboard includes:
- KPI metrics (Total Spent, Transactions, Avg Monthly Spend)
- Budget vs Actual Spending chart
- Monthly Spending Trend line chart
- K-Means Cluster scatter plot
- Financial Health Score bar chart
- Full monthly breakdown table

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data manipulation and analysis |
| Matplotlib / Seaborn | Data visualization |
| Scikit-learn | K-Means clustering, StandardScaler |
| Streamlit | Interactive dashboard |

---

## 📁 Project Structure
wealth-behavior-profiler/
│
├── dashboard.py               # Streamlit dashboard app
├── explore.ipynb              # Data exploration notebook
├── Budget.csv                 # Budget data by category
├── personal_transactions.csv  # 806 transaction records
├── budget_vs_actual.png       # Chart export
├── monthly_trend.png          # Chart export
├── category_trends_clean.png  # Chart export
├── persona_clusters.png       # Chart export
└── health_scores.png          # Chart export

---

## 🚀 How to Run

1. Clone the repository
```bash
git clone https://github.com/Yayavari/Wealth-Behavior-Profiler.git
cd Wealth-Behavior-Profiler
```

2. Install dependencies
```bash
pip install pandas matplotlib seaborn scikit-learn streamlit
```

3. Run the dashboard
```bash
streamlit run dashboard.py
```

---

## 💡 Key Insights

- **$96,083** spent across 21 months (~$4,575/month average)
- **16 out of 17** spending categories exceeded their budget
- **Home Improvement** had the biggest overspend — $250 budgeted vs $19,092 spent
- Only **2 months** (May 2018, Jun 2019) fell below the financial health threshold
- **Steady Spender** was the dominant persona — 13 out of 21 months

---

## 👤 Author

**Yayavari R**  
Systems Engineer @ Infosys | Aspiring Data & Business Analyst  
[LinkedIn](https://www.linkedin.com/in/yayavari-r) | [GitHub](https://github.com/Yayavari)