import pandas as pd

def cashflow_forecast(df):
    df['net'] = df['income'] - df['expenses']
    forecast = df['net'].cumsum()
    return forecast

def budget_analysis(df, budget):
    df['variance'] = df['amount'] - budget
    return df
