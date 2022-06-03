import dash
import dash_bootstrap_components as dbc
from dash import html, ctx
from dash import dcc
from dash.dependencies import Input, Output, State
from flask import request, session, json
from utils import utils_google, utils, utils_jj
import pandas as pd
import requests

df = pd.read_csv("data/data_final.csv")
df_2 = pd.DataFrame(data=[1], columns=["a"])
def serve_layout():

    layout = html.Div([
        html.Div(id='none',children=[],style={'display': 'none'})
#Primera seccion----------------------------------------------------------------------------------------------------------------------------------------------------------
        ,
        html.Div(
            [
                dbc.Row([
                    dbc.Col(
                        html.A((html.Img(className="header-d_img", width=150, src="https://bootcamps-hackspace.digitaliatec.com/wp-content/uploads/2022/06/WhatsApp_Image_2022-06-02_at_8.41.52_PM-removebg-preview.png",alt="La PC de tus sueños a tu alcance | JJ ASAMBLE", title="La PC de tus sueños a tu alcance|JJ ASAMBLE")
                        )), width=8),
                    #html.Li(
                    #    html.A("Home"), style={"display": "block", "color": "white", "text-align": "center", "padding": "14px 16px", "text-decoration": "none", "float": "right"}),
                    #html.Li(
                    #    html.A("News"), style={"display": "block", "color": "white", "text-align": "center", "padding": "14px 16px", "text-decoration": "none", "float": "right"}),
                    #html.Li(
                    #    html.A("Contact"), style={"display": "block", "color": "white", "text-align": "center", "padding": "14px 16px", "text-decoration": "none", "float": "right"}),
                    #html.Li(
                    #    html.A("About"), style={"display": "block", "color": "white", "text-align": "center", "padding": "14px 16px", "text-decoration": "none", "float": "right"}),
                    dbc.Col(
                        html.A("Suscríbete"),
                        style={"margin":"9px 45px 35px 25px", "box-sizing": "border-box","outline-color": "rgb(247, 198, 0)","border": "1px solid black", "box-shadow": "0 2px 8px rgba(0,0,0,.16078)","padding":" 0","max-height":"30px","vertical-align": "center","cursor": "pointer","text-decoration": "none","align-items": "center","background-color": "rgb(247, 198, 0)","border-radius": "8px","box-shadow": "0 2px 8px rgba(0,0,0,.16078)","color": "black","display": "flex","font": "900 11px/1 Noto Sans KR, sans-serif","height": "30px","max-width":"150px", "min-width":"100px", "justify-content": "center","text-transform": "uppercase","width": "87px","font-weight": "700", "margin-top":"auto", "margin-bottom":"auto"}
                        , width=4),
                        ])
                       ],className="header-d"

                       ),

        html.Div(
            [
                dbc.Row(
                        html.Img(
                        src="https://yamoshi.com.pe/img/cms/Images/BANNER%20GRANDE%20(1).png"
                        , style={"maxWidth":"100%", "margin":"0px 0px 30px 0px"}
                        )
                        , justify="center"
                    )
                , dbc.Col([
                    # dbc.Row(
                    #     html.H3('J&J Assemble')
                    #     , justify = 'center'
                    # )
                     dbc.Row(
                        html.P('JJ Asamble te permite configurar paso a paso tu pc gararantizando la compatibilidad de los componentes  y comparar precios de diferentes páginas web. Simplemente elige el tipo de Socket que quieres y nuestro configurador seleccionará los componentes compatibles por ti.')
                        , id="row-jj-initial-description", justify = 'center'
                    )
                    # , dbc.Row(
                    #     html.P('Crea tu pc paso a paso, la compatibilidad del procesador y placa base está garantizada.')
                    #     , justify = 'center'
                    # )
                ])
                , dbc.Row([
                        dbc.Col([
                            dbc.Row(
                                html.Button(
                                    "Según los detalles",
                                    id='btn-detalles', className="btn-select-jj",n_clicks=0, style={"background-color": "rgb(247, 198, 0)","color": "black", "cursor": "pointer","box-shadow": "0px 8px 16px 0px rgba(0,0,0,0.2)"},
                                    title="Aquí podrás armar tu pc con componentes compatibles de acuerdo a tu selección",
                                    )
                                )
                            ]
                            , width=5
                        )
                        , dbc.Col([
                            dbc.Row(
                                html.Button(
                                    "Según el monto",
                                    id='btn-monto', className="btn-select-jj", n_clicks=0,style={"background-color": "rgb(247, 198, 0)","color": "black", "cursor": "pointer", "box-shadow": "0px 8px 16px 0px rgba(0,0,0,0.2)"},
                                    title="Aquí podrás comprar tu pc o laptop de acuerdo a tu presupuesto"
                                    )
                                )
                            ]
                            , width = 5
                        )
                    ]
                , justify = 'center'
                )
            ]
            , style={"display":"inline-block", "maxWidth":"100%"}
        ),
        #Seccion detalles-------------------------------------------------------------------------------------------------------------------------
        html.Div(
            id='div-detalles1'
            ),
        #Seccion monto-----------------------------------------------------------------------------------------------------------------------------
        html.Div(
            id='div-monto'
            )
        ], className = "dash-inside-container", style={"display":"inline-block",  "background-color": "rgb(255, 255, 255)", "margin": "0px"} )
    return layout

#Fin Seccion principal-----------------------------------------------------------------------------------------------------------------------------

#Seccion de detalles y monto

def init_callbacks(dash_app):

    #Callback para boton detalles y monto----------------------------------------------------------------------------------------------------------
    @dash_app.callback(
    [Output('div-detalles1', 'children'), Output('div-monto', 'children')],
    [Input('btn-detalles', 'n_clicks'),Input('btn-monto', 'n_clicks')],
    )
    def abrir_detalles_monto(n_clicks1,n_clicks2):
        print("start abrir_detalles_monto")
        if n_clicks1==0 and n_clicks2==0:
            return None, None
        button_id = ctx.triggered_id
        print(button_id, "button_id")
        if button_id=='btn-detalles':
            return utils_jj.children_detalles, None
        elif button_id=='btn-monto':
            return None,  utils_jj.children_monto

#Callback boton segun detalles-------------------------------------------------------------------------------------------------------------------

    #Callback para los dropdown
    @dash_app.callback(
    Output('row-socket1', 'children'),
    [Input('socket', 'value')],
    )
    def socket(value):
        print("start socket")
        if value is None or value=="" or value==[]:
            return None
        return utils_jj.children_socket(value)

    #Callback para mostrar fitrada la data en la tabla segun cada dropdown---------------------------------------------------------------------------------------

    @dash_app.callback(
    Output('div-tables', 'children'),
    [Input('btn-buscar', 'n_clicks')],
    [
    State('socket', 'value'),
    State('mb_id', 'value'),
    State('cpu_id', 'value'),
    State('ram_id', 'value'),
    State('alm_id', 'value'),
    State('gpu_id', 'value'),
    State('psu_id', 'value'),
    State('case_id', 'value')
    ]
    )
    def abrir_tabla(n_clicks, socket, mb, cpu, ram, alm, gpu, psu, case):
        print("start abrir_tabla")
        if n_clicks==0: return None
        return utils_jj.table_results(socket, mb, cpu, ram, alm, gpu, psu, case)

    #Callback para mostrar los productos seleccionados en una tabla ---------------------------------------------------------------------------------------

    @dash_app.callback(
    Output('div-tabla_2', 'children'),
    Input('table-1', 'data'),
    Input('table-1', 'selected_rows'),
    )
    def tabla_precio_detalles(data, selected_rows):
        print("start tabla_precio_detalles")
        if selected_rows is None: return None
        #print(selected_rows)
        df_data = pd.DataFrame(data)
        df_data = df_data.iloc[selected_rows]
        #print(df_data)
        return utils_jj.create_data_table(df_data,"tabla-precio_detalles", filter_a="none", row_select=None)

    #Callback para mostrarla suma del precio total de los productos elegidos-------------------------------------------------------------------------------------

    @dash_app.callback(
     Output('div-tabla_3','children'),
     Input('table-1', 'data'),
    Input('table-1', 'selected_rows'),
    )
    def tabla_precio_total(data, selected_rows):
        if selected_rows is None: return None
        else:
            print('start tabla-precio_detalles2')
            df_data1 = pd.DataFrame(data)
            df_data1 = df_data1.iloc[selected_rows]
            valor = df_data1['Precio'].astype(float).sum()
            df_suma = pd.DataFrame()
            df_suma['TOTAL']  = [round(valor)]

            return utils_jj.create_data_table(df_suma,"tabla-precio_detalles2", filter_a="none", row_select=None)

#Callback boutton segun monto----------------------------------------------------------------------------------------------------------------------

    #Callbacks para agrandar las imagenes de pc y laptop con un click-------------------------------------------------------------------------------------------

    @dash_app.callback(
     Output('img-pc', 'width'),
    [Input('img-pc', 'n_clicks')]
    )
    def abrir_pc(n_clicks):
        if n_clicks % 2 == 0:
            return 150
        else:
            return 250

    @dash_app.callback(
     Output('img-laptop', 'width'),
    [Input('img-laptop', 'n_clicks')]
    )
    def abrir_pc(n_clicks):
        if n_clicks % 2 == 0:
            return 150
        else:
            return 250

    #Callback para filtrar la data segun el width de las iagenes y el RangeSlider y mostrarlo en una tabla-----------------------------------------------------------------------------------------------------------------------------------------------

    @dash_app.callback(
    Output('div-tables1','children'),
    [
    Input('img-pc','width'),
    Input('img-laptop','width'),
    Input('Precio-slider','value')
    ]
    )
    def tabla_pc(width, width1,value):
        df1 = df[['Tienda','Categoría','Título','Stock','Precio','URL']]
        if width==250 and width1==250:
            return utils_jj.create_data_table(df1[
                (df1.Categoría.isin(['PC','Laptop'])) & (df1['Precio'] >= value[0]) & (df1['Precio'] <= value[1])
                ], id='tabla_pc_laptop')
        elif width==250:
            return utils_jj.create_data_table(df1[
                (df1.Categoría=="PC") & (df1['Precio'] >= value[0]) & (df1['Precio'] <= value[1])
                ], id='tabla_pc_laptop')
        elif width1==250:
            return utils_jj.create_data_table(df1[
                (df1.Categoría=="Laptop") & (df1['Precio'] >= value[0]) & (df1['Precio'] <= value[1])
                ], id='tabla_pc_laptop')
