import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from flask import request, session, json
from utils import utils_google, utils
import pandas as pd
import requests

def serve_layout():

    layout = html.Div([
                        html.Div(id='none',children=[],style={'display': 'none'})
                        , dbc.Col(
                                dbc.Row([
                                        html.H1(
                                                f"Admin Digitalia",
                                                id="title",
                                                )
                                        ],
                                        justify = 'center'
                                        )
                                    )
                        , dbc.Col(dbc.Row(id = 'table-orders-row', style={"height":"auto", "overflow":"auto"}), style={"margin":"5px"})

                        ], className = "dash-inside-container")
    return layout

def init_callbacks(dash_app):

    @dash_app.callback(Output('table-orders-row', 'children'),
    [Input('none', 'children')])
    def table(none):
        print("start table")
        df_tickets = utils_google.read_ws_data(utils_google.open_ws("Base_general_Digitalia", "Proyectos"))
        df_tickets = df_tickets.astype(str)
        print(df_tickets)
        print("finished table correctly")
        return utils.create_data_table(df = df_tickets, id = "table-projects")
