# ai.py
from textblob import TextBlob
import random
import json

# Analizador de sentimiento
def analyze_sentiment(message):
    analysis = TextBlob(message)
    polarity = analysis.sentiment.polarity
    if polarity > 0.1:
        return "positivo"
    elif polarity < -0.1:
        return "negativo"
    else:
        return "neutral"

# Predicción de cierre de lead (mock)
def predict_lead_closure(lead_data):
    # Aquí puedes reemplazar por un modelo real entrenado
    probability = round(random.uniform(0, 1), 2)
    return probability

# Recomendaciones de upsell/cross-sell (mock)
def recommend_upsell(customer_data):
    # Lista de productos ficticios
    products = ["Producto A", "Producto B", "Producto C", "Producto D"]
    recommendations = random.sample(products, 2)
    return recommendations

# Para probar localmente
if __name__ == "__main__":
    msg = "El cliente está muy satisfecho con el servicio"
    print("Sentiment:", analyze_sentiment(msg))
    print("Lead probability:", predict_lead_closure({}))
    print("Recommendations:", recommend_upsell({}))
