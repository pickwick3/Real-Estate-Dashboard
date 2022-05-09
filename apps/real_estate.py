from app import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go
from Webscraper import Scraper


def getData(state_abbrev, city_or_town):
    scraper = Scraper(state_abbrev, city_or_town)
    return scraper.Report_Data(report_type='real_estate')

layout = html.Div([
    html.H1('Real Estate Data', style={"textAlign": "center"}),
    html.Div([
        html.Div([
            html.Pre(children="State Abbreviation", style={"fontSize":"120%"}),
            dcc.Input(
                id = 'state-input-real-estate',
                placeholder = 'Enter a state abbrev...',
                type = 'text',
                value = ''
            )
        ]),
        html.Div([
            html.Pre(children='Town/City (separate spaces with dashes)', style={"fontSize": "120%"}),
            dcc.Input(
                id = 'town-city-input-real-estate',
                placeholder = 'Enter a town or city...',
                type = 'text',
                value = ''
            )
        ]),
        html.Button('Submit', id='submit-button-real-estate')
    ]),
    html.Div([
        html.Pre(
            id = 'median-home-value',
            style = dict(fontSize = '150%')
        ),
        html.Pre(
            id = 'num-homes-and-apts',
            style = dict(fontSize = '150%')
        ),
        html.Pre(
            id = 'avg-mkt-rent',
            style = dict(fontSize = '150%')
        ),
        dcc.Graph(
            id = 'home-ownership-rate'
        ),
        dcc.Graph(
            id = 'age-of-homes'
        ),
        dcc.Graph(
            id = 'types-of-homes'
        ),
        dcc.Graph(
            id = 'home-size'
        )
    ])
])

@app.callback(
    [
        Output(
            component_id = 'median-home-value',
            component_property = 'children'
        ),
        Output(
            component_id = 'num-homes-and-apts',
            component_property = 'children'
        ),
        Output(
            component_id = 'avg-mkt-rent',
            component_property = 'children'
        ),
        Output(
            component_id = 'home-ownership-rate',
            component_property = 'figure'
        ),
        Output(
            component_id = 'age-of-homes',
            component_property = 'figure'
        ),
        Output(
            component_id = 'types-of-homes',
            component_property = 'figure'
        ),
        Output(
            component_id = 'home-size',
            component_property = 'figure'
        )
    ],
    [
        Input(
            component_id = 'submit-button-real-estate',
            component_property = 'n_clicks'
        )

    ],
    [
        State(
            component_id = 'state-input-real-estate',
            component_property = 'value'
        ),
        State(
            component_id = 'town-city-input-real-estate',
            component_property = 'value'
        )
    ]
)
def updateTable(n_clicks, state_input, town_city_input):
    data = getData(state_input, town_city_input)

    median_home_value = data['median_home_value']
    num_homes_and_apts = data['num_homes_and_apts']
    avg_mkt_rent = data['avg_mkt_rent']
    home_ownership_rate = data[['owners', 'renters', 'vacant']]
    age_of_homes = data[['newer', 'new', 'old', 'older']]
    types_of_homes = data[['single_family_homes', 'townhomes', 'small_apt_buildings', 'apt_complexes', 'mobile_homes', 'other_home_types']]
    bedroom_count = data[['no_bedroom', 'one_bedroom', 'two_bedrooms', 'three_bedrooms', 'four_bedrooms', 'five_or_more_bedrooms']]

    trace0 = [go.Bar(
        x = home_ownership_rate.index,
        y = home_ownership_rate.values,
        marker = dict(color=home_ownership_rate.values, colorscale='viridis')
        )]
    trace1 = [go.Bar(
        x = ['2000 or newer', '1970-1999', '1940-1969', '1939 or older'], y = age_of_homes.values,
        marker = dict(color=age_of_homes.values, colorscale='viridis')
        )]
    trace2 = [go.Bar(
        x = types_of_homes.index,
        y = types_of_homes.values,
        marker = dict(color=types_of_homes.values, colorscale='viridis')
        )]
    trace3 = [go.Bar(
        x = bedroom_count.index, y = bedroom_count.values,
        marker = dict(color=bedroom_count.values, colorscale='viridis')
        )]

    return(
        f'Median Home Value = ${median_home_value}',
        f'Number of Homes and Apts = {num_homes_and_apts}',
        f'Average Market Rent = ${avg_mkt_rent}',
        dict(
            data = trace0,
            layout = go.Layout(
                title = 'Home Ownership Rate'
            )
        ),
        dict(
            data = trace1,
            layout = go.Layout(
                title = 'Age of Homes'
            )
        ),
        dict(
            data = trace2,
            layout = go.Layout(
                title = 'Types of Homes'
            )
        ),
        dict(
            data = trace3,
            layout = go.Layout(
                title = 'Bedroom Count'
            )
        )
    )