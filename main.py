import pandas as pd
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

planilha = client.open_by_key(ID_PLANILHA)
sheet = planilha.sheet1

dados = sheet.get_all_records()
df = pd.DataFrame(dados)

# print("\nBase carregada:")
# print(df.head())

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
df["score"] = modelo.decision_function(X_scaled)
df["classificacao"] = df["predicao"].map({1: "Normal", -1: "Anomalia"})

df = df.sort_values(by="score").reset_index(drop=True)

# =========================
# 6. Mostrar resultados
# =========================
print("\nResultado final:")
print(df.to_string(formatters={"score": "{:.2f}".format}))

print("\nSomente anomalias encontradas:")
print(df[df["classificacao"] == "Anomalia"][["obra", "score"]])

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

# =========================
# 8. Resumo das anomalias
# =========================
print("\nResumo das anomalias:")

anomalias = df[df["classificacao"] == "Anomalia"].copy()
medias = df[features].mean()
desvios = df[features].std()

def interpretar_variavel(col, valor, media, desvio):
    if desvio == 0 or pd.isna(desvio):
        return None

    z = (valor - media) / desvio

    if abs(z) < 2.0:
        return None

    if col == "valor_executado":
        return "valor_executado muito alto" if z > 0 else "valor_executado muito baixo"
    elif col == "valor_orcado":
        return "valor_orcado acima do padrão" if z > 0 else "valor_orcado abaixo do padrão"
    elif col == "percentual_execucao":
        return "percentual_execucao muito alto" if z > 0 else "percentual_execucao muito baixo"
    elif col == "atraso_dias":
        return "atraso_dias muito alto" if z > 0 else "atraso_dias abaixo do padrão"
    elif col == "aditivos":
        return "aditivos altos" if z > 0 else "aditivos baixos"
    elif col == "pendencias":
        return "pendencias altas" if z > 0 else "pendencias baixas"

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

# =========================
# 9. Salvar arquivos
# =========================
plt.savefig("grafico_anomalias.png", dpi=300, bbox_inches="tight")
df.to_csv("resultado_obras.csv", index=False)

plt.show()
