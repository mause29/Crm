import sys, json
from ai_automation import route_lead, generate_alerts

args = sys.argv[1:]

# Determinar si es ruteo o alertas
data = json.loads(args[0])
if isinstance(data, list):
    # Generar alertas
    result = {"alerts": generate_alerts(data)}
else:
    # Ruteo de lead
    result = {"assignedAgent": route_lead(data)}

print(json.dumps(result))
