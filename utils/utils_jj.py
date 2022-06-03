from pickle import LIST
import dash
import dash_bootstrap_components as dbc
from dash import html, ctx
from dash import dcc
from dash.dependencies import Input, Output, State
from flask import request, session, json
from utils import utils_google, utils
import pandas as pd
import requests
from dash import dash_table
#
df = pd.read_csv("data/data_final.csv")
df_2 = pd.DataFrame(data=[1], columns=["a"])

children_detalles=  [
    #Desplegables por categoria
        dbc.Row([
            dbc.Col([
            utils.dropdown(id='socket', className='dropdown', options=[
                                        
                {"value":"LGA1200-10", "label":"LGA1200-10"},
                {"value":"LGA1200-11", "label":"LGA1200-11"},
                {"value":"LGA1700-12", "label":"LGA1700-12"},
                {"value":"AM4", "label":"AM4"}
                                        
                ], value=None, multi=False, placeholder="Socket")

            ],
            width=4,
            className="input-col"
            ) 
        ],
            className="inputs-row",
        ),
        html.Div(
        id='row-socket1',
            className="inputs-row",
        )
    ]


def children_socket(socket):
    print('START SOCKET')
    df_temp = df[df["Socket"]==socket]

    print('START OPTIONS')
    options_mb = [{"value":x, "label":"all"} for x in list(df_temp[df_temp.Categoría=="MB"].Generación.dropna().unique())]
    options_procesador = [{"value":x, "label":x} for x in list(df_temp[df_temp.Categoría=="CPU"].Generación.dropna().unique())]
    options_ram = [{"value":x, "label":x} for x in list(df[df.Categoría=="RAM"].Capacidad.dropna().unique())]
    options_almacenamiento = [{"value":x, "label":x} for x in list(df[df.Categoría=="Almacenamiento"].Capacidad.dropna().unique())]
    options_tarjeta = [{"value":x, "label":x} for x in list(df[df.Categoría=="GPU"].Capacidad.dropna().unique())]
    options_psu = [{"value":x, "label":x} for x in list(df[df.Categoría=="PSU"].Capacidad.dropna().unique())]
    options_case = [{"value":x, "label":x} for x in list(df[df.Categoría=="Case"].Generación.dropna().unique())]
    children_socket = [
                    dbc.Row([
                        dbc.Col([
                        utils.dropdown(id='mb_id', className='dropdown', options=options_mb,
                                    value=None, multi=False, placeholder="Motherboard")
                                ], width=4, className="input-col"),

                        dbc.Col([
                        utils.dropdown(id='cpu_id', className='dropdown', options=options_procesador,
                                   value=None, multi=False, placeholder="Procesador")
                                ], width=4, className="input-col"),

                        dbc.Col([
                        utils.dropdown(id='ram_id', className='dropdown', options=options_ram,
                                        value=None, multi=False, placeholder="Memoria Ram")
                                ],width=4,className="input-col"),

                        dbc.Col([
                        utils.dropdown(id='alm_id', className='dropdown', options=options_almacenamiento,
                                    value=None, multi=False, placeholder="Almacenamiento")
                                ],width=4,className="input-col"),

                        dbc.Col([
                        utils.dropdown(id='gpu_id', className='dropdown', options=options_tarjeta
                        ,           value=None, multi=False, placeholder="Tarjeta de Video")
                                ],width=4,className="input-col"),
                                
                        dbc.Col([
                        utils.dropdown(id='psu_id', className='dropdown', options=options_psu
                        ,           value=None, multi=False, placeholder="Fuente de poder")
                            ],width=4,className="input-col"),

                        dbc.Col([
                        utils.dropdown(id='case_id', className='dropdown', options=options_case,
                        value=None, multi=False, placeholder="Case")
                        ], width=4, className="input-col"),
                        #Boton buscar
                        dbc.Col([
                        dbc.Row(
                            html.Button(
                                "Buscar",
                                id='btn-buscar',n_clicks=0, style={"cursor": "pointer", "background-color": "rgb(247, 198, 0)","color": "black","margin": "15px 80px 15px 0px", "box-shadow": "0px 8px 16px 0px rgba(0,0,0,0.2)"}
                                )
                            )
                        ],id='col-buscar',width=4,className="input-col"),
                        ],justify = 'center', style={"min-height": "85px", "margin": "15px 80px 15px 0px",  "padding": "0"}),
                        

                        #Tablas de seccion detalles
                        html.Div(
                            id="div-tables"),
                        ]
                    
    return children_socket

def table_results(socket, mb, cpu, ram, alm, gpu, psu, case):
    df_temp = df[df["Socket"]==socket]
    df_mb = df_temp[(df_temp["Categoría"]=="MB") & (df_temp["Generación"]==mb)]
    df_procesadores = df_temp[(df_temp["Categoría"]=="CPU") & (df_temp["Generación"]==cpu)]
    df_ram = df[(df["Categoría"]=="RAM") & (df["Capacidad"]==ram)]
    df_alm = df[(df["Categoría"]=="Almacenamiento") & (df["Capacidad"]==alm)]
    df_gpu = df[(df["Categoría"]=="GPU") & (df["Capacidad"]==gpu)]
    df_psu = df[(df["Categoría"]=="PSU") & (df["Capacidad"]==psu)]
    df_case = df[(df["Categoría"]=="Case") & (df["Generación"]==case)]
    df_final = pd.concat([df_mb,df_procesadores,df_ram,df_alm,df_gpu,df_psu,df_case])         
    children_table= [
        dbc.Row([html.Div(create_data_table(df_final,'table-1'))],id="tabla_1", style={"overflowX":"auto"}),
            #Tabla de presupuesto     
        dbc.Row([html.Div(id="div-tabla_2")]),  
        dbc.Row([html.Div(id="div-tabla_3")])
        ]
    return children_table


children_monto=[
    dbc.Row([
        html.Div(
            html.Img(
                src="https://cdn-icons-png.flaticon.com/512/3515/3515293.png"
                ,id='img-pc',n_clicks=0, width=150
                ), style={"marginLeft":"auto", "marginRight":"auto", "margin":"30px 0px 40px 0px", "cursor": "pointer"},
                title="Pulsa para elegir tu PC"
            ),
        #Imagen CyC    
        html.Div(
            html.Img(
                src="https://cdn-icons-png.flaticon.com/512/3616/3616913.png"
                ,id='img-laptop',n_clicks=0, width=150
                ), style={"marginLeft":"auto", "marginRight":"auto", "margin":"30px 0px 30px 0px", "cursor": "pointer"},
                title="Pulsa para elegir tu Laptop"
                ),  
    ]),       
    #Despegable de precio maximo     
    dbc.Row([
        dbc.Col([
        dcc.RangeSlider(id='Precio-slider',
                    min=1000,
                    max=8000,
                    value=[1000,8000],step=1000,tooltip={"placement": "bottom", "always_visible": True},
                    allowCross=False
                    )
        ],
        width=6,
        className="input-col"
        ),
    ],justify = 'center'),
    html.Div(id="div-tables1")]   



def create_data_table(df, id, rows=20,filter_a="native",row_select="multi"): #filter_a="native",
    df = df.astype(str)
    df = df.replace("None", "")
    """Create Dash datatable from Pandas DataFrame."""
    table = dash_table.DataTable(
        id=id,
        columns=[
            {'name': i, 'id': i, 'deletable': False} for i in df.columns
            # omit the id column
            if i != 'id'
        ],
        data=df.to_dict('records'),
        sort_action="native",
        sort_mode='multi',
        page_size=rows,
        style_cell={
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'maxWidth': 170,
        'minWidth': 170,
        "fontSize":"11px",
        'border': '2px solid black'
        },
        style_data={'color': 'black'},
        style_filter={'backgroundColor': 'white','color': 'black'},
        style_header={'whiteSpace': 'normal', 'fontWeight': 'bold', "fontSize":"12px", "padding-top": "12px", "padding-bottom": "12px", "text-align": "left", "background-color": "rgb(247, 198, 0)", "color": "black", 'height': 'auto','border': '2px solid black'},
        filter_action=filter_a,
        row_selectable=row_select,
        style_cell_conditional=[
                                {
                                'if': {'column_id': c},
                                'display': 'none'
                                } for c in ['id']
                                ]
    )
    return table