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


reference_products = [
    'BANANA NANICA', 'MAMAO PAPAYA', 'ALFACE', 'TOMATE', 'CEBOLA', 
    'REPOLHO', 'REPOLHO ROXO', 'BETERRABA', 'BATATA MONALISA', 'PEPINO', 'PAO FRANCES', 'PAO HOT DOG', 'PIMENTAO', 'MELANCIA'
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
        df = pd.read_excel(file_path)
        
        # Adiciona o dataframe à lista
        dataframes.append(df)

# Faz a concatenação de todos os dataframes
df_full = pd.concat(dataframes, ignore_index=True)

# Aplicar a substituição de vírgula por ponto nas colunas específicas
df_full['valor_un_tributavel'] = df_full['valor_un_tributavel'].apply(converter_decimal).astype(float)
df_full['valor_un_comercializacao'] = df_full['valor_un_comercializacao'].apply(converter_decimal).astype(float)
df_full['qtd'] = df_full['qtd'].apply(converter_decimal).astype(float)  # Converter quantidade para float, se ainda não estiver

# Criar uma nova coluna 'valor_unitario' ajustada
df_full['valor_unitario'] = df_full.apply(
    lambda row: row['valor_un_tributavel'] / row['qtd'] if row['unidade'] == 'UNID' and row['qtd'] != 0 else row['valor_un_tributavel'], axis=1
)

# Aplicar a normalização apenas para os produtos com 'cod_ean' igual a 'SEM GTIN'
df_full['descricao_normalizado'] = df_full.apply(
    lambda row: normalize_product_name(row['descricao'], reference_products) if row['cod_ean'] == 'SEM GTIN' else row['descricao'], axis=1
)

# Define o COD_EAN como a própria descricao_normalizado, caso seja SEM GTIN
df_full['cod_ean_desc'] = df_full.apply(lambda row: row['descricao_normalizado'] if row['cod_ean'] == 'SEM GTIN' else row['cod_ean'], axis=1)

# Filtrar produtos com mais de 1 registro
df_full = df_full[df_full.groupby('cod_ean_desc')['cod_ean_desc'].transform('count') > 1]

# Calcular a variacao de precos, agrupando por cod_ean_desc
df_full['variacao_preco'] = df_full.groupby('cod_ean_desc')['valor_unitario'].pct_change()

# Criar um novo DataFrame que contém a última variação de preço para cada produto
df_variacao_preco = df_full.drop_duplicates('cod_ean_desc', keep='last')[['cod_ean_desc', 'descricao_normalizado', 'variacao_preco']]

df_variacao_preco = df_variacao_preco.dropna().reset_index(drop=True)

# Calcular a inflação real como a média da variação percentual de todos os produtos
inflacao_real = df_variacao_preco['variacao_preco'].mean()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H3(f"Inflação Real: {inflacao_real:.2%}"),  # Exibe a inflação real no layout
    dcc.Graph(id='variacao-preco-graph'),  # Gráfico para variação de preço
    dcc.Graph(id='preco-graph')  # Gráfico para preço ao clicar em produto
])

index_to_cod_ean_desc = {}  # Dicionário para mapear índices para cod_ean_desc

@app.callback(
    Output('variacao-preco-graph', 'figure'),
    [Input('preco-graph', 'clickData')]
)
def update_variacao_preco_graph(clickData):
    data = []
    global index_to_cod_ean_desc
    index_to_cod_ean_desc = {}
    
    for i, produto in enumerate(df_variacao_preco['cod_ean_desc'].unique()):
        df_filtrado = df_variacao_preco[df_variacao_preco['cod_ean_desc'] == produto]
        data.append(go.Bar(
            x=df_filtrado['descricao_normalizado'], 
            y=df_filtrado['variacao_preco'], 
            name=produto,
            text=[f"{x:.2%}" for x in df_filtrado['variacao_preco']],  # Adiciona o valor da variação de preço em cada barra
            textposition='auto'  # Posiciona o texto dentro das barras
        ))
        index_to_cod_ean_desc[i] = produto  # Adicione o mapeamento ao dicionário
    
    # Criação do gráfico de variação de preço
    fig = go.Figure(data=data)
    
    # Definindo altura personalizada
    fig.update_layout(
        title='Variação de Preço de Todos os Produtos ao Longo do Tempo', 
        xaxis_title='Produto', 
        yaxis_title='Variação de Preço',
        yaxis=dict(tickformat=".2%", showgrid=True),  # Formato de porcentagem para variação de preço
        height=900  # Defina a altura do gráfico
    )
    
    return fig

@app.callback(
    Output('preco-graph', 'figure'),
    [Input('variacao-preco-graph', 'clickData')]
)
def update_graph(clickData):
    if clickData is None:
        # Se nenhum dado foi clicado, não exiba nada
        return go.Figure()
    else:
        # Obtenha o produto selecionado a partir dos dados clicados
        produto_selecionado = index_to_cod_ean_desc[clickData['points'][0]['curveNumber']]
        
        # Filtra os dados com base no produto selecionado
        df_filtrado = df_full[df_full['cod_ean_desc'] == produto_selecionado]
        
        # Obtém o nome do produto a partir da coluna 'descricao_normalizado'
        nome_produto = df_filtrado['descricao_normalizado'].iloc[0]
        
        # Agora agrupamos os dados por cnpj_empresa e nome_empresa e plotamos uma linha para cada empresa
        fig = go.Figure()

        for cnpj, nome_empresa in df_filtrado.groupby(['cnpj_empresa', 'nome_empresa']).groups.keys():
            df_empresa = df_filtrado[(df_filtrado['cnpj_empresa'] == cnpj) & (df_filtrado['nome_empresa'] == nome_empresa)]
            fig.add_trace(go.Scatter(
                x=df_empresa['data_nf'], 
                y=df_empresa['valor_unitario'], 
                mode='lines+markers', 
                name=f'{nome_empresa} ({cnpj})',
                showlegend=True  # Força a legenda a ser exibida
            ))

        titulo = f"Variação de Preços ao Longo do Tempo por Empresa para o produto: {nome_produto}"
        
        # Ajustes do layout
        fig.update_layout(
            title=titulo, 
            xaxis_title='Data', 
            yaxis_title='Preço Unitário',
            yaxis=dict(tickprefix="R$ ", tickformat=".2f", showgrid=True),
            height=600  # Defina a altura do gráfico
        )
        return fig

if __name__ == '__main__':
    app.run_server(debug=True)
