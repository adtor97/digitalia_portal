from dashboards import login, admin, experiencia_2, mem, jj, artefacta, tests
import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from flask import request, session, render_template, send_file, json, make_response, render_template_string
from datetime import datetime, date
from utils import utils, utils_google
import io
import pandas as pd
from waitress import serve

#from .layout import html_layout

def create_dashboard():
    template_dash = open("templates/layout.html")
    # print(template_dash.read())
    template_dash_ = str(template_dash.read()).replace('\n','')
    # print
    layout = str(template_dash_)

    """Create a Plotly Dash dashboard."""
    app = dash.Dash(__name__,
                    external_stylesheets = [dbc.themes.BOOTSTRAP, 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',],
                    meta_tags = [{"name": "viewport", "content": "width=device-width"}],
                    index_string=layout
                    )
                    # Create Layout

    app.title = "El Burgués Admin"

    return app

app = create_dashboard()
app.config['suppress_callback_exceptions'] = True
server = app.server
#server.secret_key = str(datetime.today())
server.secret_key = str(date.today())
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Store(id='user'),
])

index_layout = html.Div([
                        html.Div(id='none',children=[],style={'display': 'none'})
                        , html.Div(dcc.Store(id='user-info'))
                        , dbc.Row([html.H1("Elige tu ruta", id="title", style={"color":"#1b2b58", "font-size":"28px"})],
                                justify = 'center', style={"margin-top":"2%", "margin-bottom":"2%"})
                        , dbc.Col(dbc.Row(id="home-row-link", style={"min-width":"25%", 'display':'flex'}), id='home-col-row-link')
                    ], style={"margin-bottom":"100px", "max-width":"80%", 'margin-left':'auto', 'margin-right':'auto'})


login_layout = login.serve_layout()
login.init_callbacks(app)

admin_layout = admin.serve_layout()
admin.init_callbacks(app)

#virus_layout = virus.serve_layout()
#virus.init_callbacks(app)

experiencia_2_layout = experiencia_2.serve_layout()
experiencia_2.init_callbacks(app)

mem_layout = mem.serve_layout()
mem.init_callbacks(app)

jj_layout = jj.serve_layout()
jj.init_callbacks(app)

artefacta_layout = artefacta.serve_layout()
artefacta.init_callbacks(app)

tests_layout = tests.serve_layout()
tests.init_callbacks(app)

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    #global app
    #app = app
    #user = request.authorization['username']
    if pathname.lower() == '/login':
        try:  session.pop("user")
        except: pass
        return login_layout

    if pathname.lower() == '/experiencia_2':
        app.title = "Encuesta temporal"
        return experiencia_2_layout
    elif pathname.lower() == '/mem':
        app.title = "MEM"
        return mem_layout
    elif pathname.lower() == '/jj':
        app.title = "JJ"
        return jj_layout
    elif pathname.lower() == '/artefacta':
        app.title = "Artefacta"
        return artefacta_layout
    elif pathname.lower() == '/tests':
        app.title = "Tests"
        return tests_layout

    try:
        user = session["user"]
    except:
        return login_layout

    if pathname.lower() == '/admin' and 'admin' in user["usuario_vistas"]:
        app.title = "Admin"
        return admin_layout
    #elif pathname.lower() == '/virus' and 'virus' in user["usuario_vistas"]:
    #    app.title = "Virus"
    #    return virus_layout
    else:
        return index_layout
    # You could also return a 404 "URL not found" page here

@app.callback(dash.dependencies.Output("home-row-link", 'children'),
              [dash.dependencies.Input('none', 'children')])
def display_links(none):
    user = session["user"]
    views = [
            {"name":"Admin", "path":"admin"},
            #{"name":"Virus", "path":"virus"},
            {"name":"Tests", "path":"tests"}, {"name":"MEM", "path":"mem"}, {"name":"JJ", "path":"jj"}
            ]

    links = [utils.link_format(view["name"], view["path"]) for view in views if view["path"] in user["usuario_vistas"]]
    links = list(links)
    return links

if __name__ == '__main__':
    #app.run_server(debug=True)
    serve(server, host="0.0.0.0", port=8050)
