import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pathlib
from app import app


PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data/").resolve()
#-------------  Importing  ----------------
df = pd.read_csv(DATA_PATH.joinpath("final_df.csv"))

#-------------  Interactive components ----------------
firm_name_options = [dict(label=firm, value=firm) for firm in df['Company Name'].dropna().unique()]


layout= dbc.Container([
    
    dbc.Row([
        dbc.Col([
            html.H2('Company Analysis',className = 'text-center ')
        ],width=12)
    ]),

    dbc.Row(
        dbc.Col([
            html.H6("Company Choice",className='text-left text mb-4 ml-4'),
            dcc.Dropdown(
                id='firm_drop',
                options=firm_name_options,
                value=['Apple', 'Amazon', 'Accenture'],
                multi=True)
        ],width=12, className="mb-3")
    ),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Average Salary',className = 'text-white'),
                    dbc.ListGroup([
                        dbc.ListGroupItem(id='avgsalary')
                    ])
                ])
            ], color="#4E8975",className='mb-5'),
            dbc.Card([
                dbc.CardBody([
                    html.H4('Average Rating',className = 'text-white'),
                    dbc.ListGroup([
                        dbc.ListGroupItem(id='avgrating')
                    ])
                ])
            ], color="#4E8975",className='mb-5'),
            dbc.Card([
                dbc.CardBody([
                    html.H4('Best Company',className = 'text-white'),
                    dbc.ListGroup([
                        dbc.ListGroupItem(id='bestsal')
                    ])
                ])
            ],color = "#4E8975"),
        ], width={'size': 6}, className="mb-3 mt-3"),
        dbc.Col([
            dbc.Card(
                dcc.Graph(id='fig'),body = True,color = "#4E8975"
            )
        ],width={'size':6},className="mb-3 mt-3"),
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dcc.Graph(id='pie'), body=True, color="#4E8975"
            )
        ], width={'size': 6}, className="mb-3 mt-3"),
        dbc.Col([
            dbc.Card(
                   dcc.Graph(id='littledots'),body = True,color = "#4E8975"
            )
        ], width={'size': 6},className="mb-5 mt-3"),
    ])
],style={'background-color':'#f9fff0'} ,fluid = True)


@app.callback(
    [
    Output('pie', 'figure'),
    Output('fig', 'figure')
    ],
    [
    Input('firm_drop', 'value')
    ]
)

def plots(firm):
    sector = df[df['Company Name'].isin(firm)]['Sector'].replace(
        to_replace=['-1', -1], value='Information Technology').value_counts().nlargest(n=10)
    sector_df = pd.DataFrame(sector).reset_index().rename(columns={"index": "sector", "Sector": "job count"})

    pieplot = px.pie(sector_df,
                 values="job count",
                 names="sector",
                 labels="sector",
                 title="Selected Companies Sector",
                 color=sector.values,
                 color_discrete_sequence=['#195b4b','#0e332a','#13473b','#1e6f5c','#61af54','#71b765','#81bf77','#91c788','#a1cf99','#b1d7ab','#c1dfbc']
                     )

    pieplot.update_traces(
        hovertemplate='Sector: %{label} <br>Number of Postings: %{value} <extra></extra>',
        opacity=0.7,
        #marker_line_color='rgb(8,48,107)',
        #marker_line_width=1.5, textposition='inside',
        textinfo='percent+value+label')
    pieplot.update_layout(title_x=0.5)

    ######################################################################################
    loc_title = df[df['Company Name'].isin(firm)]["Location"].value_counts().sort_values(ascending=False).head(10)
    loc_title_df = pd.DataFrame(loc_title)

    fig = px.bar(loc_title_df, x="Location", y=loc_title_df.index,
                 color='Location',
                 labels={"loc_title_df.index": "Location",
                         "Location": "no. of jobs"},
                 title="Number of Job Postings per Location",
                 text=loc_title_df['Location'],
                 color_continuous_scale='mint'
                 )

    fig.update_traces(
        hovertemplate='City: %{y} <br>Number of Postings: %{x} <extra></extra>',
        textposition='outside',
        #marker_line_color='rgb(8,48,107)',
        #marker_line_width=1.5,
        opacity=0.7)
    fig.update_layout(
        xaxis_title="Number of Postings",
        yaxis_title="City",
        title_x=0.5)

    fig.update(layout_coloraxis_showscale=False)
    return pieplot,\
           fig

@app.callback(
    Output('littledots', 'figure'),
    [
        Input('firm_drop', 'value')
    ]
)

def scatterplot(firm):
    scatterdf = df[df['Company Name'].isin(firm)][['Company Name', 'Rating', 'Avg Salary']].groupby('Company Name').mean().reset_index()

    figscat = px.scatter(
        y=scatterdf['Avg Salary'],
        x=scatterdf['Rating'],
        text=scatterdf['Company Name'],
        #mode='markers',
        #marker=dict(
        #size=scatterdf['Rating'],
        #color=scatterdf['Avg Salary'],  # set color equal to a variable
        #color_continuous_scale='mint',  # one of plotly colorscales
        #showscale=False,
        )

    figscat.update_xaxes(
        range=[0, 5],  # sets the range of xaxis
    )
    figscat.update_yaxes(
        range=[0, 250],  # sets the range of xaxis
    )
    figscat.update_layout(title=dict(
                                 text='Company Rating per Company Average Salary',
                                 x=.5  # Title relative position according to the xaxis, range (0,1)
    ),
                    xaxis_title = "Rating",
                    yaxis_title = "Average Salary",
    )
    figscat.update_traces(
        hovertemplate='Company: %{text} <br>Rating: %{x} <br>Average Salary: %{y} <extra></extra>',
        marker=dict(size=12,
                    color='#61af54'),
        showlegend=False
    )
    #figscat.update(layout_coloraxis_showscale=False)

    return figscat


@app.callback(
    [
    Output('avgsalary', 'children'),
    Output('avgrating', 'children'),
    Output('bestsal', 'children'),
    ],
    [
    Input('firm_drop', 'value')
    ]
)

def indicator(firm):
    scatterdf = df[df['Company Name'].isin(firm)][['Company Name', 'Rating', 'Avg Salary']].groupby('Company Name').mean().reset_index()

    avgsal = round(scatterdf['Avg Salary'].mean(),2)
    avgrat = round(scatterdf['Rating'].mean(),2)
    maxsal = scatterdf['Avg Salary'].max()
    name = scatterdf[scatterdf['Avg Salary'] == maxsal].iloc[0, 0]
    value = round(scatterdf[scatterdf['Avg Salary'] == maxsal].iloc[0, 2],2)

    return str(avgsal),\
           str(avgrat),\
           str(name)+' | ' + str(value)
