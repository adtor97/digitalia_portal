import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from flask import request, session
from utils.utils_login import loginizer

def serve_layout():
    index_login = html.Div([
                            dbc.Row([html.H1("Login Portal Digitalia", id="title", style={"color":"#1b2b58", "font-size":"28px"})],
                                    justify = 'center'),
                            dbc.Row([
                                    dbc.Col([dbc.Form([
                                                        dbc.Input(type="email", id="login-username", placeholder="Enter email", className="login-username-input")
                                                        , dbc.Input(type="password", id="login-password", placeholder="Enter password", className="login-password-input")
                                                        , html.Button("Login", id="btn-login")
                                                        , dcc.Loading(dbc.Row(id="login-result"), type="circle")
                                                        ])
                                            , dbc.Row(html.Button("Reset or Sign up", id="btn-login-reset"))
                                            , dbc.Row(id='login-reset')
                                            ]),

                                ], style={"min-width":"25%", 'display':'flex'})
                        ], className = "dash-inside-container")
    return index_login
#dbc.NavLink("Login succesful! Click to go to Menu", active=True, href="/", external_link=True, style={'margin-left':'auto','margin-right':'auto', 'margin-top':'5px'})
#

def init_callbacks(dash_app):
    @dash_app.callback(
    Output('login-result', 'children'),
    [Input('btn-login', 'n_clicks')],
    [State('login-username', 'value'), State('login-password', 'value')
    ])
    def login_result(n_clicks, username, password):
        print("start login_result")
        #print("login_result:", n_clicks, username, password)
        if n_clicks is None:
            print("finished login_result correctly")
            return None
        if username is None or password is None:
            print("finished login_result correctly")
            return html.P(children=["Usuario o contraseña equivocado, por favor vuelve a intentar."], style={"color":"red", 'margin-left':'auto','margin-right':'auto', 'margin-top':'5px'})
        login_result = loginizer(username, password)
        #print(login_result)
        if login_result == False:
            print("finished login_result correctly")
            return html.P(children=["Usuario o contraseña equivocado, por favor vuelve a intentar."], style={"color":"red", 'margin-left':'auto','margin-right':'auto', 'margin-top':'5px'})
        else:
            session['user'] = login_result
            print("finished login_result correctly")
            return dcc.Location(id='login-url', href='/', refresh=True)
            #return dbc.NavLink("Login succesful! Click to go to Menu", active=True, href="/", external_link=True, style={'margin-left':'auto','margin-right':'auto', 'margin-top':'5px'})

    @dash_app.callback(
    Output('login-reset', 'children'),
    [Input('btn-login-reset', 'n_clicks')
    ])
    def login_reset(n_clicks):
        print("start login_reset")
        if n_clicks is None: n_clicks=0
        if n_clicks//2 != n_clicks/2:
            print("finished login_reset correctly")
            return html.P(id="text-login-reset",
                            children=["Estamos trabajando en esta funcionalidad", html.Br(),
                                      html.A(html.Strong('Para resetear contraseña o crear usuario click acá.'), href='https://wa.link/kk1twp', target='_blank')],
                                      style={"width":"60%", "text-align":"center", "margin-left": "auto", "margin-right": "auto", "margin-top":"15px"}
                            )
        else:
            print("finished login_reset correctly")
            return None
