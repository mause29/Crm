import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Predicción de cierre de oportunidades
def predict_opportunity_success(dataframe):
    X = dataframe.drop(['closed'], axis=1)
    y = dataframe['closed']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    return predictions, model

# Segmentación automática de clientes
def segment_customers(dataframe):
    conditions = [
        (dataframe['revenue'] > 10000),
        (dataframe['revenue'] <= 10000) & (dataframe['revenue'] > 5000),
        (dataframe['revenue'] <= 5000)
    ]
    categories = ['VIP', 'Medium', 'Low']
    dataframe['segment'] = pd.cut(dataframe['revenue'], bins=[0, 5000, 10000, float('inf')], labels=['Low', 'Medium', 'VIP'])
    return dataframe
