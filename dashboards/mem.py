import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from flask import request, session, json
from utils import utils_google, utils
import pandas as pd
import requests

df = pd.read_csv("templates/data.csv")

def serve_layout():

    layout = html.Div([
                        html.Div(id='none',children=[],style={'display': 'none'})
                        , dbc.Col(
                                dbc.Row([
                                        html.H1(
                                                f"MEM",
                                                id="title",
                                                )
                                        ],
                                        justify = 'center'
                                        )
                                    )

                        ], className = "dash-inside-container")
    return layout

def init_callbacks(dash_app):

    return None
