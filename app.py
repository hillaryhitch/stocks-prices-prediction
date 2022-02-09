import dash
# Create a server side resource.


app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server
