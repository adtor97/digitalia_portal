import pandas as pd
from io import StringIO, BytesIO
import dash_bootstrap_components as dbc
from dash import dcc
from dash import dash_table
from dash import html
from utils import utils_google
from flask import render_template, json

def link_format(name, path):
    path = f"/{path}"
    link = dbc.Col(dcc.Link(name,
                    href=path,
                    refresh=True,
                    className="home-link")
            , className="home-col-link")
    return link


def dropdown(id, className='dropdown', options=[], value=[], multi=False, placeholder=""):
    dropdown = html.Div(
                        dcc.Dropdown(id=id,
                                    options=options,
                                    value=value,
                                    placeholder=placeholder,
                                    multi=multi),
                        style={"margin-top":"1%", "margin-left":"3%"}
                        )
    return dropdown


def create_data_table(df, id, rows=30, row_selectable=False):
    df = df.astype(str)
    df = df.replace("None", "").replace('nan','')
    """Create Dash datatable from Pandas DataFrame."""
    table = dash_table.DataTable(
        id=id,
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        sort_action="native",
        sort_mode='multi',
        page_size=rows,
        #virtualization=True,
        #style_cell={"fontSize":"11px", 'whiteSpace': 'normal', 'height':'35px', 'maxHeight': '35px','minWidth': '90px','maxWidth': '150px', 'overflow': 'hidden','textOverflow': 'ellipsis',},
        style_cell={
        #'whiteSpace': 'normal',
        #'height': 'auto',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'maxWidth': 200,
        'minWidth': 90,
        "fontSize":"11px"
        },
        style_header={'whiteSpace': 'normal', 'fontWeight': 'bold', "fontSize":"12px", 'backgroundColor': 'rgb(230, 230, 230)', 'height': 'auto'},
        #style_table={'height': 'auto', 'max-height':'auto'},
        #editable=True,
        filter_action="native",
        #column_selectable="multi",
        row_selectable=row_selectable,
        #selected_rows=[],
        #row_deletable=True,
        #page_action="native",
        #fixed_rows={"headers": True},
        #fixed_columns={'headers': True, 'data': 1},
        export_format="xlsx",
        tooltip_data=[{column: {'value': str(value), 'type': 'markdown'}
                        for column, value in row.items()}
                            for row in df.to_dict('records')
                    ],
        #tooltip_duration=None,
        style_cell_conditional=[
                                {
                                'if': {'column_id': c},
                                'display': 'none'
                                } for c in ['id','Recomendados']
                                ]
    )
    print(table)
    return table

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

def generate_card(value=0, title=None, id=None):
    return dbc.Col(
                    [
                    dbc.Card(
                                [
                                dbc.CardHeader(title),
                                dbc.CardBody(
                                                [
                                                html.P(value, id=f"{id}-value", className="card-value")
                                                ]
                                            ),
                                ],
                                id = id,
                                className="card-dig"
                            )
                    ],
                    #className="div-complete-inrow"
                    )
