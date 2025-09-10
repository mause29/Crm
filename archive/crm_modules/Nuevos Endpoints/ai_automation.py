import random
from datetime import datetime, timedelta

# Ruteo inteligente de leads
def route_lead(lead_data):
    """
    Asigna automáticamente el lead al agente más adecuado según reglas básicas.
    - Puede expandirse con ML para priorizar leads más probables de cerrar.
    """
    agents = ["Agente A", "Agente B", "Agente C", "Agente D"]
    # Ejemplo: ruteo por región o tipo de lead
    region = lead_data.get("region", "general")
    assigned_agent = random.choice(agents)
    return assigned_agent

# Generación de alertas inteligentes
def generate_alerts(data_stream):
    """
    Analiza el flujo de datos y genera alertas si se detectan patrones:
    - Clientes inactivos
    - Leads con alta probabilidad de perder
    - Tendencias de ventas inusuales
    """
    alerts = []
    for record in data_stream:
        # Ejemplo de alerta simple
        if record.get("days_since_last_contact", 0) > 30:
            alerts.append({
                "type": "inactividad_cliente",
                "message": f"Cliente {record['client_id']} no ha sido contactado en más de 30 días",
                "date": datetime.now().isoformat()
            })
        if record.get("lead_probability", 1) < 0.2:
            alerts.append({
                "type": "lead_bajo_rendimiento",
                "message": f"Lead {record['lead_id']} tiene baja probabilidad de cierre",
                "date": datetime.now().isoformat()
            })
        # Tendencias de ventas
        if record.get("sales_today", 0) > record.get("average_sales", 100):
            alerts.append({
                "type": "alta_venta",
                "message": f"Ventas inusualmente altas hoy: {record['sales_today']}",
                "date": datetime.now().isoformat()
            })
    return alerts

# Para pruebas locales
if __name__ == "__main__":
    lead = {"region": "norte"}
    print("Assigned Agent:", route_lead(lead))
    data_stream = [
        {"client_id": 1, "days_since_last_contact": 45, "lead_probability": 0.1, "sales_today": 200, "average_sales": 100},
        {"client_id": 2, "days_since_last_contact": 10, "lead_probability": 0.9, "sales_today": 50, "average_sales": 100},
    ]
    print("Alerts:", generate_alerts(data_stream))
