import copy
import json
import os
import sys
from datetime import datetime

import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import matplotlib
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go
import pymysql
from colour import Color
from dash.dependencies import Input, Output
from plotly import tools
from sklearn import preprocessing

db_name = "loneliness"
mapbox_access_token = 'pk.eyJ1IjoiYXhlbG1icmlzdG9sIiwiYSI6ImNqdndjdTJqcjF0NTQ0YW1zajltNG9mNmYifQ.9aVhyD9PCBmyPvUO8ObxkA'
# plotly.tools.set_credentials_file(username='axelmbristol', api_key='Gbnf3TETPtRpt1WY0vr2')
WIDTH = '380px'
HEIGHT = '570px'
ZOOM = 4.9
LATITUDE_INIT = 53.5
LONGITUDE_INIT = -2.10
MARKER_CITY_SELECTED_SIZE = 8


def get_traces(conditions, year_list, depression_perc_list, alzheimers_perc_list,
               blood_pressure_perc_list, hypertension_perc_list, diabetes_perc_list,
               cardiovascular_disease_perc_list, insomnia_perc_list, addiction_perc_list, social_anxiety_perc_list,
               loneliness_perc_list, depression_zscore_list, alzheimers_zscore_list, blood_pressure_zscore_list,
               hypertension_zscore_list, diabetes_zscore_list, cardiovascular_disease_zscore_list,
               insomnia_zscore_list, addiction_zscore_list, social_anxiety_zscore_list, loneliness_zscore_list,
               loneills_list, number_of_patients_list):
    traces = []

    if len(conditions) >= 0:
        if 'number_of_patients' in conditions:
            traces.append(go.Bar(
                opacity=0.5,
                x=year_list,
                y=number_of_patients_list,
                showlegend=False,
                marker=dict(
                    color='rgb(31,119,180)',
                ),
                name='number_of_patients'

            ))

        if 'depression_perc' in conditions:
            traces.append(go.Bar(
                x=year_list,
                y=depression_perc_list,
                showlegend=False,
                marker=dict(
                    color='rgb(255,127,14)',
                ),
                name='depression_perc',
            ))

        if 'alzheimers_perc' in conditions:
            traces.append(go.Bar(
                x=year_list,
                y=alzheimers_perc_list,
                showlegend=False,
                marker=dict(
                    color='rgb(44,160,44)',
                ),
                name='alzheimers_perc',
            ))

        if 'blood_pressure_perc' in conditions:
            traces.append(go.Bar(
                x=year_list,
                y=blood_pressure_perc_list,
                showlegend=False,
                marker=dict(
                    color='rgb(214,39,40)',
                ),
                name='blood_pressure_perc'
            ))

        if 'hypertension_perc' in conditions:
            traces.append(go.Bar(
                x=year_list,
                y=hypertension_perc_list,
                showlegend=False,
                marker=dict(
                    color='rgb(148,103,189)',
                ),
                name='hypertension_perc'
            ))

        if 'diabetes_perc' in conditions:
            traces.append(go.Bar(
                x=year_list,
                y=diabetes_perc_list,
                showlegend=False,
                marker=dict(
                    color='rgb(140,86,75)',
                ),
                name='diabetes_perc'
            ))

        if 'cardiovascular_disease_perc' in conditions:
            traces.append(go.Bar(
                x=year_list,
                y=cardiovascular_disease_perc_list,
                showlegend=False,
                marker=dict(
                    color='rgb(227,119,194)',
                ),
                name='cardiovascular_disease_perc'
            ))

        if 'insomnia_perc' in conditions:
            traces.append(go.Bar(
                x=year_list,
                y=insomnia_perc_list,
                showlegend=False,
                marker=dict(
                    color='rgb(127,127,127)',
                ),
                name='insomnia_perc'
            ))

        if 'addiction_perc' in conditions:
            traces.append(go.Bar(
                x=year_list,
                y=addiction_perc_list,
                showlegend=False,
                marker=dict(
                    color='rgb(188,189,34)',
                ),
                name='addiction_perc'
            ))

        if 'social_anxiety_perc' in conditions:
            traces.append(go.Bar(
                x=year_list,
                y=social_anxiety_perc_list,
                showlegend=False,
                marker=dict(
                    color='rgb(23,190,207)',
                ),
                name='social_anxiety_perc'
            ))

        if 'loneliness_perc' in conditions:
            traces.append(go.Bar(
                x=year_list,
                y=loneliness_perc_list,
                showlegend=False,
                marker=dict(
                    color='rgb(31,119,180)',
                ),
                name='loneliness_perc'
            ))

        if 'depression_zscore' in conditions:
            traces.append(go.Bar(
                x=year_list,
                y=depression_zscore_list,
                showlegend=False,
                marker=dict(
                    color='rgb(249,195,96)',
                ),
                name='depression_zscore'
            ))

        if 'alzheimers_zscore' in conditions:
            traces.append(go.Bar(
                x=year_list,
                y=alzheimers_zscore_list,
                showlegend=False,
                marker=dict(
                    color='rgb(165,183,92)',
                ),
                name='alzheimers_zscore'
            ))

        if 'blood_pressure_zscore' in conditions:
            traces.append(go.Bar(
                x=year_list,
                y=blood_pressure_zscore_list,
                showlegend=False,
                marker=dict(
                    color='rgb(92,161,109)',
                ),
                name='blood_pressure_zscore'
            ))

        if 'hypertension_zscore' in conditions:
            traces.append(go.Bar(
                x=year_list,
                y=hypertension_zscore_list,
                showlegend=False,
                marker=dict(
                    color='rgb(36,134,124)',
                ),
                name='hypertension_zscore'
            ))

        if 'diabetes_zscore' in conditions:
            traces.append(go.Bar(
                x=year_list,
                y=diabetes_zscore_list,
                showlegend=False,
                marker=dict(
                    color='rgb(30,103,114)',
                ),
                name='diabetes_zscore'
            ))

        if 'cardiovascular_disease_zscore' in conditions:
            traces.append(go.Bar(
                x=year_list,
                y=cardiovascular_disease_zscore_list,
                showlegend=False,
                marker=dict(
                    color='rgb(47,72,88)',
                ),
                name='cardiovascular_disease_zscore'
            ))

        if 'insomnia_zscore' in conditions:
            traces.append(go.Bar(
                x=year_list,
                y=insomnia_zscore_list,
                showlegend=False,
                marker=dict(
                    color='rgb(60,83,124)',
                ),
                name='insomnia_zscore'
            ))

        if 'addiction_zscore' in conditions:
            traces.append(go.Bar(
                x=year_list,
                y=addiction_zscore_list,
                showlegend=False,
                marker=dict(
                    color='rgb(196,103,145)',
                ),
                name='addiction_zscore'
            ))
        if 'social_anxiety_zscore' in conditions:
            traces.append(go.Bar(
                x=year_list,
                y=social_anxiety_zscore_list,
                showlegend=False,
                marker=dict(
                    color='rgb(169,80,151)',
                ),
                name='social_anxiety_zscore'
            ))
        if 'loneliness_zscore' in conditions:
            traces.append(go.Bar(
                x=year_list,
                y=loneliness_zscore_list,
                showlegend=False,
                marker=dict(
                    color='rgb(223,69,126)',
                ),
                name='loneliness_zscore'
            ))

        if 'loneills' in conditions:
            traces.append(go.Bar(
                x=year_list,
                y=loneills_list,
                showlegend=False,
                marker=dict(
                    color='rgb(255,80,80)',
                ),
                name='loneills'
            ))

    # if 'loneills' in conditions and len(conditions) == 1:
    #     traces.append(go.Bar(
    #         x=year_list,
    #         y=[abs(x) for x in depression_zscore_list],
    #         showlegend=False,
    #         marker=dict(
    #             color='rgb(255,200,14)',
    #         ),
    #         name='depression_zscore'
    #     ))
    #     traces.append(go.Bar(
    #         x=year_list,
    #         y=[abs(x) for x in alzheimers_zscore_list],
    #         showlegend=False,
    #         marker=dict(
    #             color='rgb(44,160,44)',
    #         ),
    #         name='alzheimers_zscore'
    #     ))
    #     traces.append(go.Bar(
    #         x=year_list,
    #         y=[abs(x) for x in hypertension_zscore_list],
    #         showlegend=False,
    #         marker=dict(
    #             color='rgb(148,103,189)',
    #         ),
    #         name='hypertension_zscore'
    #     ))
    #     traces.append(go.Bar(
    #         x=year_list,
    #         y=[abs(x) for x in insomnia_zscore_list],
    #         showlegend=False,
    #         marker=dict(
    #             color='rgb(127,127,127)',
    #         ),
    #         name='insomnia_zscore'
    #     ))
    #     traces.append(go.Bar(
    #         x=year_list,
    #         y=[abs(x) for x in addiction_zscore_list],
    #         showlegend=False,
    #         marker=dict(
    #             color='rgb(189,189,34)',
    #         ),
    #         name='addiction_zscore'
    #     ))
    #     traces.append(go.Bar(
    #         x=year_list,
    #         y=[abs(x) for x in social_anxiety_zscore_list],
    #         showlegend=False,
    #         marker=dict(
    #             color='rgb(23,190,207)',
    #         ),
    #         name='social_anxiety_zscore'
    #     ))
    return traces


def execute_sql_query(query, records=None, log_enabled=False):
    print(query)
    try:
        sql_db = connect_to_sql_database(db_name=db_name)
        cursor = sql_db.cursor()
        if records is not None:
            print("SQL Query: %s" % query, records)
            cursor.executemany(query, records)
        else:
            if log_enabled:
                print("SQL Query: %s" % query)
            cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            if log_enabled:
                print("SQL Answer: %s" % row)
        return rows
    except Exception as e:
        print("Exeception occured:{}".format(e))


def connect_to_sql_database(db_server_name="localhost", db_user="axel", db_password="@2015", db_name="",
                            char_set="utf8mb4", cusror_type=pymysql.cursors.DictCursor):
    # print("connecting to db %s..." % db_name)
    sql_db = pymysql.connect(host=db_server_name, user=db_user, password=db_password,
                             db=db_name, charset=char_set, cursorclass=cusror_type)
    return sql_db


def get_side_by_side_div(div_l, div_r, year_text_color='dimgray'):
    return html.Div([

        html.Div([div_l,
                  html.Big(
                      id='label-2016',
                      children="2016",
                      style={'color': year_text_color, 'margin-top': '-40px', 'margin-left': '10px', 'height': '30px', 'background-color':'transparent', 'float':'left', 'z-index': '-1', 'position': 'absolute'})
                     ,
                  html.Big(
                      id='label-2017',
                      children="2017",
                      style={'color': year_text_color,'margin-top': '-40px', 'margin-left': '400px', 'height': '30px',
                             'background-color': 'transparent', 'float': 'left', 'z-index': '-1',
                             'position': 'absolute'})
                     ,
                  html.Big(
                      id='label-2018',
                      children="2018",
                      style={'color': year_text_color,'margin-top': '-40px', 'margin-left': '790px', 'height': '30px',
                             'background-color': 'transparent', 'float': 'left', 'z-index': '-1',
                             'position': 'absolute'})

                  ]
                 ,
                 style={'height': '500px', 'width': '1160px', 'float': 'left'}),

        html.Div([div_r], style={'height': '500px', 'width': '300px', 'float': 'right', 'margin-right': '450px', 'margin-top': '37px'})
    ], id='side-by-side',
        style={'height': '500px', 'width': '1920px', 'margin-bottom': '0px', 'margin-top': '100px'})


def build_graphs_layout():

    return html.Div([
        get_side_by_side_div(
            html.Div([
                html.Div([
                    dcc.Graph(
                        figure=go.Figure(
                            data=[
                                go.Scattermapbox(
                                    lat=['53.350140'],
                                    lon=['-6.266155'],
                                    mode='markers',
                                    marker=go.scattermapbox.Marker(
                                        size=14,
                                        opacity=0.0
                                    ),
                                    text=[''],
                                ),
                            ],
                            layout=go.Layout(
                                title='2016',
                                margin=go.layout.Margin(l=0, r=0, t=0, b=0),
                                autosize=True,
                                hovermode='closest',
                                mapbox=go.layout.Mapbox(
                                    accesstoken=mapbox_access_token,
                                    bearing=0,
                                    center=go.layout.mapbox.Center(
                                        lat=LATITUDE_INIT,
                                        lon=LONGITUDE_INIT
                                    ),
                                    pitch=0,
                                    zoom=ZOOM
                                ),
                            )
                        ),
                        style={'height': HEIGHT, 'visibility': 'visible'},
                        id='map-2016',
                        config={
                            'displayModeBar': False
                        }
                    )], style={'margin-right': '8px', 'height': HEIGHT, 'width': WIDTH, 'background-color': 'red', 'display': 'inline-block'}),
                html.Div([
                    dcc.Graph(
                        figure=go.Figure(
                            data=[
                                go.Scattermapbox(
                                    lat=['53.350140'],
                                    lon=['-6.266155'],
                                    mode='markers',
                                    marker=go.scattermapbox.Marker(
                                        size=14,
                                        opacity=0.0
                                    ),
                                    text=[''],
                                ),
                            ],
                            layout=go.Layout(
                                margin=go.layout.Margin(l=0, r=0, t=0, b=0),
                                autosize=True,
                                hovermode='closest',
                                mapbox=go.layout.Mapbox(
                                    accesstoken=mapbox_access_token,
                                    bearing=0,
                                    center=go.layout.mapbox.Center(
                                        lat=LATITUDE_INIT,
                                        lon=LONGITUDE_INIT
                                    ),
                                    pitch=0,
                                    zoom=ZOOM
                                ),
                            )
                        ),
                        style={'height': HEIGHT, 'visibility': 'visible'},
                        id='map-2017',
                        config={
                            'displayModeBar': False
                        }
                    )], style={'margin-right': '8px', 'height': HEIGHT, 'width': WIDTH, 'background-color': 'blue', 'display': 'inline-block'}),
                html.Div([
                    dcc.Graph(
                        figure=go.Figure(
                            data=[
                                go.Scattermapbox(
                                    lat=['53.350140'],
                                    lon=['-6.266155'],
                                    mode='markers',
                                    marker=go.scattermapbox.Marker(
                                        size=14,
                                        opacity=0.0
                                    ),
                                    text=[''],
                                ),
                            ],
                            layout=go.Layout(
                                margin=go.layout.Margin(l=0, r=0, t=0, b=0),
                                autosize=True,
                                hovermode='closest',
                                mapbox=go.layout.Mapbox(
                                    accesstoken=mapbox_access_token,
                                    bearing=0,
                                    center=go.layout.mapbox.Center(
                                        lat=LATITUDE_INIT,
                                        lon=LONGITUDE_INIT
                                    ),
                                    pitch=0,
                                    zoom=ZOOM
                                ),
                            )
                        ),
                        style={'height': HEIGHT, 'visibility': 'visible'},
                        id='map-2018',
                        config={
                            'displayModeBar': False
                        }
                    )
                ], style={'height': HEIGHT, 'width': WIDTH, 'background-color': 'green', 'display': 'inline-block'})
            ])
            ,
            html.Div([
                dcc.Graph(
                    figure=go.Figure(
                        data=[
                            go.Scatter(
                                x=[],
                                y=[],
                                name='',
                            )
                        ],
                        layout=go.Layout(
                            margin=go.layout.Margin(l=0, r=0, t=0, b=0),
                            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=10, width=10
                        )
                    ),
                    style={'height': '680px', 'visibility': 'visible', 'padding-top': '0px'},
                    id='detail-graph',
                    # config={
                    #     'displayModeBar': True
                    # }
                )
            ],
                style={'height': '680px', 'visibility': 'visible', 'margin-top': '-70px', 'background-color': 'transparent'},
                id='city-figures'
            ),
        )

    ], style={'background-color': 'transparent', 'margin-top': '50px', 'max-width': '1920px', 'min-width': '1920px'})


def build_dashboard_layout(city_names):
    return html.Div([
        html.Div([html.Pre(id='relayout-data-last-config', style={'display': 'none'})]),
        html.Div([
            html.Img(id='logo', style={'width': '277px', 'height': '77px', 'margin-right': '20px', 'margin-top': '10px', 'margin-left': '10px'},
                     src='http://dof4zo1o53v4w.cloudfront.net/s3fs-public/styles/logo/public/logos/university-of-bristol'
                         '-logo.png?itok=V80d7RFe'),
            html.Img(id='logo-2', style={'width': '240px', 'height': '67px', 'margin-right': '20px', 'margin-top': '10px', 'background-color': 'transparent'},
                     src='https://www.statisticsauthority.gov.uk/wp-content/uploads/2018/11/DSC_LOGO_RGB_FULL_COLOUR_300_DPI.png'),
            html.Img(id='logo-4', style={'width': '117px', 'height': '77px', 'margin-right': '20px'},
                     src='https://upload.wikimedia.org/wikipedia/commons/d/dc/DCMS_logo_1.png'),
            html.Img(id='logo-3', style={'width': '140px', 'height': '77px', 'margin-right': '20px'},
                     src='https://upload.wikimedia.org/wikipedia/en/thumb/6/68/Department_for_Education.svg/1200px-Department_for_Education.svg.png'),
        ], style={'width': '1920px', 'height': '87px', 'margin-bottom': '-20px', 'background-color': 'transparent'}),


        html.Div(id='dropdown-data-city', style={'display': 'none'}),
        html.Br(),
        html.Big(
            children="Loneliness Data challenge. This work was undertaken as part of a data challenge organised by the"
                     " Jean Golding Institute for Data-Intensive Research at the University of Bristol and ONS. "
                     "Data Science Campus,",
            style={'margin-left': '10px'}),
        # html.Br(),
        # html.Big(
        #     children="Department for Culture Media & Sport, Department for Education, "
        #              "Jean Golding Institute.",
        #     style={'margin-left': '10px'}),
        html.Br(),
        html.Br(),
        # html.B(id='farm-title'),
        html.Div([html.Pre(id='relayout-data', style={'display': 'none'})]),

        html.Div([
            html.Div([
                html.Div([
                    html.Div([html.Big('City selection:'),
                              html.Button('RESET', id='button', style={'border-color': 'transparent','margin-left':
                                  '220px', 'width': '0px', 'height': '0px', 'margin-top': '-10px'}),
                              dcc.Dropdown(
                                  id='city-dropdown',
                                  multi=True,
                                  options=format_for_dropdown(city_names),
                                  value=['Bristol, City of BS10 6AF, United Kingdom', 'City of London EC1A 7HF, United Kingdom'],
                                  placeholder="Select city...",
                                  style={'width': '400px', 'font-weight': 'bold'}
                              )],
                             style={'width': '570px', 'margin-left': '10px',
                                    'autocomplete': 'off'}),

                    html.Div([
                        html.Div([html.Big('Student domicile:'),
                                  dcc.Dropdown(
                                      id='domicile-dropdown',
                                      multi=False,
                                      options=format_for_dropdown(domiciles),
                                      placeholder="Select domicile...",
                                      style={'width': '180px', 'font-weight': 'bold', }
                                  )],
                                 style={'width': '180px', 'margin-left': '10px', 'display': 'inline-block'}),

                        html.Div([html.Big('Study level:'),
                                  dcc.Dropdown(
                                      id='study-level-dropdown',
                                      multi=False,
                                      options=format_for_dropdown(study_levels),
                                      placeholder="Level...",
                                      style={'width': '100px', 'font-weight': 'bold'}
                                  )],
                                 style={'width': '100px', 'margin-left': '10px', 'display': 'inline-block'}),
                        html.Div([html.Big('Study mode:'),
                                  dcc.Dropdown(
                                      id='study-mode-dropdown',
                                      multi=False,
                                      options=format_for_dropdown(study_modes),
                                      placeholder="Mode...",
                                      style={'width': '100px', 'font-weight': 'bold'}
                                  )],
                                 style={'width': '110px', 'margin-left': '10px', 'display': 'inline-block'})
                    ],
                        style={'width': '460px', 'margin-left': '0px', 'background-color': 'gray'}),


                    dcc.Checklist(
                        id='normalize-checkbox',
                        options=[
                            {'label': 'Enable normalization of map data', 'value': 'enabled'},
                        ],
                        values=[],
                        labelStyle={'display': 'inline-block'},
                        style={'margin-top': '10px', 'height': '20px', 'min-width': '100px', 'margin-left': '10px',
                               'color': 'white', 'background-color': 'gray',
                               'font-weight': 'bold', 'display': 'none'}
                    ),

                    html.Big(
                        id='label-c-mapping',
                        children="Enable Choropleth Mapping:",
                        style={'margin-bottom': '0px','margin-left': '10px'})
                    ,
                    html.Div([
                        daq.BooleanSwitch(
                            id='choropleth-mode-lowres-checkbox',
                            on=False,
                            color='rgb(171, 226, 251)',
                            label='Regions',
                            labelPosition='right',
                            style={'margin-top': '0px', 'height': '30px', 'width': '110px', 'margin-left': '10px',
                                   'color': 'white', 'background-color': 'gray',
                                   'font-weight': 'bold', 'float': 'left'}
                        ),
                        daq.BooleanSwitch(
                            id='choropleth-mode-highres-checkbox',
                            on=False,
                            color='rgb(171, 226, 251)',
                            label='Counties',
                            labelPosition='right',
                            style={'margin-top': '0px', 'height': '30px', 'width': '110px', 'margin-left': '130px',
                                   'color': 'white', 'background-color': 'gray',
                                   'font-weight': 'bold'}
                        )
                    ], style={'margin-top': '-3px', 'height': '30px', 'width': '270px', 'margin-left': '0px', 'background-color': 'gray'}
                    ),

                    daq.BooleanSwitch(
                        id='dark-mode-checkbox',
                        on=True,
                        color='rgb(171, 226, 251)',
                        label='Enable Dark Mode',
                        labelPosition='right',
                        style={'margin-top': '5px', 'margin-bottom': '15px', 'height': '20px', 'width': '180px',
                               'margin-left': '8px',
                               'color': 'white', 'background-color': 'gray',
                               'font-weight': 'bold'}
                    ),


                ], style={'float': 'left'}),
                html.Div([
                    html.Big('Select conditions of interest for selected city. (z-score of prescriptions by GP for condition, by global mean and standard deviation):'),
                    html.Div([
                        dcc.Checklist(
                            id='condition-checkbox',
                            options=[
                                {'label': 'Loneliness', 'value': 'loneills'},
                                # {'label': 'loneliness perc ', 'value': 'loneliness_perc'},
                                {'label': 'Social anxiety', 'value': 'social_anxiety_zscore'},
                                # {'label': 'social anxiety perc ', 'value': 'social_anxiety_perc'},
                                {'label': 'Depression', 'value': 'depression_zscore'},
                                # {'label': 'depression perc ', 'value': 'depression_perc'},
                                {'label': 'Addiction', 'value': 'addiction_zscore'},
                                # {'label': 'addiction perc ', 'value': 'addiction_perc'},
                                {'label': 'Insomnia', 'value': 'insomnia_zscore'},
                                # {'label': 'insomnia perc ', 'value': 'insomnia_perc'},
                                {'label': 'Cardiovascular disease', 'value': 'cardiovascular_disease_zscore'},
                                # {'label': 'cardiovascular disease perc ', 'value': 'cardiovascular_disease_perc'},
                                {'label': 'Diabetes', 'value': 'diabetes_zscore'},
                                # {'label': 'diabetes perc ', 'value': 'diabetes_perc'},
                                {'label': 'Hypertension', 'value': 'hypertension_zscore'},
                                # {'label': 'hypertension perc ', 'value': 'hypertension_perc'},
                                {'label': 'Blood pressure', 'value': 'blood_pressure_zscore'},
                                # {'label': 'blood pressure perc ', 'value': 'blood_pressure_perc'},
                                {'label': 'Alzheimers', 'value': 'alzheimers_zscore'},
                                # {'label': 'alzheimers perc ', 'value': 'alzheimers_perc'},
                                {'label': 'Number of patients ', 'value': 'number_of_patients'}
                            ],
                            values=[],
                            labelStyle={'display': 'inline-block'},
                            style={'margin-top': '0px', 'height': '20px', 'min-width': '100px', 'margin-right': '10px',
                                   'color': 'white', 'background-color': 'gray',
                                   'font-weight': 'bold', 'display': 'inline-block'}
                        )
                        ,
                        dcc.Checklist(
                            id='select-all-checkbox',
                            options=[
                                {'label': 'Select All', 'value': 'enabled'}
                            ],
                            values=[],
                            style={'margin-top': '-50px', 'height': '20px', 'min-width': '100px', 'margin-right': '10px',
                                   'color': 'white', 'background-color': 'gray',
                                   'font-weight': 'bold', 'display': 'inline-block'}
                        ),
                        html.Br(),
                        html.Big('Select conditions of interest for UK map between 2016 and 2018 (z-score of prescriptions by GP for condition, by global mean and standard deviation):'),
                        dcc.RadioItems(
                            id='condition-radio',
                            options=[
                                {'label': 'Loneliness', 'value': 'loneills'},
                                # {'label': 'loneliness perc ', 'value': 'loneliness_perc'},
                                {'label': 'Social anxiety', 'value': 'social_anxiety_zscore'},
                                # {'label': 'social anxiety perc ', 'value': 'social_anxiety_perc'},
                                {'label': 'Depression', 'value': 'depression_zscore'},
                                # {'label': 'depression perc ', 'value': 'depression_perc'},
                                {'label': 'Addiction', 'value': 'addiction_zscore'},
                                # {'label': 'addiction perc ', 'value': 'addiction_perc'},
                                {'label': 'Insomnia', 'value': 'insomnia_zscore'},
                                # {'label': 'insomnia perc ', 'value': 'insomnia_perc'},
                                {'label': 'Cardiovascular disease', 'value': 'cardiovascular_disease_zscore'},
                                # {'label': 'cardiovascular disease perc ', 'value': 'cardiovascular_disease_perc'},
                                {'label': 'Diabetes', 'value': 'diabetes_zscore'},
                                # {'label': 'diabetes perc ', 'value': 'diabetes_perc'},
                                {'label': 'Hypertension', 'value': 'hypertension_zscore'},
                                # {'label': 'hypertension perc ', 'value': 'hypertension_perc'},
                                {'label': 'Blood pressure', 'value': 'blood_pressure_zscore'},
                                # {'label': 'blood pressure perc ', 'value': 'blood_pressure_perc'},
                                {'label': 'Alzheimers', 'value': 'alzheimers_zscore'},
                                # {'label': 'alzheimers perc ', 'value': 'alzheimers_perc'},
                                {'label': 'Number of patients ', 'value': 'number_of_patients'}
                            ],
                            value='loneills',
                            style={'margin-top': '0px', 'height': '20px', 'min-width': '100px',
                                   'margin-right': '10px',
                                   'color': 'white', 'background-color': 'gray',
                                   'font-weight': 'bold', 'display': 'inline-block'},
                            labelStyle={'display': 'inline-block'}
                        )
                    ],
                        style={'margin-bottom': '30px', 'margin-left': '0px', 'width': '1220px', 'background-color': 'transparent',
                               'display': 'inline-block'}
                    ),
                ],
                    style={'margin-left': '-130px', 'display': 'inline-block', 'width': '1100px', 'height': '135px',
                           'background-color': 'gray',
                           'margin-bottom': '0px'}
                )


            ], id='dashboard', style={'width': '100%', 'height': '228px', 'display': 'inline-block', 'background-color': 'gray'})
        ], style={'margin-top': '-20px', 'width': '100%', 'min-width': '1920px', 'background-color': 'gray'}),


    ], style={'min-width': '1920px', 'height': '257px', 'width': '100%', 'background-color': 'gray', 'margin-bottom': '0px'})


def format_for_dropdown(input):
    result = []
    input.sort()
    for elem in input:

        result.append({'label': 'United Kingdom' if elem == 'United Kingdom,' else elem.replace('United Kingdom', '')
                      .replace(",", '')
                      .replace('City of ', '')
                      .replace('"', '')
                      .replace(' and St. Damian in the Blean ', '')
                      .replace(' and Hawley ', '')
                      .replace(' with Towthorpe ', '')
                      .replace(' and Malling ', '')
                      .replace(' and Stobswood ', '')
                      .replace('on Thames ', '')
                      .replace(' and Highbridge', '')
                      .replace('postgraduate', 'PG')
                      .replace('Postgraduate', 'PG')
                      .replace('First degree', '1stdegree')
                      .replace(' (research)', 'R')
                      .replace(' (taught)', 'T')
                      .replace('undergraduate', 'UG')

                          , 'value': elem})
    return result


def build_default_app_layout(app, city_names):
    app.layout = html.Div(
        [
            build_dashboard_layout(city_names), build_graphs_layout(),
            html.Small(
                children="Axel Montout, Lucy Vass, Luke McGuinness. 2019.",
                style={'margin-top': '0px', 'width': '100%', 'left': '0px', 'bottom': '0px',
                       'background-color': 'transparent', 'text-align': 'center', 'z-index': '-1', 'position': 'fixed'})
        ], id='main-div',

    )


def get_as_list(key, list_of_dict, laua=None, region=None, clean_city_name=False):
    result = []
    for d in list_of_dict:
        if laua is not None:
            if 'laua' in d and d['laua'] != laua:
                continue
        if region is not None:
            if 'rgn' in d and d['rgn'] != region:
                continue
        if clean_city_name:
            result.append(clean_domicile_name(d[key].replace('"', '')))
        else:
            result.append(d[key])
    return result


def make_city_marker(latitude_list, longitude_list, name_list, data_list, id=None, selected_city=[], normalize=False):
    indexes = []
    latitude_list_selected = []
    longitude_list_selected = []
    print(selected_city)
    for selected in selected_city:
        try:
            idx = name_list.index(selected)
            indexes.append(idx)
            latitude_list_selected.append(latitude_list[idx])
            longitude_list_selected.append(longitude_list[idx])
        except ValueError as e:
            print(e)

    colors = ['rgb(214, 39, 40)' if x > 0 else 'rgb(17, 157, 255)' for x in data_list]
    sizes = []

    if normalize:
        normalizes_size = pd.DataFrame(data_list)
        x = normalizes_size.values  # returns a numpy array
        scaler = preprocessing.StandardScaler()
        x_scaled = scaler.fit_transform(x)
        d = pd.DataFrame(x_scaled) * 1
        s = d.values.flatten().tolist()
        for x in s:
            sizes.append(abs(float(x)))
    else:
        for x in data_list:
            sizes.append(abs(x))

    texts = ["%s %s" % (x, data_list[i]) for i, x in enumerate(name_list)]

    latitude_list.append(16.241100)
    longitude_list.append(-61.533100)
    sizes.append(4)
    colors.append('rgb(0, 255, 0)')
    texts.append('Birth place of Axel.')

    markers_selected_city = go.Scattermapbox(
        lat=latitude_list_selected,
        lon=longitude_list_selected,
        mode='markers',
        marker=go.scattermapbox.Marker(
            symbol='marker',
            size=MARKER_CITY_SELECTED_SIZE,
            opacity=1
        ),
        text=selected_city,
        showlegend=False,
        name=''
    )

    return go.Scattermapbox(
        lat=latitude_list,
        lon=longitude_list,
        mode='markers',
        marker=go.scattermapbox.Marker(
            color=colors,
            size=sizes,
            opacity=0.8
        ),
        text=texts,
        showlegend=False,
        name=''
    ), markers_selected_city


def multipoly_to_polylist2(mpoly):
    # find out how many components are in the Multipoly:
    npoly = len(mpoly['geometry']['coordinates'])

    # create a deep copy of the Multipoly dict:
    temp = copy.deepcopy(mpoly)

    # extract some bits and pieces out of the deep copy:
    plist = []

    # loop through the components and make a list of Polygons:
    for n in range(0, npoly):
        geo_feature = dict(type="Feature")
        geo_feature['properties'] = temp['properties']
        geo_feature['properties']['part'] = str(n)
        geo_feature['geometry'] = dict(type='Polygon')
        geo_feature['geometry']['coordinates'] = temp['geometry']['coordinates'][n]

        # check whether there's more than one polygon - make sure the shape of the coordinate array
        # is correct:
        if (npoly > 1):
            geo_feature['geometry']['coordinates'] = temp['geometry']['coordinates'][n]
        else:
            geo_feature['geometry']['coordinates'] = [temp['geometry']['coordinates'][n]]

        # keep appending each Polygon into the list:
        plist.append(copy.deepcopy(geo_feature))

    return plist


def multipoly_to_polylist(mpoly):
    # find out how many components are in the Multipoly:
    npoly = len(mpoly['features'][0]['geometry']['coordinates'])

    # create a deep copy of the Multipoly dict:
    temp = copy.deepcopy(mpoly)

    # extract some bits and pieces out of the deep copy:
    plist = dict(type="FeatureCollection")
    plist["crs"] = temp["crs"]
    plist["features"] = []

    # loop through the components and make a list of Polygons:
    for n in range(0, npoly):
        geo_feature = dict(type="Feature")
        geo_feature['properties'] = temp['features'][0]['properties']
        geo_feature['properties']['part'] = str(n)
        geo_feature['geometry'] = dict(type='Polygon')

        # check whether there's more than one polygon - make sure the shape of the coordinate array
        # is correct:
        if (npoly > 1):
            geo_feature['geometry']['coordinates'] = temp['features'][0]['geometry']['coordinates'][n]
        else:
            geo_feature['geometry']['coordinates'] = [temp['features'][0]['geometry']['coordinates'][n]]

        # keep appending each Polygon into the list:
        plist['features'].append(copy.deepcopy(geo_feature))

    return plist


def chunks(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]


def get_color_from_value(value, color_gradient, chunked_values):
    gradient = None
    for idx, item in enumerate(chunked_values):
        min_v = min(item)
        max_v = max(item)
        if min_v <= value <= max_v:
            color = color_gradient[idx]
            gradient = matplotlib.colors.cnames[str(color).lower()] if '#' not in str(color) else str(color)
            return gradient


def get_color_from_var(var):
    if var == 'depression_perc':
        return 'orange'
    if var == 'alzheimers_perc':
        return 'green'
    if var == 'blood_pressure_perc':
        return 'red'
    if var == 'hypertension_perc':
        return 'purple'
    if var == 'diabetes_perc':
        return 'brown'
    if var == 'cardiovascular_disease_perc':
        return 'pink'
    if var == 'insomnia_perc':
        return 'gray'
    if var == 'addiction_perc':
        return 'lightgreen'
    if var == 'social_anxiety_perc':
        return 'aqua'
    if var == 'loneliness_perc':
        return 'blue'
    if var == 'depression_zscore':
        return 'yellow'
    if var == 'alzheimers_zscore':
        return 'green'
    if var == 'blood_pressure_zscore':
        return 'red'
    if var == 'hypertension_zscore':
        return 'purple'
    if var == 'diabetes_zscore':
        return 'brown'
    if var == 'cardiovascular_disease_zscore':
        return 'pink'
    if var == 'insomnia_zscore':
        return 'gray'
    if var == 'addiction_zscore':
        return 'lightgreen'
    if var == 'social_anxiety_zscore':
        return 'aqua'
    if var == 'number_of_patients':
        return 'blue'


def build_geojon_migration_line(longitude_dom, latitude_dom, longitude_stu, latitude_stu):
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [longitude_dom, latitude_dom], [longitude_stu, latitude_stu],
                    ]
                },
                "properties": {
                    "prop0": "value0",
                    "prop1": 0.0
                }
            }
        ]
    }


def build_geojon_migration_point(long, lat):
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        [long, lat]
                    ]
                },
                "properties": {
                    "prop0": "value0",
                    "prop1": 0.0
                }
            }
        ]
    }


def process_numer_range(value):
    if 0 <= value <= 10:
        return 10
    if 10 <= value <= 20:
        return 15
    if 20 <= value <= 50:
        return 20
    if 50 <= value <= 100:
        return 25
    if 100 <= value <= 500:
        return 40
    if 500 <= value <= 1000:
        return 45
    if 500 <= value <= 2000:
        return 50
    if 500 <= value <= 20000000:
        return 55


def build_choropleth_map(year, radio, detail_figure, normalize=False, style='basic', high_res=False, domicile=None, level='All', mode='Full-time'):
    sources_migration_lines, sources_migration_points_dom_lat, sources_migration_points_dom_long, \
    sources_migration_points_he_lat, sources_migration_points_he_long, \
    numbers, labels_marker_he = get_migration_data(domicile, year, level, mode)
    selected = []
    try:
        for i in range(0, len(detail_figure['layout']['annotations'])):
            selected.append(detail_figure['layout']['annotations'][i]['text'] + ', United Kingdom')
    except KeyError as e:
        print(e)

    filename = 'Regions_December_2015_Ultra_Generalised_Clipped_Boundaries_in_England.geojson'
    if high_res:
        filename = 'map.geojson'

    with open(filename) as f:
        GEOJSON_DATA = json.load(f)
        flist = GEOJSON_DATA['features']

        sources = []

        for feature in flist:
            plist = multipoly_to_polylist2(feature)
            sources.append({"type": "FeatureCollection", 'features': copy.deepcopy(plist)})
            lons = []
            lats = []
        for k in range(len(sources)):

            # combine (lon,lat) data for all polygons in region:
            npoly = len(sources[k]['features'])
            region_coords = np.array(sources[k]['features'][0]['geometry']['coordinates'][0])
            for j in range(1, npoly):
                tmp = np.array(sources[k]['features'][j]['geometry']['coordinates'][0])
                region_coords = np.vstack((region_coords, tmp))

            if len(region_coords.shape) > 1:
                m, M = region_coords[:, 0].min(), region_coords[:, 0].max()
                lons.append(0.5 * (m + M))
                m, M = region_coords[:, 1].min(), region_coords[:, 1].max()
                lats.append(0.5 * (m + M))
            else:
                m, M = region_coords[0].min(), region_coords[0].max()
                lons.append(0.5 * (m + M))
                m, M = region_coords[1].min(), region_coords[1].max()
                lats.append(0.5 * (m + M))

        facecolour = []
        value_color = []
        labels_he_nut = []

        if not high_res:
            data_list = execute_sql_query('SELECT %s, rgn FROM %s WHERE year="%s"' % (radio, 'final_data', year))
            for p in range(len(sources)):
                region = sources[p]['features'][0]['properties']['rgn15cd']
                region_name = sources[p]['features'][0]['properties']['rgn15nm']
                l = get_as_list(radio, data_list, region=region)
                value = sum(l)/len(l)
                if radio == 'number_of_patients':
                    value = sum(l)

                labels_he_nut.append('%s %.5f' % (region_name, value))
                value_color.append(value)
        else:
            data_list = execute_sql_query('SELECT %s, laua FROM %s WHERE year="%s"' % (radio, 'final_data', year))
            for p in range(len(sources)):
                laua = sources[p]['features'][0]['properties']['lau115cd']
                countie_name = sources[p]['features'][0]['properties']['lau115nm']
                l = get_as_list(radio, data_list, laua=laua)
                value = sum(l) / len(l)
                if radio == 'number_of_patients':
                    value = sum(l)

                labels_he_nut.append('%s %.5f' % (countie_name, value))
                value_color.append(value)
                # todo fix input array
                if laua == 'E07000012':
                    sources[p]['features'][0]['geometry']['coordinates'] = [sources[p]['features'][0]['geometry']['coordinates']]

        if high_res:
            resolution = 20
        else:
            resolution = 1

        all_values_sorted = sorted(value_color)
        all_values_chunked = chunks(all_values_sorted, resolution)

        # color_gradient = list(Color("white").range_to(Color(get_color_from_var(radio)), len(all_values_chunked)))
        # if radio == 'loneills':
        #     color_gradient = list(Color("yellow").range_to(Color("red"), len(all_values_chunked)))
        # if radio == 'loneliness_perc':
        #     color_gradient = list(Color("aqua").range_to(Color("blue"), len(all_values_chunked)))
        legend_color_high = "red"
        legend_color_low = "white"
        if radio == 'loneills':
            color_gradient = list(Color("yellow").range_to(Color("red"), len(all_values_chunked)))
            legend_color_high = 'red'
            legend_color_low = 'yellow'
        if radio == 'social_anxiety_zscore':
            color_gradient = list(Color("white").range_to(Color("red"), len(all_values_chunked)))
            legend_color_high = 'red'
        if radio == 'addiction_zscore':
            color_gradient = list(Color("white").range_to(Color("violet"), len(all_values_chunked)))
            legend_color_high = 'violet'
        if radio == 'insomnia_zscore':
            color_gradient = list(Color("white").range_to(Color("blue"), len(all_values_chunked)))
            legend_color_high = 'blue'
        if radio == 'cardiovascular_disease_zscore':
            color_gradient = list(Color("white").range_to(Color("blue"), len(all_values_chunked)))
            legend_color_high = 'blue'
        if radio == 'diabetes_zscore':
            color_gradient = list(Color("white").range_to(Color("#008080"), len(all_values_chunked)))
            legend_color_high = 'rgb(0,128,128)'
        if radio == 'hypertension_zscore':
            color_gradient = list(Color("white").range_to(Color("#008080"), len(all_values_chunked)))
            legend_color_high = 'rgb(0,128,128)'
        if radio == 'blood_pressure_zscore':
            color_gradient = list(Color("white").range_to(Color("green"), len(all_values_chunked)))
            legend_color_high = 'green'
        if radio == 'alzheimers_zscore':
            color_gradient = list(Color("white").range_to(Color("lightgreen"), len(all_values_chunked)))
            legend_color_high = 'lightgreen'
        if radio == 'depression_zscore':
            color_gradient = list(Color("white").range_to(Color("yellow"), len(all_values_chunked)))
            legend_color_high = 'yellow'
        if radio == 'number_of_patients':
            color_gradient = list(Color("white").range_to(Color("blue"), len(all_values_chunked)))
            legend_color_high = 'blue'

        for value in value_color:
            facecolour.append(get_color_from_value(value, color_gradient, all_values_chunked))
            # facecolour.append(mapped_value[value])

        trace0 = go.Bar(x=[0], y=[0], name='High (max value: %.4f)' % max(value_color), marker=dict(color=legend_color_high))
        trace1 = go.Bar(x=[0], y=[0], name='Low (min value: %.4f)' % min(value_color), marker=dict(color=legend_color_low))

        NUTS1 = dict(type='scattermapbox',
                     lat=lats,
                     lon=lons,
                     mode='markers',
                     text=labels_he_nut,
                     marker=dict(size=1, color='r'),
                     showlegend=False,
                     hoverinfo='text'
                     )
        layers = [dict(sourcetype='geojson',
                       source=sources[k],
                       below="water",
                       type='fill',
                       color=facecolour[k],
                       opacity=1
                       ) for k in range(len(sources))]

        layers_migration_lines = [dict(sourcetype='geojson',
                                       source=sources_migration_lines[k],
                                       type='line',
                                       color='white',
                                       opacity=0.5,
                                       paint={'line-color': 'red', 'line-width': 1, 'line-dasharray': [2, 1]}
                                       ) for k in range(len(sources_migration_lines))]

        layout = dict(font=dict(family='Balto'),
                      margin=go.layout.Margin(l=0, r=0, t=0, b=0),
                      autosize=False,
                      # width=WIDTH,
                      # height=HEIGHT,
                      showlegend=True,
                      legend=dict(
                          x=0,
                          y=1,
                          traceorder='normal',
                          font=dict(
                              family='sans-serif',
                              size=12,
                              color='#ffffff'
                          ),
                          bgcolor='rgb(50, 50, 50)' if style == 'dark' else 'rgb(128, 128, 128)',
                          borderwidth=0
                      ),
                      hovermode='closest',
                      mapbox=dict(accesstoken=mapbox_access_token,
                                  layers=layers + layers_migration_lines,
                                  bearing=0,
                                  center=dict(
                                      lat=LATITUDE_INIT,
                                      lon=LONGITUDE_INIT),
                                  pitch=0,
                                  zoom=4.9,
                                  style=style
                                  )
                      )
        latitude_list_selected = []
        longitude_list_selected = []
        selected_city = []
        for city in selected:
            if 'City of ' in city:
                post_code = ''.join(city.split('City of ')[1].split(',')[0].split(' ')[-2:])
            else:
                post_code = ''.join(city.split(',')[0].split(' ')[-2:])
            data_list = execute_sql_query('SELECT latitude, longitude FROM %s WHERE year="%s" AND pcstrip="%s"'
                                          % ('final_data', year, post_code))
            lat = data_list[0]['latitude']
            long = data_list[0]['longitude']
            latitude_list_selected.append(lat)
            longitude_list_selected.append(long)
            selected_city.append(city)

        markers_selected_city = go.Scattermapbox(
            lat=latitude_list_selected,
            lon=longitude_list_selected,
            showlegend=False,
            mode='markers',
            marker=go.scattermapbox.Marker(
                symbol='marker',
                size=MARKER_CITY_SELECTED_SIZE,
                opacity=1
            ),
            text=selected_city,
            name=''
        )

        markers_selected_dom = go.Scattermapbox(
            lat=sources_migration_points_dom_lat,
            lon=sources_migration_points_dom_long,
            mode='markers',
            marker=go.scattermapbox.Marker(
                color='white',
                size=10,
                opacity=1
            ),
            text=domicile,
            showlegend=False,
            name=''
        )

        markers_selected_he = go.Scattermapbox(
            lat=sources_migration_points_he_lat,
            lon=sources_migration_points_he_long,
            mode='markers',
            marker=go.scattermapbox.Marker(
                color='white',
                size=numbers,
                opacity=0.5
            ),
            text=labels_marker_he,
            showlegend=False,
            name=''
        )

        fig = dict(data=[NUTS1, markers_selected_city, markers_selected_dom, markers_selected_he, trace0, trace1], layout=layout)
        # if year == 2016:
        #     fig = dict(data=[NUTS1, markers_selected_city, trace0, trace1], layout=layout)
        # else:
        #     fig = dict(data=[NUTS1, markers_selected_city], layout=layout)

    result = {'data': fig['data'], 'layout': layout}
    return result


def get_migration_data(domicile, year, level, mode, loneli=None):
    sources_migration_lines = []
    sources_migration_points_dom_lat = []
    sources_migration_points_dom_long = []
    sources_migration_points_he_lat = []
    sources_migration_points_he_long = []
    numbers = []
    labels_marker_he = []
    if domicile is not None:
        print(domicile)
        data_domicile_list = execute_sql_query('SELECT region_of_he_provider, number, domicile, domicile_lat, domicile_long, '
                                               'region_of_he_provider_lat, region_of_he_provider_long FROM %s WHERE academic_year=%s AND domicile="%s" AND level_of_study="%s" AND mode_of_study="%s" GROUP BY '
                                               'region_of_he_provider, number, domicile, domicile_lat, domicile_long, region_of_he_provider_lat, region_of_he_provider_long' % ('student_migration', year-1, domicile, level, mode))
        print(data_domicile_list)
        for item in data_domicile_list:
            if item['number'] <= 0:
                continue
            if item['region_of_he_provider'] == 'United Kingdom':
                continue
            if item['region_of_he_provider'] == 'Wales':
                continue
            if item['region_of_he_provider'] == 'Scotland':
                continue
            if item['region_of_he_provider'] == 'Northern Ireland':
                continue
            sources_migration_lines.append(build_geojon_migration_line(item['domicile_long'], item['domicile_lat'], item['region_of_he_provider_long'], item['region_of_he_provider_lat']))

            # get_ml_data(loneli, domicile, item['region_of_he_provider'])

            sources_migration_points_dom_lat.append(item['domicile_lat'])
            sources_migration_points_dom_long.append(item['domicile_long'])
            sources_migration_points_he_lat.append(item['region_of_he_provider_lat'])
            sources_migration_points_he_long.append(item['region_of_he_provider_long'])
            numbers.append(process_numer_range(item['number']))
            labels_marker_he.append("%s students in %s" % (str(item['number']), item['region_of_he_provider']))

    return sources_migration_lines, sources_migration_points_dom_lat, sources_migration_points_dom_long, sources_migration_points_he_lat, sources_migration_points_he_long, numbers, labels_marker_he


def build_map(year, radio, detail_figure, normalize=False, style='basic', domicile=None, level='All', mode='Full-time'):
    sources_migration_lines, sources_migration_points_dom_lat, sources_migration_points_dom_long, \
    sources_migration_points_he_lat, sources_migration_points_he_long, \
    numbers, labels_marker_he = get_migration_data(domicile, year, level, mode)

    selected = []
    try:
        for i in range(0, len(detail_figure['layout']['annotations'])):
            selected.append(detail_figure['layout']['annotations'][i]['text'] + ', United Kingdom')
    except KeyError as e:
        print(e)

    longitude_list = []
    latitude_list = []
    place_name_list = []
    data_radio_list = []

    data_list = execute_sql_query('SELECT %s, place_name, latitude, '
                                  'longitude FROM %s WHERE year="%s" GROUP BY '
                                  'loneills, place_name, latitude, longitude' % (radio, 'final_data', year))

    for data in data_list:
        longitude = str(data['longitude'])
        latitude = str(data['latitude'])
        place_name = data['place_name']
        data_radio = float(data[radio])
        longitude_list.append(longitude)
        latitude_list.append(latitude)
        data_radio_list.append(data_radio)
        place_name_list.append("%s" % place_name)

    markers, markers_selected_city = make_city_marker(latitude_list, longitude_list, place_name_list,
                                                      data_radio_list, id=radio, selected_city=selected,
                                                      normalize=False if 'zscore' in radio or radio == 'loneills' else True)

    trace0 = go.Bar(x=[0], y=[0], name='Positive (max value: %d)' % max(data_radio_list), marker=dict(color='rgb(214, 39, 40)'))
    trace1 = go.Bar(x=[0], y=[0], name='Negative (min value: %d)' % min(data_radio_list), marker=dict(color='rgb(17, 157, 255)'))

    layers_migration_lines = [dict(sourcetype='geojson',
                                   source=sources_migration_lines[k],
                                   type='line',
                                   color='white',
                                   opacity=0.1
                                   ) for k in range(len(sources_migration_lines))]

    markers_selected_dom = go.Scattermapbox(
        lat=sources_migration_points_dom_lat,
        lon=sources_migration_points_dom_long,
        mode='markers',
        marker=go.scattermapbox.Marker(
            color='white',
            size=10,
            opacity=0.8
        ),
        text=domicile,
        showlegend=False,
        name=''
    )

    markers_selected_he = go.Scattermapbox(
        lat=sources_migration_points_he_lat,
        lon=sources_migration_points_he_long,
        mode='markers',
        marker=go.scattermapbox.Marker(
            color='white',
            size=numbers,
            opacity=0.8
        ),
        text=labels_marker_he,
        showlegend=False,
        name=''
    )

    markers = [markers, markers_selected_city, markers_selected_dom, markers_selected_he, trace0, trace1]

    layout = go.Layout(
        margin=go.layout.Margin(l=0, r=0, t=0, b=0),
        autosize=True,
        showlegend=True,
        legend=dict(
            x=0,
            y=1,
            traceorder='normal',
            font=dict(
                family='sans-serif',
                size=12,
                color='#ffffff'
            ),
            bgcolor='rgb(50, 50, 50)' if style == 'dark' else 'rgb(128, 128, 128)',
            borderwidth=0
        ),
        hovermode='closest',
        mapbox=dict(accesstoken=mapbox_access_token,
                    layers=layers_migration_lines,
                    bearing=0,
                    center=dict(
                        lat=LATITUDE_INIT,
                        lon=LONGITUDE_INIT),
                    pitch=0,
                    zoom=ZOOM,
                    style=style
                    ),
    )
    result = {'data': markers, 'layout': layout}
    return result


def clean_domicile_name(input):
    return input.replace(' not otherwise specified', '').replace('Antarctica and ', '') \
        .replace(', Banbridge and Craigavon', '').replace(' (Except Middle East)', '') \
        .replace(' [Bolivia, Plurinational State of]', '').replace('[Brunei Darussalam]', '').replace(' [Myanmar]', '') \
        .replace(' (European Union)', '').replace(' [Timor Leste]', '').replace(' (Non-European Union)', '') \
        .replace(' [Iran, Islamic Republic of]', '').replace(' [Korea, Democratic People\'s Republic of]', '') \
        .replace(' [Macedonia, The Former Yugoslav Republic of]', '').replace(' [Micronesia, Federated States of]', '') \
        .replace(' [Korea, Republic of]', '').replace(' (district council area unknown)', '') \
        .replace(' [Russian Federation]', '').replace(' (French Part) [St Martin]', '') \
        .replace(' [Syrian Arab Republic]', '').replace(' (council area unknown)', '') \
        .replace(' [Virgin Islands, U. S.]', '').replace(' [Viet Nam]', '') \
        .replace(' (unitary authority unknown)', '').replace(' [Tanzania, United Republic of]', '') \
        .replace(' [Holy See (Vatican City State)]', '').replace(' [Venezuela, Bolivarian Republic of]', '') \
        .replace('Occupied Palestinian Territories [Palestine, State of]', 'Palestine') \
        .replace('Pitcairn, Henderson, Ducie and Oeno Islands [Pitcairn]', 'Pitcairn') \
        .replace(' (county/unitary authority unknown)', '') \
        .replace(' (Special Administrative Region of China) [Hong Kong]', '') \
        .replace(' (Special Administrative Region of China) [Macao]', '').replace(' [Virgin Islands, British]', '')


print('init dash...')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# server = Flask(__name__, static_folder='assets')
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})
# app.css.append_css({"external_url": "body.css"})
# server = app.server
app.title = 'Loneliness Data challenge'


print("dash ccv %s" % dcc.__version__)
print(sys.argv)
db_server_name = "localhost"
db_user = "axel"
db_password = "@2015"
char_set = "utf8"
cusror_type = pymysql.cursors.DictCursor

sql_db = pymysql.connect(host=db_server_name, user=db_user, password=db_password)
connect_to_sql_database(db_server_name, db_user, db_password, db_name, char_set, cusror_type)

city_names = get_as_list('place_name', execute_sql_query("SELECT DISTINCT(place_name) FROM %s" % 'final_data'),
                         clean_city_name=True)
print(city_names)
domiciles = get_as_list('domicile', execute_sql_query("SELECT DISTINCT(domicile) FROM %s" % 'student_migration'),
                        clean_city_name=True)
print(domiciles)
study_levels = get_as_list('level_of_study', execute_sql_query("SELECT DISTINCT(level_of_study) FROM %s" % 'student_migration'))
print(study_levels)

study_modes = get_as_list('mode_of_study', execute_sql_query("SELECT DISTINCT(mode_of_study) FROM %s" % 'student_migration'))
print(study_modes)

build_default_app_layout(app, city_names)

# @server.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(server.root_path, 'assets'), 'favicon.ico')

@app.callback(
    Output('side-by-side', 'style'),
    [Input('city-dropdown', 'value')])
def update_dashboard_height(value):
    print(value)
    if value is not None and len(value) > 2:
        return {'height': '500px', 'width': '1920px', 'margin-bottom': '0px', 'margin-top': '130px'}
    else:
        return {'height': '500px', 'width': '1920px', 'margin-bottom': '0px', 'margin-top': '100px'}


@app.callback(
    Output('dashboard', 'style'),
    [Input('city-dropdown', 'value')])
def update_dashboard_height(value):
    print(value)
    if len(value) > 2:
        return {'width': '100%', 'height': '258px', 'display': 'inline-block', 'background-color': 'gray'}
    else:
        return {'width': '100%', 'height': '228px', 'display': 'inline-block', 'background-color': 'gray'}

@app.callback(
    Output('detail-graph', 'style'),
    [Input('detail-graph', 'figure')])
def hide_graph(fig):
    print(fig)
    if len(fig['data']) == 0:
        return {'display': 'none', 'height': '0px'}
    else:
        return {'display': True}

@app.callback(
    Output('label-2016', 'style'),
    [Input('dark-mode-checkbox', 'on')])
def hide_graph(dark_mode_enabled):
    if dark_mode_enabled:
        return {'color': 'white', 'margin-top': '-40px', 'margin-left': '10px', 'height': '30px', 'background-color':'transparent', 'float':'left', 'z-index': '-1', 'position': 'absolute'}
    else:
        return {'color': 'dimgray', 'margin-top': '-40px', 'margin-left': '10px', 'height': '30px', 'background-color':'transparent', 'float':'left', 'z-index': '-1', 'position': 'absolute'}

@app.callback(
    Output('label-2017', 'style'),
    [Input('dark-mode-checkbox', 'on')])
def hide_graph(dark_mode_enabled):
    if dark_mode_enabled:
        return {'color': 'white', 'margin-top': '-40px', 'margin-left': '400px', 'height': '30px', 'background-color':'transparent', 'float':'left', 'z-index': '-1', 'position': 'absolute'}
    else:
        return {'color': 'dimgray', 'margin-top': '-40px', 'margin-left': '400px', 'height': '30px', 'background-color':'transparent', 'float':'left', 'z-index': '-1', 'position': 'absolute'}


@app.callback(
    Output('label-2018', 'style'),
    [Input('dark-mode-checkbox', 'on')])
def hide_graph(dark_mode_enabled):
    if dark_mode_enabled:
        return {'color': 'white', 'margin-top': '-40px', 'margin-left': '790px', 'height': '30px', 'background-color':'transparent', 'float':'left', 'z-index': '-1', 'position': 'absolute'}
    else:
        return {'color': 'dimgray', 'margin-top': '-40px', 'margin-left': '790px', 'height': '30px', 'background-color':'transparent', 'float':'left', 'z-index': '-1', 'position': 'absolute'}


@app.callback(
    Output('detail-graph', 'figure'),
    [Input('condition-checkbox', 'values'),
     Input('city-dropdown', 'value')])
def update_figure(conditions, city_list):

    if city_list is not None and len(city_list) > 0:
        titles = tuple([x.replace(', United Kingdom','') for x in city_list])
        fig = tools.make_subplots(rows=len(city_list), cols=1, subplot_titles=titles)
        for i, city in enumerate(city_list):
            print(city)
            year_list = []
            depression_perc_list = []
            alzheimers_perc_list = []
            blood_pressure_perc_list = []
            hypertension_perc_list = []
            diabetes_perc_list = []
            cardiovascular_disease_perc_list = []
            insomnia_perc_list = []
            addiction_perc_list = []
            social_anxiety_perc_list = []
            loneliness_perc_list = []
            depression_zscore_list = []
            alzheimers_zscore_list = []
            blood_pressure_zscore_list = []
            hypertension_zscore_list = []
            diabetes_zscore_list = []
            cardiovascular_disease_zscore_list = []
            insomnia_zscore_list = []
            addiction_zscore_list = []
            social_anxiety_zscore_list = []
            loneliness_zscore_list = []
            loneills_list = []
            place_name_list = []
            number_of_patients_list = []
            data = execute_sql_query('SELECT year, number_of_patients, depression_perc,'
                                     ' alzheimers_perc, blood_pressure_perc,'
                                     ' hypertension_perc, diabetes_perc, cardiovascular_disease_perc,'
                                     ' insomnia_perc, addiction_perc, social_anxiety_perc,'
                                     ' loneliness_perc, depression_zscore, alzheimers_zscore,'
                                     ' blood_pressure_zscore, hypertension_zscore, '
                                     'diabetes_zscore, cardiovascular_disease_zscore,insomnia_zscore,'
                                     ' addiction_zscore, social_anxiety_zscore, loneliness_zscore,'
                                     ' loneills, place_name FROM %s WHERE place_name="%s" GROUP BY year,'
                                     ' number_of_patients,'
                                     ' depression_perc, alzheimers_perc, blood_pressure_perc, hypertension_perc,'
                                     ' diabetes_perc, cardiovascular_disease_perc, insomnia_perc, addiction_perc,'
                                     ' social_anxiety_perc, loneliness_perc, depression_zscore, alzheimers_zscore,'
                                     ' blood_pressure_zscore, hypertension_zscore, diabetes_zscore,'
                                     ' cardiovascular_disease_zscore,insomnia_zscore, addiction_zscore,'
                                     ' social_anxiety_zscore, loneliness_zscore,'
                                     ' loneills, place_name' % ('final_data', city))
            for row in data:
                year_list.append(row['year'])
                depression_perc_list.append(row['depression_perc'])
                alzheimers_perc_list.append(row['alzheimers_perc'])
                blood_pressure_perc_list.append(row['blood_pressure_perc'])
                hypertension_perc_list.append(row['hypertension_perc'])
                diabetes_perc_list.append(row['diabetes_perc'])
                cardiovascular_disease_perc_list.append(row['cardiovascular_disease_perc'])
                insomnia_perc_list.append(row['insomnia_perc'])
                addiction_perc_list.append(row['addiction_perc'])
                social_anxiety_perc_list.append(row['social_anxiety_perc'])
                loneliness_perc_list.append(row['loneliness_perc'])
                depression_zscore_list.append(row['depression_zscore'])
                alzheimers_zscore_list.append(row['alzheimers_zscore'])
                blood_pressure_zscore_list.append(row['blood_pressure_zscore'])
                hypertension_zscore_list.append(row['hypertension_zscore'])
                diabetes_zscore_list.append(row['diabetes_zscore'])
                cardiovascular_disease_zscore_list.append(row['cardiovascular_disease_zscore'])
                insomnia_zscore_list.append(row['insomnia_zscore'])
                addiction_zscore_list.append(row['addiction_zscore'])
                social_anxiety_zscore_list.append(row['social_anxiety_zscore'])
                loneliness_zscore_list.append(row['loneliness_zscore'])
                loneills_list.append(row['loneills'])
                place_name_list.append(row['place_name'])
                number_of_patients_list.append(row['number_of_patients'])

            traces = get_traces(conditions, year_list, depression_perc_list, alzheimers_perc_list,
                                blood_pressure_perc_list, hypertension_perc_list, diabetes_perc_list,
                                cardiovascular_disease_perc_list, insomnia_perc_list, addiction_perc_list, social_anxiety_perc_list,
                                loneliness_perc_list, depression_zscore_list, alzheimers_zscore_list, blood_pressure_zscore_list,
                                hypertension_zscore_list, diabetes_zscore_list, cardiovascular_disease_zscore_list,
                                insomnia_zscore_list, addiction_zscore_list, social_anxiety_zscore_list, loneliness_zscore_list,
                                loneills_list, number_of_patients_list)

            for idx, t in enumerate(traces):
                if i == 0:
                    t.showlegend = True
                fig.append_trace(t, i+1, 1)

        fig['layout']['xaxis'].update(nticks=4)
        for n in range(0, len(city_list)-1):
            print('xaxis%d' % (n+2))
            fig['layout']['xaxis%d' % (n+2)].update(nticks=4)

        fig['layout'].update(height=660, width=700,
                             paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                             barmode='stack' if len(conditions) == 1 and 'loneills' in conditions else 'group')

        # fig['style'].update(display=True)

        # py.iplot(fig, filename='make-subplots-multiple-with-titles')

        result = {'data': fig.data, 'layout': fig.layout}
        return result
    else:
        print('clean...')
        layout = go.Layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        return {'data': {}, 'layout': layout}


@app.callback(
    Output('condition-checkbox', 'values'),
    [Input('select-all-checkbox', 'values')])
def update_checkbox(sellect_all):
    print(sellect_all)
    # options = ['depression_perc', 'alzheimers_perc',
    #            'blood_pressure_perc', 'hypertension_perc', 'diabetes_perc',
    #            'cardiovascular_disease_perc', 'insomnia_perc', 'addiction_perc',
    #            'social_anxiety_perc', 'loneliness_perc', 'depression_zscore',
    #            'alzheimers_zscore', 'blood_pressure_zscore', 'hypertension_zscore',
    #            'diabetes_zscore', 'cardiovascular_disease_zscore', 'insomnia_zscore',
    #            'addiction_zscore', 'social_anxiety_zscore', 'loneliness_zscore', 'loneills']
    options = ['depression_zscore','alzheimers_zscore', 'blood_pressure_zscore', 'hypertension_zscore',
               'diabetes_zscore', 'cardiovascular_disease_zscore', 'insomnia_zscore',
               'addiction_zscore', 'social_anxiety_zscore', 'loneliness_zscore', 'loneills']
    if sellect_all is not None and 'enabled' in sellect_all:
        return options
    else:
        return ['loneills']


def format_to_checkbox_string(string_list, empty=False):
    result = []
    for string in string_list:
        if len(string) > 10:
            print(string)
        result.append({'label': string, 'value': '' if empty else string})
    return result

@app.callback(
    Output('map-2016', 'figure'),
    [Input('condition-checkbox', 'values'),
     Input('condition-radio', 'value'),
     Input('detail-graph', 'figure'),
     Input('normalize-checkbox', 'values'),
     Input('dark-mode-checkbox', 'on'),
     Input('choropleth-mode-lowres-checkbox', 'on'),
     Input('choropleth-mode-highres-checkbox', 'on'),
     Input('domicile-dropdown', 'value'),
     Input('study-level-dropdown', 'value'),
     Input('study-mode-dropdown', 'value')
     ])
def update_figure(_, radio, detail_figure, normalize, mode, choropleth, choropleth_highres, domicile, level, mode_of_study):
    if level is None:
        level = 'All'
    if mode_of_study is None:
        mode_of_study = 'Full-time'
    if choropleth or choropleth_highres:
        return build_choropleth_map(2016, radio, detail_figure, 'enabled' in normalize, style='dark' if mode else 'basic', high_res=choropleth_highres, domicile=domicile, level=level, mode=mode_of_study)
    else:
        return build_map(2016, radio, detail_figure, 'enabled' in normalize, style='dark' if mode else 'basic', domicile=domicile, level=level, mode=mode_of_study)

@app.callback(
    Output('choropleth-mode-lowres-checkbox', 'on'),
    [Input('choropleth-mode-highres-checkbox', 'on')])
def update_figure(highres_on):
    if highres_on:
        return False

@app.callback(
    Output('choropleth-mode-lowres-checkbox', 'disabled'),
    [Input('choropleth-mode-highres-checkbox', 'on')])
def update_figure(highres_on):
    if highres_on:
        return True
    else:
        return False

@app.callback(
    Output('map-2017', 'figure'),
    [Input('condition-checkbox', 'values'),
     Input('condition-radio', 'value'),
     Input('detail-graph', 'figure'),
     Input('normalize-checkbox', 'values'),
     Input('dark-mode-checkbox', 'on'),
     Input('choropleth-mode-lowres-checkbox', 'on'),
     Input('choropleth-mode-highres-checkbox', 'on'),
     Input('domicile-dropdown', 'value'),
     Input('study-level-dropdown', 'value'),
     Input('study-mode-dropdown', 'value')
     ])
def update_figure(_, radio, detail_figure, normalize, mode, choropleth, choropleth_highres, domicile, level, mode_of_study):
    if level is None:
        level = 'All'
    if mode_of_study is None:
        mode_of_study = 'Full-time'
    if choropleth or choropleth_highres:
        return build_choropleth_map(2017, radio, detail_figure, 'enabled' in normalize,
                                    style='dark' if mode else 'basic', high_res=choropleth_highres, domicile=domicile, level=level, mode=mode_of_study)
    else:
        return build_map(2017, radio, detail_figure, 'enabled' in normalize,
                         style='dark' if mode else 'basic', domicile=domicile, level=level, mode=mode_of_study)

@app.callback(
    Output('map-2018', 'figure'),
    [Input('condition-checkbox', 'values'),
     Input('condition-radio', 'value'),
     Input('detail-graph', 'figure'),
     Input('normalize-checkbox', 'values'),
     Input('dark-mode-checkbox', 'on'),
     Input('choropleth-mode-lowres-checkbox', 'on'),
     Input('choropleth-mode-highres-checkbox', 'on'),
     Input('domicile-dropdown', 'value'),
     Input('study-level-dropdown', 'value'),
     Input('study-mode-dropdown', 'value')
     ])
def update_figure(_, radio, detail_figure, normalize, mode, choropleth, choropleth_highres, domicile, level, mode_of_study):
    if level is None:
        level = 'All'
    if mode_of_study is None:
        mode_of_study = 'Full-time'
    if choropleth or choropleth_highres:
        return build_choropleth_map(2018, radio, detail_figure, 'enabled' in normalize,
                                    style='dark' if mode else 'basic', high_res=choropleth_highres, domicile=domicile, level=level, mode=mode_of_study)
    else:
        return build_map(2018, radio, detail_figure, 'enabled' in normalize,
                         style='dark' if mode else 'basic', domicile=domicile, level=level, mode=mode_of_study)

@app.callback(
    Output('city-dropdown', 'value'),
    [Input('button', 'n_clicks_timestamp')])
def empty_dropdown(n_clicks):
    if n_clicks is not None:
        click_date = datetime.utcfromtimestamp(float(n_clicks)/1000.0).strftime('%Y-%m-%d %H:%M:%S').split(' ')[1][3:]
        now_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S').split(' ')[1][3:]
        print(click_date, now_date)
        if click_date == now_date:
            return []
    else:
        raise dash.exceptions.PreventUpdate()

@app.callback(
    Output('dropdown-data-city', 'children'),
    [Input('city-dropdown', 'value')]
)
def disable_dropdown(value):
    if len(value) > 4:
        v = [value[0], value[-1]]
        return json.dumps(v, indent=2)
    else:
        return json.dumps(value, indent=2)


@app.callback(
    Output('city-dropdown', 'disabled'),
    [Input('dropdown-data-city', 'children'),
     Input('button', 'n_clicks_timestamp')])
def update_serial_number_drop_down(dropdown_value, n_clicks):
    if n_clicks is not None:
        click_date = datetime.utcfromtimestamp(float(n_clicks)/1000.0).strftime('%Y-%m-%d %H:%M:%S').split(' ')[1][3:]
        now_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S').split(' ')[1][3:]
        print(click_date, now_date)
        if click_date == now_date:
            return False
    d = json.loads(dropdown_value)
    if d is not None:
        return len(d) > 3


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)




