import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from flask import request, session, json
from utils import utils_google, utils
import pandas as pd
import requests
import numpy as np

import plotly.graph_objects as go
from plotly.offline import plot
import plotly_express as px
from plotly.subplots import make_subplots

def serve_layout():

    layout = html.Div([
                        html.Div(id='none-artefacta',children=[],style={'display': 'none'})
                        , dbc.Col(
                                dbc.Row([
                                        html.H1(
                                                f"Artefacta vs Marcimex",
                                                id="title-artefacta",
                                                className="title"
                                                )
                                        ],
                                        justify = 'center'
                                        )
                                    )
                        , dbc.Row([
                            dbc.Col(dbc.Row(id = 'kpis-products-row', style={"height":"auto", "overflow":"auto"}, justify = 'center'), width=12)
                            ]
                            , style={"marginBottom":"25px"}
                            )
                        , dbc.Row([
                            dbc.Col(dbc.Row(id = 'graph-products-row', style={"height":"auto", "overflow":"auto"}, justify = 'center'), width=12)
                            ])
                        , dbc.Row([
                            dbc.Col(dbc.Row(id = 'table-products-row', style={"height":"auto", "overflow":"visible", "justify-content":"center"}), width=12)
                            ])
                        ], className = "dash-inside-container")
    return layout

def init_callbacks(dash_app):

    @dash_app.callback(Output('kpis-products-row', 'children'), Output('table-products-row', 'children'), Output('graph-products-row', 'children'),
    [Input('none-artefacta', 'children')])
    def layout_products(none):
        print("start table")
        df_artefacta = utils_google.read_ws_data(utils_google.open_ws("base_general_artefacta", "productos_artefacta"))
        df_artefacta = df_artefacta.replace({"\$ ":""}, regex=True).replace({"\$":"", ",":""}, regex=True)
        df_artefacta["precio_anterior"] = df_artefacta.apply(lambda x: x["precio_actual"] if (x["precio_anterior"] is None) or (x["precio_anterior"] is np.nan) or (x["precio_anterior"] == "") else x["precio_anterior"], axis=1)
        df_artefacta["precio_anterior"] = df_artefacta["precio_anterior"].astype(float)
        df_artefacta["precio_actual"] = df_artefacta["precio_actual"].astype(float)

        df_marcimex = utils_google.read_ws_data(utils_google.open_ws("base_general_artefacta", "productos_marcimex"))
        df_marcimex = df_marcimex.replace({"\$ ":""}, regex=True).replace({"\$":"", ",":""}, regex=True)
        df_marcimex["precio_anterior"] = df_marcimex.apply(lambda x: x["precio_actual"] if (x["precio_anterior"] is None) or (x["precio_anterior"] is np.nan) or (x["precio_anterior"] == "") else x["precio_anterior"], axis=1)
        df_marcimex["precio_anterior"] = df_marcimex["precio_anterior"].astype(float)
        df_marcimex["precio_actual"] = df_marcimex["precio_actual"].astype(float)

        #df_artefacta = df_artefacta.astype(str)
        df_final = df_artefacta[["nombres", "precio_actual", "precio_anterior", "link"]].merge(df_marcimex[["nombres", "precio_actual", "precio_anterior", "link"]], on="nombres", suffixes=('_artefacta', '_marcimex'))
        df_final = df_final[["nombres", "precio_actual_artefacta", "precio_actual_marcimex", "precio_anterior_artefacta", "precio_anterior_marcimex", "link_artefacta", "link_marcimex"]]
        print(df_artefacta["precio_anterior"], df_marcimex["precio_anterior"])

        max_price = round((max(df_artefacta["precio_actual"].max(), df_marcimex["precio_actual"].max()) + 100)/100, 0)*100

        desc_artefacta = "$"+str(round(df_artefacta["precio_anterior"].sum() - df_artefacta["precio_actual"].sum(), 2))
        desc_marcimex = "$"+str(round(df_marcimex["precio_anterior"].sum() - df_marcimex["precio_actual"].sum(), 2))
        menor_artefacta = df_final.apply(lambda x: 1 if x["precio_actual_artefacta"]<x["precio_actual_marcimex"] else 0, axis=1).sum()
        menor_marcimex = df_final.apply(lambda x: 1 if x["precio_actual_marcimex"]<x["precio_actual_artefacta"] else 0, axis=1).sum()
        print('df_artefacta["precio_actual"].sum()', df_artefacta["precio_actual"].sum())
        print('df_marcimex["precio_actual"].sum()', df_marcimex["precio_actual"].sum())
        dif_precios = "$"+str(round(df_artefacta["precio_actual"].sum() - df_marcimex["precio_actual"].sum(), 2))

        print("finished table correctly")
        return [
                    [
                        utils.generate_card(value=desc_artefacta, title="Descuento total Artefacta", id="kpi-dscto_artefacta")
                        , utils.generate_card(value=desc_marcimex, title="Descuento total Marcimex", id="kpi-dscto_marcimex")
                        , utils.generate_card(value=menor_artefacta, title="Productos menor precio Artefacta", id="kpi-menor_artefacta")
                        , utils.generate_card(value=menor_marcimex, title="Productos menor precio Marcimex", id="kpi-menor_marcimex")
                        , utils.generate_card(value=dif_precios, title="Precios Artefacta-Marcimex", id="kpi-dif_precios")
                    ]
                    , utils.create_data_table(df = df_final, id = "table-products")
                    , dcc.Graph(
                            id="graph-products"
                            , figure=go.Figure(
                                            data=go.Scatter(
                                                        x=df_final["precio_actual_artefacta"].values
                                                        , y=df_final["precio_actual_marcimex"].values
                                                        , text=df_final["nombres"]
                                                        , mode='markers'
                                                        )
                                            , layout = {
                                                        "title": "Comparador"
                                                        , "xaxis_title": "Artefacta"
                                                        , "yaxis_title": "Marcimex"
                                                        , "shapes": [{'type': 'line', 'yref': 'paper', 'xref': 'paper', 'y0': 0, 'y1': 1, 'x0': 0, 'x1': 1}]
                                                        , "yaxis_range": [0, max_price]
                                                        , "xaxis_range": [0, max_price]
                                                        }
                                            )
                            , style={"width":"95%"}
                            )
                ]
