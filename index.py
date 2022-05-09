from app import app
from apps import real_estate
from apps import crime
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Real Estate Data | ', href='/apps/real_estate'),
        dcc.Link('Crime Data', href='/apps/crime')
    ], className="row"),
    html.Div(id='page-content', children=[])
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/real_estate':
        return real_estate.layout
    if pathname == '/apps/crime':
        return crime.layout
    else:
        return "Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=False)
