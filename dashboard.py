import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Wealth Behavior Profiler", layout="wide")

@st.cache_data
def load_data():
    transactions = pd.read_csv("personal_transactions.csv")
    budget = pd.read_csv("Budget.csv")
    transactions['Date'] = pd.to_datetime(transactions['Date'])
    return transactions, budget

transactions, budget = load_data()

spending = transactions[transactions['Transaction Type'] == 'debit']
spending = spending.copy()
spending['Month'] = spending['Date'].dt.to_period('M')

actual_spending = spending.groupby('Category')['Amount'].sum().reset_index()
actual_spending.columns = ['Category', 'Total Spent']
comparison = pd.merge(actual_spending, budget, on='Category', how='left')
comparison['Budget'] = comparison['Budget'].fillna(0)
comparison = comparison.sort_values('Total Spent', ascending=False)

monthly_features = spending.groupby('Month').agg(
    total_spent=('Amount', 'sum'),
    transaction_count=('Amount', 'count'),
    avg_transaction=('Amount', 'mean'),
    max_transaction=('Amount', 'max'),
    unique_categories=('Category', 'nunique')
).reset_index()
monthly_features['Month'] = monthly_features['Month'].astype(str)

features = ['total_spent', 'transaction_count', 'avg_transaction',
            'max_transaction', 'unique_categories']
X = monthly_features[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
kmeans = KMeans(n_clusters=3, random_state=42)
monthly_features['Cluster'] = kmeans.fit_predict(X_scaled)
persona_map = {2: 'High Spender 🚨', 1: 'Steady Spender 📊', 0: 'Cautious Spender 😴'}
monthly_features['Persona'] = monthly_features['Cluster'].map(persona_map)

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

st.title("💰 Personal Wealth Behavior Profiler")
st.markdown("*Behavioral analysis of personal spending patterns using K-Means clustering*")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Spent", f"${spending['Amount'].sum():,.0f}")
col2.metric("Total Transactions", len(spending))
col3.metric("Months Analyzed", len(monthly_features))
col4.metric("Avg Monthly Spend", f"${spending['Amount'].sum()/len(monthly_features):,.0f}")

st.markdown("---")

st.subheader("🎭 Spending Personas")
persona_summary = monthly_features.groupby('Persona').agg(
    Months=('Month', 'count'),
    Avg_Monthly_Spend=('total_spent', 'mean'),
    Avg_Health_Score=('Health Score', 'mean')
).round(2).reset_index()
persona_summary.columns = ['Persona', 'Months', 'Avg Monthly Spend ($)', 'Avg Health Score']
st.dataframe(persona_summary, use_container_width=True)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Budget vs Actual Spending")
    comparison_filtered = comparison[comparison['Budget'] > 0]
    comparison_small = comparison_filtered[
        ~comparison_filtered['Category'].isin(['Mortgage & Rent', 'Home Improvement'])
    ].copy()
    fig, ax = plt.subplots(figsize=(8, 5))
    x = range(len(comparison_small))
    width = 0.35
    ax.bar([i - width/2 for i in x], comparison_small['Budget'],
           width, label='Budget', color='steelblue')
    ax.bar([i + width/2 for i in x], comparison_small['Total Spent'],
           width, label='Total Spent', color='coral')
    ax.set_xticks(list(x))
    ax.set_xticklabels(comparison_small['Category'], rotation=45, ha='right', fontsize=8)
    ax.legend()
    ax.set_title('Budget vs Actual (Excl. Housing)')
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("📈 Monthly Spending Trend")
    monthly_spending = spending.groupby('Month')['Amount'].sum().reset_index()
    monthly_spending['Month'] = monthly_spending['Month'].astype(str)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(monthly_spending['Month'], monthly_spending['Amount'],
            marker='o', color='coral', linewidth=2)
    ax.fill_between(range(len(monthly_spending)), monthly_spending['Amount'],
                    alpha=0.3, color='coral')
    ax.set_xticks(range(len(monthly_spending)))
    ax.set_xticklabels(monthly_spending['Month'], rotation=45, ha='right', fontsize=8)
    ax.set_title('Monthly Spending (2018-2019)')
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    st.pyplot(fig)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🧠 Spending Personas — K-Means Clusters")
    colors = {'High Spender 🚨': 'red',
              'Steady Spender 📊': 'steelblue',
              'Cautious Spender 😴': 'green'}
    fig, ax = plt.subplots(figsize=(8, 5))
    for persona, group in monthly_features.groupby('Persona'):
        ax.scatter(group['transaction_count'], group['total_spent'],
                   label=persona, color=colors[persona], s=100)
        for _, row in group.iterrows():
            ax.annotate(row['Month'], (row['transaction_count'], row['total_spent']),
                       textcoords="offset points", xytext=(5, 5), fontsize=7)
    ax.set_xlabel('Number of Transactions')
    ax.set_ylabel('Total Spent ($)')
    ax.set_title('Spending Personas Cluster Map')
    ax.legend()
    ax.grid(linestyle='--', alpha=0.5)
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("💯 Monthly Financial Health Score")
    colors_score = monthly_features['Persona'].map({
        'High Spender 🚨': 'red',
        'Steady Spender 📊': 'steelblue',
        'Cautious Spender 😴': 'green'
    })
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(monthly_features['Month'], monthly_features['Health Score'],
           color=colors_score, edgecolor='white')
    ax.axhline(y=70, color='orange', linestyle='--', linewidth=1.5, label='Health Threshold (70)')
    ax.set_xticklabels(monthly_features['Month'], rotation=45, ha='right', fontsize=8)
    ax.set_title('Financial Health Score by Month')
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)

st.markdown("---")

st.subheader("📋 Monthly Breakdown")
display_df = monthly_features[['Month', 'Persona', 'total_spent',
                                'transaction_count', 'Health Score']].copy()
display_df.columns = ['Month', 'Persona', 'Total Spent ($)', 'Transactions', 'Health Score']
display_df['Total Spent ($)'] = display_df['Total Spent ($)'].round(2)
st.dataframe(display_df, use_container_width=True)

st.markdown("---")
st.caption("Built by Yayavari R | Personal Wealth Behavior Profiler | Python · Pandas · Scikit-learn · Streamlit")