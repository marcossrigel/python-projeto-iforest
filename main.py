import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# =========================
# 1. Conectar ao Google Sheets
# =========================
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

CAMINHO_CREDENCIAIS = r"C:\temp\py-projeto-iforest\credenciais.json"
ID_PLANILHA = "1oQgFTTb6MEdZLMJkz-Lb-93MY2DpsYz5M_Lx-Tfqi28"

creds = ServiceAccountCredentials.from_json_keyfile_name(CAMINHO_CREDENCIAIS, scope)
client = gspread.authorize(creds)

# abrir planilha pela chave
planilha = client.open_by_key(ID_PLANILHA)
sheet = planilha.sheet1

# pegar dados
dados = sheet.get_all_records()
df = pd.DataFrame(dados)

print("\nBase carregada:")
print(df.head())

# =========================
# 2. Selecionar variáveis
# =========================
features = [
    "valor_orcado",
    "valor_executado",
    "percentual_execucao",
    "atraso_dias",
    "aditivos",
    "pendencias"
]

for col in features:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=features).copy()

X = df[features]

# =========================
# 3. Padronizar os dados
# =========================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# =========================
# 4. Treinar o Isolation Forest
# =========================
modelo = IsolationForest(
    n_estimators=100,
    contamination=0.15,
    random_state=42
)

modelo.fit(X_scaled)

# =========================
# 5. Fazer predições
# =========================
df["predicao"] = modelo.predict(X_scaled)
df["score_anomalia"] = modelo.decision_function(X_scaled)
df["classificacao"] = df["predicao"].map({1: "Normal", -1: "Anomalia"})

df = df.sort_values(by="score_anomalia").reset_index(drop=True)

# =========================
# 6. Mostrar resultados
# =========================
print("\nResultado final:")
print(df[["obra", "classificacao", "score_anomalia"]])

print("\nSomente anomalias encontradas:")
print(df[df["classificacao"] == "Anomalia"][["obra", "score_anomalia"]])

# =========================
# 7. Gráfico simples
# =========================
plt.figure(figsize=(10, 6))

for i in range(len(df)):
    x = df.loc[i, "valor_orcado"]
    y = df.loc[i, "valor_executado"]
    nome = df.loc[i, "obra"]

    if df.loc[i, "classificacao"] == "Anomalia":
        plt.scatter(x, y, marker="x", s=100)
    else:
        plt.scatter(x, y, marker="o")

    plt.text(x, y, nome, fontsize=8)

plt.xlabel("Valor Orçado")
plt.ylabel("Valor Executado")
plt.title("Detecção de Anomalias em Obras com Isolation Forest")
plt.grid(True)

print("\nResumo das anomalias:")

anomalias = df[df["classificacao"] == "Anomalia"].copy()

# médias e desvios padrão
medias = df[features].mean()
desvios = df[features].std()

def interpretar_variavel(col, valor, media, desvio):
    if desvio == 0 or pd.isna(desvio):
        return None

    z = (valor - media) / desvio

    # só considera anômalo se estiver realmente fora do padrão
    if abs(z) < 1.5:
        return None

    # regras de texto
    if col == "valor_executado":
        if z > 0:
            return "valor_executado muito alto"
        else:
            return "valor_executado muito baixo"

    elif col == "valor_orcado":
        if z > 0:
            return "valor_orcado acima do padrão"
        else:
            return "valor_orcado abaixo do padrão"

    elif col == "percentual_execucao":
        if z > 0:
            return "percentual_execucao muito alto"
        else:
            return "percentual_execucao muito baixo"

    elif col == "atraso_dias":
        if z > 0:
            return "atraso_dias muito alto"
        else:
            return "atraso_dias abaixo do padrão"

    elif col == "aditivos":
        if z > 0:
            return "aditivos altos"
        else:
            return "aditivos baixos"

    elif col == "pendencias":
        if z > 0:
            return "pendencias altas"
        else:
            return "pendencias baixas"

    return None

for _, row in anomalias.iterrows():
    print(f"\n{row['obra']}")
    print("Variáveis anômalas:")

    achados = []

    for col in features:
        texto = interpretar_variavel(col, row[col], medias[col], desvios[col])
        if texto:
            achados.append(texto)

    if achados:
        for item in achados:
            print(f"- {item}")
    else:
        print("- sem variável individual muito destacada; anomalia detectada pelo conjunto")

plt.show()
df.to_csv("resultado_obras.csv", index=False)

