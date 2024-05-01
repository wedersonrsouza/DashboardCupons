import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

# Carregando os dados dos cupons fiscais
df_full = pd.read_excel('Estudos\df_full.xlsx')

## Define o COD_EAN como a propria descricao, caso seja SEM GTIN:

df_full['cod_ean_desc'] = df_full.apply(lambda row: row['descricao'] if row['cod_ean'] == 'SEM GTIN' else row['cod_ean'], axis=1)


# Filtrar produtos com mais de 1 registro
df_full = df_full[df_full.groupby('cod_ean_desc')['cod_ean_desc'].transform('count') > 1]

## Calcular a variacao de precos, agrupando por cod_ean_desc

df_full['variacao_preco'] = df_full.groupby('cod_ean_desc')['valor_un_comercializacao'].pct_change()

# Criar um novo DataFrame que contém a última variação de preço para cada produto
df_variacao_preco = df_full.drop_duplicates('cod_ean_desc', keep='last')[['cod_ean_desc', 'descricao', 'variacao_preco']]

df_variacao_preco = df_variacao_preco.dropna().reset_index(drop=True)

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='variacao-preco-graph'),  # Gráfico para variação de preço
    dcc.Graph(id='preco-graph')  # Gráfico para preço
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
            x=df_filtrado['descricao'], 
            y=df_filtrado['variacao_preco'], 
            name=produto,
            text=[f"{x:.2%}" for x in df_filtrado['variacao_preco']],  # Adiciona o valor da variação de preço em cada barra
            textposition='auto'  # Posiciona o texto dentro das barras
        ))
        index_to_cod_ean_desc[i] = produto  # Adicione o mapeamento ao dicionário
    fig = go.Figure(data=data)
    fig.update_layout(title='Variação de Preço de Todos os Produtos ao Longo do Tempo', xaxis_title='Produto', yaxis_title='Variação de Preço',
                      yaxis=dict(tickformat=".2%", showgrid=True))  # Formato de porcentagem para variação de preço
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
        print(clickData)
        # Obtenha o produto selecionado a partir dos dados clicados
        produto_selecionado = index_to_cod_ean_desc[clickData['points'][0]['curveNumber']]
        df_filtrado = df_full[df_full['cod_ean_desc'] == produto_selecionado]
        df_filtrado = df_filtrado[['data_nf', 'descricao', 'valor_un_comercializacao']]
        print(df_filtrado)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_filtrado['data_nf'], y=df_filtrado['valor_un_comercializacao'], mode='lines+markers', name='Preço'))
        fig.update_layout(title='Variação de Preços ao Longo do Tempo', xaxis_title='Data', yaxis_title='Preço',
                          yaxis=dict(tickprefix="R$ ", showgrid=True))
        return fig

if __name__ == '__main__':
    app.run_server(debug=True)
