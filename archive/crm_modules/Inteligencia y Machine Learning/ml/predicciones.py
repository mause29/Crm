import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from crm.models import Oportunidad

def entrenar_modelo_oportunidades():
    qs = Oportunidad.objects.all().values('valor', 'dias_en_etapa', 'etapa')
    df = pd.DataFrame(qs)
    df['cerrado'] = df['etapa'].apply(lambda x: 1 if x == 'Cerrado' else 0)
    X = df[['valor', 'dias_en_etapa']]
    y = df['cerrado']
    modelo = RandomForestClassifier(n_estimators=100)
    modelo.fit(X, y)
    return modelo

def predecir_cierre(modelo, valor, dias_en_etapa):
    return modelo.predict([[valor, dias_en_etapa]])[0]
