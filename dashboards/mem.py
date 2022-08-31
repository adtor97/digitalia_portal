#from pydoc import classname
#from tkinter.ttk import Separator
#from turtle import width
import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from flask import request, session, json
from utils import utils_google, utils
import plotly.express as px
import pandas as pd
import requests

typo='utf-8'

# df = pd.read_excel("data/laptopsv2.xlsx")
df = pd.read_csv("data/laptops_final.csv",engine='python',sep=';', encoding=typo)
# df['cluster_predicted'] = df['cluster_predicted'].map({0:'Gama Alta',
#                              1:'Gama Media',
#                              2:'Gama Media Alta ',
#                              3:'Gama Baja Media',
#                              4:'Gama Baja'},
#                              na_action=None)

marca = df['Marca'].unique()
options_marca = [{"label":marca[i], "value":marca[i]} for i in range(len(marca))]

cluster = df['cluster_predicted'].unique()
options_cluster = [{"label":cluster[i], "value":cluster[i]} for i in range(len(cluster))]


def serve_layout():

    layout = html.Div([
                        html.Div(id='none',children=[],style={'display': 'none'})
                        , dbc.Col(
                                dbc.Row([
                                        html.H1(
                                                f"Datos de laptops extraídos de plataformas ecommerce",
                                                id="title",
                                                )
                                        ],
                                        justify = 'center'
                                        ),

                                    ),

                        html.Div([
                            dbc.Row([
                                dbc.Col([
                                    utils.dropdown(id='drop-marca',options=options_marca,value=None, multi=False, placeholder="Elige la marca de tu laptop", className='dropdown'),
                                ],
                                width=4,
                                className='input-col'
                                )
                            ],
                            className = 'inputs-row',
                            style={'margin':'30px'}
                            ),
                            dbc.Row([
                                dbc.Col([
                                    utils.dropdown(id='drop-cluster',options=options_cluster,value=None, multi=False, placeholder="Elige la categoría de tu laptop", className='dropdown'),
                                ],
                                width=4,
                                className='input-col'
                                )
                            ],
                            className = 'inputs-row',
                            style={'margin':'30px'}
                            ),
                            html.Div(id='table1-div'),
                        ]),
                        html.Div(id='none',children=[],style={'display': 'none'})
                        , dbc.Col(
                                dbc.Row([
                                        html.H2(
                                                f"Laptops sugeridas por título",
                                                id="sub-title",
                                                )
                                        ],
                                        justify = 'center'
                                        )
                                    ),
                        html.Div(id='table2-div'),
                        html.Div(id='none',children=[],style={'display': 'none'})
                        , dbc.Col(
                                dbc.Row([
                                        html.H2(
                                                f"Laptops sugeridas por características y precio",
                                                id="sub-title",
                                                )
                                        ],
                                        justify = 'center'
                                        )
                                    ),
                        html.Div(id='table3-div')

                        ],className='dash-inside-container')


    return layout

def init_callbacks(dash_app):

    # Dropdown por marca
    @dash_app.callback(
                        Output('table1-div','children'),
                        Input('drop-marca','value'),
                        Input('drop-cluster','value')
    )
    def filtro(marca,cluster):

        df = pd.read_csv("data/laptops_final.csv",engine='python',sep=';', encoding=typo)
        # df = pd.read_excel("data/laptopsv2.xlsx")
        df=df.loc[:,['Titulo','Tienda','Precio Online','Precio Normal','Marca','Tarjeta de Video','Procesador','Memoria Ram','Pulgadas Pantalla','Almacenamiento','Link','Recomendados','cluster_predicted']]
        if (marca==None) and (cluster==None):
            return utils.create_data_table(df,id='tabla1', row_selectable="single")
        elif marca==None:
            df = df.loc[(df['cluster_predicted'] == cluster)]
            return utils.create_data_table(df,id='tabla1', row_selectable="single")
        elif cluster==None:
            df = df.loc[(df['Marca'] == marca)]
            return utils.create_data_table(df,id='tabla1', row_selectable="single")
        else:
            df = df.loc[(df['Marca'] == marca)&(df['cluster_predicted']==cluster)]
            return utils.create_data_table(df,id='tabla1', row_selectable="single")


    @dash_app.callback(
                        Output('table2-div','children'),
                        Input('tabla1','data'),
                        Input('tabla1','selected_rows')
    )
    def tabla_sugeridos(data,selected_rows):
        df = pd.read_csv("data/laptops_final.csv",engine='python',sep=';', encoding=typo)
        # f = pd.read_excel("data/laptopsv2.xlsx")
        df=df.loc[:,['Titulo','Tienda','Precio Online','Precio Normal','Marca','Tarjeta de Video','Procesador','Memoria Ram','Pulgadas Pantalla','Almacenamiento','Link','Recomendados','cluster_predicted']]
        print('mostrar tabla de sugeridos')
        if selected_rows is None: return None
        print('selected_rows')
        df_fila = pd.DataFrame(data)
        df_fila = df_fila.iloc[selected_rows]

        # list_recom = df_fila['Recomendados'][0]
        # list_recom = eval(list_recom)

        #numero = [selected_rows]
        numero_string = ' '.join(map(str, selected_rows))
        numero_int = int(numero_string)
        list_recom = df_fila.at[numero_int,'Recomendados']
        list_recom = eval(list_recom)
        print(selected_rows)
        # print(list_recom[1])
        # print(list_recom[2])
        # print(list_recom)
        df_nuevo = pd.DataFrame()
        for i in range(len(list_recom)):
            df_recom = df.loc[(df['Titulo'] == list_recom[i])]
            df_nuevo = df_nuevo.append(df_recom,ignore_index=True)

        return utils.create_data_table(df_nuevo,id='table-recomendados-1')


    @dash_app.callback(
                        Output('table3-div','children'),
                        Input('tabla1','data'),
                        Input('tabla1','selected_rows')
    )
    def tabla_cluster(data,selected_rows):
        df = pd.read_csv("data/laptops_final.csv",engine='python',sep=';', encoding=typo)
        # f = pd.read_excel("data/laptopsv2.xlsx")
        df=df.loc[:,['Titulo','Tienda','Precio Online','Precio Normal','Marca','Tarjeta de Video','Procesador','Memoria Ram','Pulgadas Pantalla','Almacenamiento','Link','Recomendados','cluster_predicted']]
        print('mostrar tabla de sugeridos')
        if selected_rows is None: return None
        print('selected_rows')
        df_fila = pd.DataFrame(data)
        df_fila = df_fila.iloc[selected_rows]

        numero_string = ' '.join(map(str, selected_rows))
        numero_int = int(numero_string)
        list_cluster = df_fila.at[numero_int,'cluster_predicted']
        list_precio = float(df_fila.at[numero_int,'Precio Online'])

        df_cluster = df
        df_cluster.loc[:, 'cluster_predicted'] = list_cluster
        df_cluster = df_cluster[(df_cluster["Precio Online"]<=list_precio+500) & (df_cluster["Precio Online"]>=list_precio-500)]
        #df_cluster = df_cluster

        return utils.create_data_table(df_cluster,id='table-recomendados-2')
