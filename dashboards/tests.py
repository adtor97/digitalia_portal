import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State, MATCH, ALL
from flask import request, session
import os
import pandas as pd
from utils import utils, utils_tests


def serve_layout():

    layout = html.Div(
                        [
                        dbc.Row(
                                    [
                                        dbc.Col(
                                            html.H1(
                                                "Tests Digitalia",
                                                id="title-tests",
                                                className="text-center",
                                                style={"font-size": "48px", "color": "#333", "margin-bottom": "20px"}
                                            ),
                                            width=12
                                        ),
                                        dbc.Col(
                                            html.P(
                                                [
                                                    "¡Hola! Elige el test del puesto al que postulas. Por favor, lee atentamente las indicaciones. Para consultas puedes contactar: ",
                                                    html.A("WhatsApp", href="https://wa.me/969051542", target="_blank", style={"color": "#25D366", "text-decoration": "underline"})
                                                ],
                                                id="subtitle-tests",
                                                className="text-justify",
                                                style={"maxWidth": "600px", "margin": "0 auto", "font-size": "18px"}
                                            ),
                                            width=12
                                        )
                                    ],
                                    justify='center',
                                    style={"margin-top": "5%", "margin-bottom": "5%"}
                                )
                        , dcc.Store(
                                    id='store-xxxx-tests'
                                    , data=None
                                )
                        , dbc.Row(
                                    [
                                        dbc.Col(
                                                [
                                                    html.Label(
                                                                html.Strong("Elige el puesto para el que deseas postular")
                                                                , className="label"
                                                                )
                                                    , utils.dropdown(
                                                                    "dropdown-position-tests"
                                                                    , className='dropdown'
                                                                    , options=[
                                                                                {"label":"Marketplace - Fullstack .Net & React", "value":"net_react_juntoz"}
                                                                                , {"label":"USA - Backend Django", "value":"startusa_backend_django"}
                                                                                , {"label":"USA - Frontend React | React Native", "value":"startusa_frotend_react"}
                                                                            ]
                                                                    , value=None
                                                                    , multi=False
                                                                    , placeholder="Elige la posición"
                                                                    )
                                                ]
                                                , sm=12
                                                , md=10
                                                , lg=6
                                                )
                                    ]
                                    , id="row-XXXX-tests"
                                )
                        , dcc.Loading(
                                    dbc.Row(
                                                id="row-test-tests"
                                                , style={"paddingTop":"30px", "overflow":"auto"}
                                            )
                                    )
                        ]
                        , className = "dash-inside-container"
                        , style = {"margin-bottom":"100px"}
                    )
    return layout

def init_callbacks(dash_app):
    @dash_app.callback(
                        Output('row-test-tests','children'),
                        Input('dropdown-position-tests','value'),
    )
    def show_test(test):
        return utils_tests.tests_values(test)
