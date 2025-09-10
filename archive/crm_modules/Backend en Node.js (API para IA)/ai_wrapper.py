import sys, json
from ai import analyze_sentiment, predict_lead_closure, recommend_upsell

args = sys.argv[1:]

if len(args) == 1:
    # Analizador de sentimiento
    message = args[0]
    result = {"sentiment": analyze_sentiment(message)}
elif len(args) == 2:
    # Lead o recomendación
    data = json.loads(args[1])
    if args[0] == "lead":
        result = {"probability": predict_lead_closure(data)}
    else:
        result = {"recommendations": recommend_upsell(data)}

print(json.dumps(result))
