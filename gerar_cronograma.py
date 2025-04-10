
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime, timedelta

# CONFIGURAÇÕES
CAMINHO_CREDENCIAL = 'credentials.json'
NOME_PLANILHA = 'Cronograma Casa Completa'
ABA_PLANILHA = 'Cronograma Visual'

# Conectar ao Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file(CAMINHO_CREDENCIAL, scopes=scope)
client = gspread.authorize(creds)
sheet = client.open(NOME_PLANILHA).worksheet(ABA_PLANILHA)

# Carregar dados da planilha
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Transformar datas
df['Data Início'] = pd.to_datetime(df['Data Início'])
df['Data Fim'] = pd.to_datetime(df['Data Fim'])

# Preparar o gráfico
start_date = df['Data Início'].min()
end_date = df['Data Fim'].max()
dias = pd.date_range(start=start_date, end=end_date, freq='D')
colaboradores = df['Colaborador / Equipe'].unique().tolist()

fig, ax = plt.subplots(figsize=(20, 6))
y_positions = {name: i for i, name in enumerate(reversed(colaboradores), start=1)}

cores_clientes = {}
cor_index = 0
palette = plt.get_cmap("tab10").colors

for _, row in df.iterrows():
    y = y_positions[row['Colaborador / Equipe']]
    x_start = row['Data Início']
    x_end = row['Data Fim']
    label = row['Cliente']

    if label not in cores_clientes:
        cores_clientes[label] = palette[cor_index % len(palette)]
        cor_index += 1

    ax.barh(y, (x_end - x_start).days + 1, left=x_start, height=0.6, color=cores_clientes[label], edgecolor='black')
    ax.text(x_start + timedelta(days=((x_end - x_start).days) / 2), y, label, va='center', ha='center', color='white', fontsize=8, fontweight='bold')

# Configurações visuais
ax.set_yticks(list(y_positions.values()))
ax.set_yticklabels(list(y_positions.keys()))
ax.invert_yaxis()
ax.set_xlim(start_date - timedelta(days=1), end_date + timedelta(days=1))
ax.xaxis.set_major_locator(plt.MultipleLocator(7))
ax.grid(axis='x', linestyle='--', alpha=0.5)
plt.title('Cronograma da Produção - Casa Completa', fontsize=14)
plt.tight_layout()

# Legenda
legenda = [mpatches.Patch(color=c, label=cliente) for cliente, c in cores_clientes.items()]
ax.legend(handles=legenda, loc='upper right')

# Salvar como imagem
plt.savefig('cronograma.png', dpi=300)
plt.show()
