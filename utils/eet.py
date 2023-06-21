import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, ctx
from dash.dependencies import Input, Output, State, MATCH, ALL
from flask import request, session
from utils import utils_SQL, utils_requests_bugs, utils_eet, utils
import os
import bcrypt
import pandas as pd
import redshift_connector
from datetime import datetime, date

def serve_layout():

    layout = html.Div(
                        [
                        dbc.Row(
                                    [
                                        html.H1(
                                                "Entegra Exclusion Tracker"
                                                , id="title-eet"
                                                , className="title"
                                                , style={"color":"#1b2b58", "font-size":"28px"}
                                                )
                                    ]
                                    , justify = 'center'
                                    , style={"margin-top":"2%", "margin-bottom":"5%"}
                                )
                        , utils_requests_bugs.requests_bugs
                        , dcc.Store(
                                    id='store-report_type-eet'
                                    , data={
                                              "entegra_exclusion_extended": "Entegra Exclusion Extended",
                                              "entegra_exclusion_segment": "Entegra Exclusion Segment",
                                            }
                                )
                        , dcc.Store(
                                    id='store-dict_cols_group-eet'
                                    , data=utils_eet.dict_cols_group()
                                )
                        , dcc.Store(
                                    id='store-dict_cols_detail-eet'
                                    , data=utils_eet.dict_cols_detail()
                                )
                        , dbc.Row(
                                    id="row-report_type-eet"
                                    , style = {"paddingTop":"30px"}
                                )
                        , dcc.Loading(
                                    dbc.Row(
                                                id="row-report_columns_filter-eet"
                                                , style={"paddingTop":"30px"}
                                            )
                                    )
                        , dcc.Loading(
                                    dbc.Row(
                                                id="row-report_column_filters-eet"
                                                , style={"paddingTop":"30px"}
                                            )
                                    )
                        , dbc.Row(
                                    id="row-btn_run-eet"
                                    , style = {"paddingTop":"10px"}
                                )
                        , dcc.Loading(
                                    dbc.Row(
                                                id="row-table_result-eet"
                                                , style = {"paddingTop":"10px", "overflow":"auto"}
                                            )
                                    )
                        ]
                        , className = "dash-inside-container"
                        , style = {"margin-bottom":"100px"}
                    )
    return layout

def init_callbacks(dash_app):
    @dash_app.callback(
                        Output('row-report_type-eet', 'children')
                        , Input('title-eet', 'children')
                        , State('store-report_type-eet', 'data')
                        )
    def select_filters(title, report_type):
        report_type_options = [{"value":x, "label":report_type[x]} for x in report_type]
        select_report_type = [
                            dbc.Col(
                                    [
                                        html.H5("Please select your report")
                                        , utils_eet.dropdown(
                                                                id="dropdown-report_type-eet"
                                                                , options=list(report_type_options)
                                                                , value=None
                                                                , placeholder="Select Report Type"
                                                                , multi=False
                                                            )
                                    ]
                                    , lg=4
                                    , md=6
                                    , sm=8
                                    )
                            ]

        return select_report_type

    @dash_app.callback(
                        Output('row-report_columns_filter-eet', 'children')
                        , Input("dropdown-report_type-eet", 'value')
                        , State('store-dict_cols_group-eet', 'data')
                        , State('store-dict_cols_detail-eet', 'data')
                        )
    def select_columns_filter(report_type, dict_cols_group, dict_cols_detail):

        if report_type==[] or report_type is None: return "Please select the report type."

        dict_cols_group.update(dict_cols_detail)
        dict_cols = dict_cols_group
        cols_options = [{"value":col, "label":dict_cols[col]} for col in dict_cols]

        select_columns_filter = [
                                    dbc.Col(
                                            [
                                                html.H5("Select columns to filter")
                                                , utils_eet.dropdown(
                                                                        id="dropdown-select_columns_filter-eet"
                                                                        , options=list(cols_options)
                                                                        , value=[]
                                                                        , placeholder="Select Columns"
                                                                        , multi=True
                                                                    )
                                            ]
                                            , lg=4
                                            , md=6
                                            , sm=8
                                            )
                                    , dbc.Col(
                                            [
                                                html.Button(
                                                            f"Select columns"
                                                            , id=f"btn-select_columns_filter-eet"
                                                            , n_clicks=0
                                                            )
                                            ]
                                            , lg=3
                                            , md=4
                                            , sm=4
                                            )
                                ]
        return select_columns_filter

    @dash_app.callback(
                        Output('row-report_column_filters-eet', 'children')
                        , Input('btn-select_columns_filter-eet', 'n_clicks')
                        , State('dropdown-select_columns_filter-eet', 'value')
                        , State('store-dict_cols_group-eet', 'data')
                        , State('store-dict_cols_detail-eet', 'data')
                        , State('dropdown-report_type-eet', 'value')
                        )
    def selects_filters(n_clicks, select_columns_filter, dict_cols_group, dict_cols_detail, report_type):
        print("start selects_filters")
        if n_clicks==0: return None
        if select_columns_filter is None: return "Please select the columns to filter"
        elif len(select_columns_filter)==0: return "Please select the columns to filter"

        dict_cols_group.update(dict_cols_detail)
        dict_cols = dict_cols_group

        filters=[]

        for filter in select_columns_filter:

            if "date" in filter:
                filter_temp = dbc.Col(
                                        [html.Label(dict_cols[filter], style={"width":"100%"})
                                        , dcc.DatePickerRange(
                                                        id={
                                                            "type":f"dateRange-select_filter-eet",
                                                            "index":f"{filter}"
                                                            },
                                                        #min_date_allowed=pastDate,
                                                        max_date_allowed = date.today(),
                                                        initial_visible_month = date.today(),
                                                        style={"width":"100%"}
                                                        )
                                        ]
                                        , lg=4,
                                        md=8,
                                        sm=10,
                                        style={"marginTop":"10px"}
                                        )
                filters.append(filter_temp)
            else:
                df_temp = utils_eet.read_entegra(query=f"select DISTINCT({filter}) FROM entegra_takeback_review.{report_type} order by {filter} asc")

                filter_temp = dbc.Col(
                                        utils_eet.dropdown(
                                                                id={
                                                                    "type":f"dropdown-select_filter-eet",
                                                                    "index":f"{filter}"
                                                                    }
                                                                , options=[{"value":val, "label":val} for val in df_temp[filter].unique()]
                                                                , value=[]
                                                                , placeholder=f"Select {dict_cols[filter]}"
                                                                , multi=True
                                                            )
                                        , lg=4,
                                        md=8,
                                        sm=10,
                                        style={"marginTop":"10px"}
                                        )
                filters.append(filter_temp)

        return filters

    @dash_app.callback(
                        Output('row-btn_run-eet', 'children')
                        , Input({'type': 'dropdown-select_filter-eet', 'index': ALL}, 'value')
                        , Input({'type': 'dateRange-select_filter-eet', 'index': ALL}, 'start_date')
                        , Input({'type': 'dateRange-select_filter-eet', 'index': ALL}, 'end_date')
                        #, State('dropdown-select_filters-eet', 'value')
                        )
    def select_filters(filters, date_filters_start, date_filters_end):
        print("start select_filters")
        print("date_filters_start", date_filters_start)
        if utils.verify_empty_selects(filters+date_filters_start+date_filters_end): return None
        #empty_filters = [[] for i in all_filters]
        #print("filters+date_filters_start", filters+date_filters_start)
        #print("empty_filters", empty_filters)
        #if filters+date_filters_start == empty_filters: return None

        return html.Button(
                                    f"Get data"
                                    , id=f"btn-run_query-eet"
                                    , n_clicks=0
                                    , style={"marginTop":"10px"}
                                )



    @dash_app.callback(
                        Output('row-table_result-eet', 'children')
                        , Input('btn-run_query-eet', 'n_clicks')
                        , State('dropdown-select_columns_filter-eet', 'value')
                        , State({'type': 'dropdown-select_filter-eet', 'index': ALL}, 'value')
                        , State({'type': 'dropdown-select_filter-eet', 'index': ALL}, 'id')
                        , State({'type': 'dateRange-select_filter-eet', 'index': ALL}, 'start_date')
                        , State({'type': 'dateRange-select_filter-eet', 'index': ALL}, 'end_date')
                        , State({'type': 'dateRange-select_filter-eet', 'index': ALL}, 'id')
                        , State('store-dict_cols_group-eet', 'data')
                        , State('store-dict_cols_detail-eet', 'data')
                        , State('dropdown-report_type-eet', 'value')
                        )
    def selects_filters(n_clicks, filters_columns, filters, filters_id, date_filters_start, date_filters_end, date_filters_id, dict_cols_group, dict_cols_detail, report_type):
        if n_clicks==0: return None
        if utils.verify_empty_selects(filters+date_filters_start+date_filters_end): return None
        if len(filters_columns)!=len(filters)+len(date_filters_start): return "Looks like you need to click the 'Select filters' button"

        dimensions_text = ""
        for dimension in dict_cols_group:
            dimensions_text+=f'''{dimension} as "{dict_cols_group[dimension]}", '''
        for dimension in dict_cols_detail:
            dimensions_text+=f'''{dimension} as "{dict_cols_detail[dimension]}", '''
        dimensions_text = dimensions_text[:-2]
        print("dimensions_text", dimensions_text)

        query=f"select {dimensions_text} from entegra_takeback_review.{report_type} where 1=1 "
        print("query pre filters", query)

        for i in range(len(filters)):
            if filters[i] is not None and len(filters[i])>0:
                column = filters_id[i]["index"]
                print("column", column)
                vals = []
                for val in filters[i]:
                    if type(val) == int or type(val) == float:
                        vals.append(val)
                    else:
                        vals.append(val.replace("'", "''"))
                query+=f'''and {column} in {utils.list_to_where(vals)} '''


        for i in range(len(date_filters_start)):
            if (date_filters_start[i] is None or date_filters_start[i]==[]) and (date_filters_end[i] is None or date_filters_end[i]==[]): pass
            try:
                start_date = date_filters_start[i]
            except:
                start_date = None
            try:
                end_date = date_filters_end[i]
            except:
                end_date = None

            if start_date is None and end_date is None: pass

            column = date_filters_id[i]["index"]
            print("column", column)
            print("end_date", end_date)
            print("end_date is None", end_date is None)
            if end_date is None and start_date is None: pass
            elif end_date is None: query+=f"""and {column} >= '{start_date}' """
            elif start_date is None: query+=f"""and {column} <= '{end_date}' """
            else: query+=f"""and ({column} >= '{start_date}' and {column} <= '{end_date}') """

        print("QUERYYYYYYYYYY")
        print(query)

        df = utils_eet.read_entegra(query=query)
        if df is None: return "Something went wrong, please update and try again."
        if len(df)==0: return "No records found, please change your filters."
        #print(df.head())
        print(df.columns)
        #df[list([measures[x]["label"].lower() for x in measures])] = df[list([measures[x]["label"].lower() for x in measures])].fillna(0).round(2)

        return utils_eet.create_data_table(df, "table-final_result-eet", rows=20)
