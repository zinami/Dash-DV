import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from app import app 

import pathlib

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data/").resolve()
#-------------  Importing  ----------------
df = pd.read_csv(DATA_PATH.joinpath("final_df.csv"))



#---------Functions----------

#---------Dropdown----------
state_options = [dict(label =state, value = state) for state in  df[df["state"]!='United Kingdom']["state"].dropna().unique()]

dropdown_state = dcc.Dropdown(
    id="state_drop",
    options = state_options,
    value = df[df["state"]!='United Kingdom']["state"].dropna().unique().tolist(),
    multi=True
    )
#------Layout ------ 

layout = dbc.Container([
    dbc.Row([
       dbc.Col([
            html.H2('Location Analysis',className = 'text-center')
        ],width=12) 
    ]),
    dbc.Row([
        dbc.Col([
            html.H4("Choose a State", className='text-left mb-4 ml-4'),
            dropdown_state
        ], width={'size': 12,'offset':0},className="mb-3")
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dcc.Graph(id="tree-graph"),body = True,color = "#4E8975"
            )
        ],width={'size':6}, className="mb-3 mt-3"),
        
        dbc.Col([
            dbc.Card(
                dcc.Graph(id="map-graph"),body = True,color = "#4E8975"
            )
        ],width={'size':6}, className="mb-3 mt-3"),
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dcc.Graph(id="pie-job"),body = True,color = "#4E8975"
            )
        ],width={'size':6}, className="mb-3 mt-3"),
        
        dbc.Col([
            dbc.Card(
                dcc.Graph(id="pie-company"),body = True,color = "#4E8975"
            )
        ],width={'size':6}, className="mb-3 mt-3"),
    ])
       
       
],style={'background-color':'#f9fff0'} ,fluid = True)




#----CallBack--------
@app.callback(
    Output('tree-graph','figure'),
    [
    Input('state_drop','value')
    ]
)
def tree(state):
    data= df[df['state'].isin(state)].groupby("state")["Location"].value_counts()
    data.dropna(inplace = True)
    data_= pd.DataFrame(data).rename(columns={"Location": "count"}).reset_index()

    fig = px.treemap(data_, path=['state', 'Location'], values='count',color='count', 
                     color_continuous_scale='mint',
                    title=('States and Cities with Number of Jobs'))
    fig.update_layout(title_x=0.5)
    fig.update_traces(
        hovertemplate='Location: %{label} <br>Number of Postings: %{value} <extra></extra>')
                
    return fig

@app.callback(
    Output('map-graph', 'figure'),
    [
    Input('state_drop', 'value')
    ]
)

def map(state):
    df_map = df[df['state'].isin(state)].groupby('State Code').size().to_frame().reset_index().rename(columns = {0:'Number of postings'})
    map_df = df[['State Code', 'Region']]
    cloro_df  = pd.merge(df_map,map_df).drop_duplicates().reset_index(drop = True)
    cloro_df.dropna(inplace=True)
    data_choropleth = dict(type='choropleth',
                            locations=cloro_df['State Code'],
                            # There are three ways to 'merge' your data with the data pre embedded in the map
                            locationmode='USA-states',
                            z= cloro_df['Number of postings'].astype(int),
                            text=cloro_df['Region'],
                            colorscale='mint'
                            )

    layout_choropleth = dict(geo=dict(scope='usa',  # default
                                      ),

                             title=dict(
                                 text='Job Postings by States',
                                 x=.5  # Title relative position according to the xaxis, range (0,1)
                             )
                             )

    fig = go.Figure(data=data_choropleth, layout=layout_choropleth)
    fig.update_traces(
        hovertemplate='State: %{location} <br>Region: %{text} <br>Number of postings: %{z} <extra></extra>',
    zmin = 0,
    zmax = 4000)
    return fig

@app.callback(
    Output('pie-job', 'figure'),
    [
    Input('state_drop', 'value')
    ]
)

def pie_job(state):
    new = df[df['state'].isin(state)].dropna()
    role = new['Job Title'].dropna().value_counts().nlargest(n=10)
    role.dropna(inplace=True)
    aaa = px.pie(role,
       values = role.values, 
       names = role.index, 
       title="Top 10 Job Titles by State", 
       color=role.values,
       color_discrete_sequence=['#195b4b','#0e332a','#13473b','#1e6f5c','#61af54','#71b765','#81bf77','#91c788','#a1cf99','#b1d7ab','#c1dfbc']
                 )
    
    aaa.update_traces(opacity=0.7,
                      hovertemplate='Job Title: %{label} <br>Number of Job Postings: %{value} <extra></extra>')
                  #marker_line_color='rgb(8,48,107)',
                  #marker_line_width=1.5)
    aaa.update_layout(title_x=0.5)
    
    return aaa

@app.callback(
    Output('pie-company', 'figure'),
    [
    Input('state_drop', 'value')
    ]
)
def pie_company(state):
    new = df[df['state'].isin(state)].dropna()
    role = new['Company Name'].dropna().value_counts().nlargest(n=10)
    role.dropna(inplace=True)
    fig = px.pie(
        role,
        values = role.values,
        names = role.index,
        title="Top 10 Hiring Companies by State",
        color=role.values.astype(float),
        color_discrete_sequence=['#195b4b', '#0e332a', '#13473b', '#1e6f5c', '#61af54', '#71b765', '#81bf77', '#91c788',
                                 '#a1cf99', '#b1d7ab', '#c1dfbc']
                )
    
    fig.update_traces(opacity=0.7,
                      hovertemplate='Company: %{label} <br>Number of Job Postings: %{value} <extra></extra>')
                  #marker_line_color='rgb(8,48,107)',
                  #marker_line_width=1.5)
    fig.update_layout(title_x=0.5)
    
    return fig    
