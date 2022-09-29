import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('data/alldata_wgs846.csv')  # .query("bld_age == '2015'")

app = Dash(__name__)
app.title = "Material Mining in Barcelona"

# setting up our figures
colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}
figure = px.scatter_mapbox(df, lat="y1", lon="x1", hover_name="ogc_fid", hover_data=["ogc_fid"],
                           zoom=12, height=780,  opacity=0.5, color=df["bld_age"],
                           color_continuous_scale=px.colors.sequential.matter,
                           title="Hover on the map to see the amount of materials each building has:",
                           )
figure.update_layout(mapbox_style="carto-positron")
figure.update_layout(margin={"r": 60, "t": 100, "l": 60, "b": 10})

# setting up the layout
app.layout = html.Div(
    style={'backgroundColor': colors['background']}, children=[
        html.A(
                    html.Img(id="logo", src=app.get_asset_url("logo.png")),
                    href="https://plotly.com/dash/",
                ),
        html.H1(children="Material Mining in Barcelona", style={
            'textAlign': 'left',
            'color': colors['text']}),
        html.H3(children='Measuring the amount of materials in buildings in Barcelona.', style={
                            'textAlign': 'left',
                            'color': colors['text']}
                ),
        html.H6(children="A project developed in IAAC, Institute for Advanced Architecture of Catalonia developed at \
                         Master in City and Technology in 2021/2022"
                ),
        html.H6(children="By students:Maria Augusta Kroetz, Dimitrios Lampriadis, Yohan Wadia, Julia Veiga, and \
                         Faculty: Diego Pajarito"
                ),
        html.Div(
            className="map",
            children=[
                html.Div(
                    className="eight columns",
                    children=[
                        html.Div(
                            children=dcc.Graph(
                                figure=figure,
                                id='map',
                                # hoverData={'points': [{'customdata': 3}]}
                                # hoverData={'points': [{'hovertext': 6980}]},
                                hoverData=None
                            )
                        )
                    ]
                )
            ]
        ),
        html.Div(
            className="histogram",
            children=[
                html.Div(
                    className="four and half columns",
                    children=[
                        html.Div(
                            children=dcc.Graph(id='histogram')
                        )

                    ]

                )
            ]
        )
    ]
)


@app.callback(
    Output('histogram', 'figure'),
    Input('map', 'hoverData'))
def histogram(hoverData):
    print("---------------------------")
    # print(hoverData['points'][0])
    if hoverData==None:
        dff = df[df["ogc_fid"] == None]
        histogram = px.histogram(df, x='ogc_fid',
                                 y=["Stone", "Concrete", "Brick", "Glass", "Metal", "Wood"],
                                 labels={'ogc_fid': 'building'}, title="Total amount of materials in Barcelona: ", height=780,
                                 width=660,
                                 color_discrete_sequence=px.colors.sequential.matter
                                 )
    else:
        id = hoverData['points'][0]['hovertext']
        # print(id)
        dff = df[df["ogc_fid"] == id]
        print(dff)
        histogram = px.histogram(dff, x='ogc_fid',
                             y=["Stone", "Concrete", "Brick", "Glass", "Metal", "Wood"],
                             labels={'ogc_fid': 'building'}, title="Amount of materials in building ID: {0} ".format(
                                        id
                                    ), height=780, width=660,
                             color_discrete_sequence=px.colors.sequential.matter
                             )
    return histogram
if __name__ == '__main__':
    app.run_server(debug=True)
