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


def create_data_table(df, id, rows=30):
    df = df.astype(str)
    df = df.replace("None", "")
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
        'maxWidth': 150,
        'minWidth': 90,
        "fontSize":"11px"
        },
        style_header={'whiteSpace': 'normal', 'fontWeight': 'bold', "fontSize":"12px", 'backgroundColor': 'rgb(230, 230, 230)', 'height': 'auto'},
        #style_table={'height': 'auto', 'max-height':'auto'},
        #editable=True,
        filter_action="native",
        #column_selectable="multi",
        #row_selectable="multi",
        #row_deletable=True,
        #page_action="native",
        #fixed_rows={"headers": True},
        #fixed_columns={'headers': True, 'data': 1},
        export_format="csv",
        #tooltip_data=[{column: {'value': str(value), 'type': 'markdown'}
        #                for column, value in row.items()}
        #                    for row in df.to_dict('records')
        #            ],
        #tooltip_duration=None,
        style_cell_conditional=[
                                {
                                'if': {'column_id': c},
                                'display': 'none'
                                } for c in ['id']
                                ]
    )
    return table
