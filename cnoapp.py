# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 10:39:58 2022

@author: Farley
"""
# importando bibliotecas ------------------------------------------------------
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback_context

# ------------------------------------------------------------------------------
# Carregando banco de dados e definindo outras variaveis----------------------
df = pd.read_csv('mg_final(2020)d.csv')
px.set_mapbox_access_token(
    'pk.eyJ1IjoiZmFybGV5c2FsZiIsImEiOiJja3puMGl0aTQyc2h6MnVvYjRjbDNwb2VkIn0.eXTCViUG_yv5BuLfehPhVw')
lista_cidades = list(df['Município'].unique())
lista_cidades.sort()
datas = {
    1: '2020-01-01',
    2: '2020-02-01',
    3: '2020-03-01',
    4: '2020-04-01',
    5: '2020-05-01',
    6: '2020-06-01',
    7: '2020-07-01',
    8: '2020-08-01',
    9: '2020-09-01',
    10: '2020-10-01',
    11: '2020-11-01',
    12: '2020-12-01',
    13: '2021-01-01',
    14: '2021-02-01',
    15: '2021-03-01',
    16: '2021-04-01',
    17: '2021-05-01',
    18: '2021-06-01',
}
dfcnae = pd.read_csv('cnae3.csv')


# ------------------------------------------------------------------------------
# definindo funções dos graficos
# definindo função para o mapa de disperção
def mapa(df, value):
    fig = px.scatter_mapbox(df, lat='latitude', lon='longitude', color=value,
                            hover_data=['id CNO', 'CNAE', 'Endereço',
                                        'Data de Registro', 'Data de Início',
                                        'Situação', 'Data da Situação',
                                        'Município', 'Responsável'],
                            height=550,
                            color_discrete_sequence=px.colors.qualitative.Light24,
                            mapbox_style='dark'
                            )
    fig.update_layout(
        legend={'orientation': 'h'},
    )
    fig.update_traces(marker_opacity=0.60, marker_size=5, selector=dict(type='scattermapbox'))
    fig.update_mapboxes(center={'lat': -18, 'lon': -43},
                        zoom=5.5)

    return [fig]


# ------------------------------------------------------------------------------
# definindo função para o grafico de barras------------------------------------
def g_barra(value):
    df2 = df[df['Município'] == value]
    df3 = df2.groupby(['Código CNAE', 'Situação']).agg({'Obras': 'sum'})
    df3.reset_index(level=0, inplace=True)
    df3.reset_index(level=0, inplace=True)
    df3 = pd.merge(df3, dfcnae, on='Código CNAE', how='left')
    fig2 = px.bar(df3, x='Código CNAE', y="Obras", color='Situação',
                  title=f'{value} - Total de Obras por Setor (CNAE 7 dígitos)', hover_data=['CNAE'],
                  text='Obras',
                  height=550)
    fig2.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig2.update_layout(
        title_pad={'b': 0, 'l': 400, 'r': 0, 't': 0})
    return [fig2]


# ------------------------------------------------------------------------------
app = Dash(__name__)
server = app.server
# ------------------------------------------------------------------------------
# Configurando layout do app
app.layout = html.Div([
    html.H1('Distribuição Geógrafica de Obras Cadastradas (CNO) - Minas Gerais',
            style={'text-align': 'center'}),

    html.Div(
        dcc.Graph(id="mapa")),

    html.Div(
        dcc.RadioItems(id='radio',
                       options=[
                           {'label': 'CNAE 7 dígitos', 'value': 'Código CNAE'},
                           {'label': 'CNAE 3 dígitos', 'value': 'CNAE (3 digitos)'},
                           {'label': 'Situação', 'value': 'Situação'},
                       ],
                       value='CNAE (3 digitos)'
                       )),

    dcc.RangeSlider(
        id='slider',
        min=1,
        max=18,
        step=None,
        marks=datas,
        value=[1, 18]
    ),

    html.Div(html.P(''), ),

    html.Div(
        dcc.Dropdown(
            id='dropdown2',
            options=[{'label': i, 'value': i} for i in lista_cidades],
            value='Belo Horizonte'
        )),

    html.Div(
        dcc.Graph(id="bar")),

    html.Div([
        dcc.Markdown("© 2022 Farley Salomão F. " +
                     "[[Github]](https://github.com/FarleySalomao) " +
                     "[[Linkedin]](https://www.linkedin.com/in/farleysalomao) "
                     "" +
                     "[[Email]](mailto:ivanlai.uk.2020@gmail.com)")

    ], style={'textAlign': 'right',
              'width': '29%'},
        className="four columns"
    )

])


# -----------------------------------------------------------------------------
# Configurando os callbacks do app
@app.callback(
    [Output(component_id='mapa', component_property='figure')],
    [Input('radio', 'value')], [Input('slider', 'value')])
def update_legenda(value_a, value_b):
    df2 = df.copy()
    df2 = df2.loc[(df2['Data de Início'] >= datas[value_b[0]]) &
                  (df2['Data de Início'] <= datas[value_b[1]])]

    return mapa(df2, value_a)


@app.callback(
    [Output(component_id='bar', component_property='figure')],
    [Input('dropdown2', 'value')])
def update_cidade(value2):
    return g_barra(value2)


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
