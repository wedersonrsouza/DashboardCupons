import os

import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output
from rapidfuzz import process


# Função para substituir vírgulas por pontos
def converter_decimal(valor):
    if isinstance(valor, str):
        return valor.replace(',', '.')
    return valor


# Função de normalização com tratamento para NoneType
def normalize_product_name(product_name, reference_list):
    # Verifica se a referência não é nula ou vazia
    if pd.isna(product_name) or not reference_list:
        return product_name  # Retorna o valor original se for inválido

    # Tenta encontrar o melhor match
    result = process.extractOne(product_name, reference_list)
    
    # Verifica se o resultado não é None
    if result:
        best_match = result[0]  # A melhor correspondência
        score = result[1]  # A pontuação de similaridade
        # Define um limite de similaridade (por exemplo, 80)
        if score >= 80:
            return best_match
    
    # Retorna o nome original caso não haja match adequado ou se o resultado for None
    return product_name


# Lista de produtos de referência
reference_products = [
    'BANANA NANICA', 'MAMAO PAPAYA', 'ALFACE', 'TOMATE', 'CEBOLA', 
    'REPOLHO', 'REPOLHO ROXO', 'BETERRABA', 'BATATA MONALISA', 'PEPINO'
]

# Lista para armazenar os dataframes individuais
dataframes = []
directory_path = "Cupons"  # Defina o caminho correto para sua pasta

# Percorre todos os arquivos na pasta
for file_name in os.listdir(directory_path):
    # Verifica se o arquivo é um XLSX
    if file_name.endswith('.xlsx'):
        file_path = os.path.join(directory_path, file_name)
        
        # Carrega o arquivo XLSX em um dataframe com conversão de vírgula para ponto
        df = pd.read_excel(file_path, converters={'valor_un_tributavel': converter_decimal})
        
        # Adiciona o dataframe à lista
        dataframes.append(df)

# Faz a concatenação de todos os dataframes
df_full = pd.concat(dataframes, ignore_index=True)

# Verifica se a coluna 'valor_un_tributavel' é realmente string
if df_full['valor_un_tributavel'].dtype == 'object':
    # Se ainda for string, converte para float
    df_full['valor_un_tributavel'] = df_full['valor_un_tributavel'].str.replace(',', '.').astype(float)

# Aplica a normalização a cada nome de produto na coluna 'descricao'
df_full['descricao_normalizado'] = df_full['descricao'].apply(lambda x: normalize_product_name(x, reference_products))

# Exibe as primeiras linhas do dataframe para ver o resultado
print(df_full.head())
