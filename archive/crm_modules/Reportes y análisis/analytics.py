import pandas as pd

def sales_report(df):
    summary = df.groupby('month')['amount'].sum()
    return summary

def top_clients(df, n=10):
    return df.groupby('client_name')['amount'].sum().sort_values(ascending=False).head(n)

def conversion_rate(df):
    total_leads = len(df)
    converted = df[df['status'] == 'closed'].shape[0]
    return converted / total_leads if total_leads > 0 else 0
