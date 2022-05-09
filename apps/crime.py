from app import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go
from Webscraper import Scraper


def getData(state_abbrev, city_or_town):
    scraper = Scraper(state_abbrev, city_or_town)
    return scraper.Report_Data(report_type='crime')

layout = html.Div([
    html.H1('Crime Data', style={"textAlign": "center"}),
    html.Div([
        html.Div([
            html.Pre(children="State Abbreviation", style={"fontSize":"120%"}),
            dcc.Input(
                id = 'state-input-crime',
                placeholder = 'Enter a state abbrev...',
                type = 'text',
                value = ''
            )
        ]),
        html.Div([
            html.Pre(children='Town/City (separate spaces with dashes)', style={"fontSize": "120%"}),
            dcc.Input(
                id = 'town-city-input-crime',
                placeholder = 'Enter a town or city...',
                type = 'text',
                value = ''
            )
        ]),
        html.Button('Submit', id='submit-button-crime')
    ]),
    html.Div([
        html.Pre(
            id = 'crime-index-output',
            style = dict(fontSize = '150%')
        ),
        dcc.Graph(
            id = 'num-annual-crimes-graph'
        ),
        dcc.Graph(
            id = 'annual-crime-rate-per-1000-graph'
        )
    ])
])

@app.callback(
    [
        Output(
            component_id = 'crime-index-output',
            component_property = 'children'
        ),
        Output(
            component_id = 'num-annual-crimes-graph',
            component_property = 'figure'
        ),
        Output(
            component_id = 'annual-crime-rate-per-1000-graph',
            component_property = 'figure'
        )
    ],
    [
        Input(
            component_id = 'submit-button-crime',
            component_property = 'n_clicks'
        )

    ],
    [
        State(
            component_id = 'state-input-crime',
            component_property = 'value'
        ),
        State(
            component_id = 'town-city-input-crime',
            component_property = 'value'
        )
    ]
)
def updateTable(n_clicks, state_input, town_city_input):
    data = getData(state_input, town_city_input)

    crime_index = data['crime_index']
    num_annual_crimes = data[['num_violent_crimes', 'num_property_crimes', 'num_total_crimes']]
    annual_crime_rate_per_1000 = data[['violent_crimes_per_1000', 'property_crimes_per_1000', 'total_crimes_per_1000']]

    trace0 = [go.Bar(
        x = num_annual_crimes.index,
        y = num_annual_crimes.values,
        marker = dict(color=num_annual_crimes.values, colorscale='viridis')
        )]
    trace1 = [go.Bar(
        x = annual_crime_rate_per_1000.index, y = annual_crime_rate_per_1000.values,
        marker = dict(color=annual_crime_rate_per_1000.values, colorscale='viridis')
        )]

    return(
        f'Crime Index = {crime_index} ({town_city_input} is safer than {crime_index}% of US cities)',
        dict(
            data = trace0,
            layout = go.Layout(
                title = 'Annual Crime Counts',
                xaxis = dict(title='Type of crime')
            )
        ),
        dict(
            data = trace1,
            layout = go.Layout(
                title = 'Annual Crime Rates Per 1000 Residents',
                xaxis = dict(title='Type of crime')
            )
        )
    )
