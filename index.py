import dash_core_components as dcc
import dash_html_components as html
import dash

from app import app
from app import server
from layouts import stocks
import callbacks

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content')
])

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
         return stocks # This is the "home page"

if __name__ == '__main__':
    app.run_server(debug=False)

