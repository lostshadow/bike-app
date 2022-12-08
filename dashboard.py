import dash
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dash_table


df=pd.read_csv('./data/bike_data.csv')
df_table=df.loc[:, ['date', 'temperature',  'humidity', 'windspeed','count', 'year', 'month', 'day']]
df_table=df_table.iloc[:14]
print(df_table)
years=df.year.unique()

colors = {
    'background': '#64696D',
    'text': '#7FDBFF'
}

fig = px.bar(df, x="month", y="count", color="year", barmode="group")
fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)


app=dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
              meta_tags=[{'name': 'viewport',
                          'content': 'width=device-width, initial-scale=1.0'}])

app.layout = dbc.Container([
    #Place for title
    dbc.Row([
        dbc.Col(html.H1("Web Dashboard location de vélo", className='text-center text-primary, mb-4'),
                width=12)


    ]),
    #Deuxième ligne
    dbc.Row([
        #Première colonne
        dbc.Col([
                html.Div([

                        dash_table.DataTable(
                            id='table',
                            columns=[{"name": i, "id": i}
                                     for i in df_table.columns],
                            data=df_table.to_dict('records'),
                            style_cell=dict(textAlign='left'),
                            style_header=dict(backgroundColor="paleturquoise"),
                            style_data=dict(backgroundColor="lavender")
                        )


                ]),

            ],width={'size': 3, 'offset': 1, 'order' : 1},
                    xs=12, sm=12, md=12, lg=5, xl=5
        ),
        #Deuxième colonne
        dbc.Col([
                html.Div([
                    dcc.Dropdown(
                        id="dropdown",
                        options=[{"label": x, "value": x} for x in years],
                        value=years[0],
                        clearable=False,
                    ),
                dcc.Graph(
                    id='bar-chart',
                    #figure=fig
                )
            ])


        ],width={'size': 7, 'offset': 1, 'order' : 1},
                    xs=12, sm=12, md=12, lg=5, xl=5),


    ]),



],fluid=True)

@app.callback(
    Output("bar-chart", "figure"),
    [Input("dropdown", "value")])
def update_bar_chart(year):
    mask = df["year"] == year
    fig = px.bar(df[mask], x="month", y="count", barmode="group")
    return fig


if __name__=='__main__':
    app.run_server(debug=True)