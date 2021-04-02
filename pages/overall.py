import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pathlib
from app import app

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data/").resolve()
#-------------  Importing  ----------------
df = pd.read_csv(DATA_PATH.joinpath("final_df.csv"))


#------ Functions ------

def salary_analysis(df):
    data6=df.copy()
    data6['Min Salary']= data6['Min Salary'].astype('float')
    data6['Max Salary']= data6['Max Salary'].astype('float')
    data6['Average Salary']= data6['Min Salary']+((data6['Max Salary']-data6['Min Salary'])/2)
    data6_1=data6[['Type of Job','Average Salary']]
    data6_DS=data6_1[data6_1['Type of Job']=='Data Scientist']
    data6_DE=data6_1[data6_1['Type of Job']=='Data Engineer']
    data6_DA=data6_1[data6_1['Type of Job']=='Data Analyst']
    data6_BA=data6_1[data6_1['Type of Job']=='Business Analyst']
    data6_BA= data6_BA[data6_BA['Average Salary']>30]
    data6_DA= data6_DA[data6_DA['Average Salary']>30]
    # Add histogram data
    x1 = data6_BA['Average Salary']#_filtered['Average Salary']
    x2 = data6_DA['Average Salary']#_filtered['Average Salary']
    x3 = data6_DE['Average Salary']#_filtered['Average Salary']
    x4 = data6_DS['Average Salary']#_filtered['Average Salary']

    # Group data together
    hist_data = [x1, x2, x3, x4]

    group_labels = ['Business Analyst', 'Data Analyst', 'Data Engineer', 'Data Scientist']

    # Create distplot with custom bin_size
    fig = ff.create_distplot(hist_data, 
                             group_labels,
                             bin_size=5,
                             show_hist=False)
    fig.update_layout(
        title='Salary Range',
        xaxis_title="Salary in US dollars",
        yaxis_title="Frequency",
        legend_title="Type of Job",
        title_x=0.5)
        #colorscale = ['#195b4b''#61af54','#a1cf99','#c1dfbc']
        #height=500,
        #width=750

    return fig

def location_bar(df):
    location = df['Location'].value_counts().nlargest(n=10)
    fig = px.bar(
        y=location.index,
        x=location.values,
        color=location.values,
        text=location.values,
        color_continuous_scale='mint',
        orientation='h',
        title='Number of Job Postings per City',
        # height=500,
        # width=750
    )

    fig.update_traces(hovertemplate='Number of Job Postings: %{x} <br>City: %{y} <extra></extra>',
                  textposition='outside',
                  #marker_line_color='rgb(8,48,107)',
                  #marker_line_width=1.5,
                  opacity=0.7)

    fig.update_layout(#width=800,
                    showlegend=False,
                    xaxis_title="Count",
                    yaxis_title="City",
                    title="Top 10 Cities by Number of Job Postings",
                    title_x=0.5)
    fig.update(layout_coloraxis_showscale=False)
    return fig



def map(df):
    df_map = df.groupby('Region').size().to_frame().reset_index().rename(columns = {0:'Number of postings'})
    map_df = df[['State Code', 'Region']]
    cloro_df  = pd.merge(df_map,map_df).drop_duplicates().reset_index(drop = True)

    data_choropleth = dict(type='choropleth',
                            locations=cloro_df['State Code'],
                            # There are three ways to 'merge' your data with the data pre embedded in the map
                            locationmode='USA-states',
                            z= cloro_df['Number of postings'].astype(int),
                            text=cloro_df['Region'],
                            colorscale='mint'
                            )

    layout_choropleth = dict(geo=dict(scope='usa'),
                             title=dict(
                                 text='Number of Job Postings per Region',
                                 x=.5  # Title relative position according to the xaxis, range (0,1)
                                ),
                            #height=500,
                            #width=750
                            )

    fig = go.Figure(data=data_choropleth, layout=layout_choropleth)
    
    fig.update_traces(
        hovertemplate='State: %{location} <br>Region: %{text} <br>Number of postings: %{z} <extra></extra>',
        zmin = 0,
        zmax = 4000)
    
    return fig

def job_bar(df):
    job = px.bar(
        pd.DataFrame(df["Job Title"].value_counts().nlargest(10))["Job Title"],
        x="Job Title",
        y=pd.DataFrame(df["Job Title"].value_counts().nlargest(10)).index,
        orientation='h',
        color='Job Title',
        text="Job Title",
        title='Number of Job Postings per Job Title',
        color_continuous_scale='mint',
        labels=dict(x="Count", y="Job Title", color="Count")
        # height=500,
        # width=750
    )
    job.update_traces(hovertemplate='Number of Job Postings: %{x} <br>Job Title: %{y} <extra></extra>',
                  textposition='outside',
                  showlegend=False,
                  #marker_line_color='rgb(8,48,107)',
                  #marker_line_width=1.5,
                  opacity=0.7)

    job.update_layout(#width=800,
                    #showscale=False,
                    showlegend=False,
                    xaxis_title="Count",
                    yaxis_title="Job Title",
                    title="Top 10 Job Titles by Number of Job Postings",
                    title_x=0.5)
    job.update(layout_coloraxis_showscale=False)
    return job

#------Layout ------ 
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Data Science and Analytics Job Openings Interactive Dashboard", className="text-center")
        ],width=12)
    ]),
    dbc.Row([
      dbc.Col([
          html.H5("António Carvalho | Bruno Fernandes | Manuel Borges | Miguel Zina",className="text-center")
      ])
    ]),
    dbc.Row([
        html.A([
            html.H6("Over the last years, data science and analytics jobs have increased exponentially. "
                   " Having this into account, we decided to explore this area and come up with the brightest insights from it to show to all " 
                    "interested students at NOVA IMS their opportunities. Here we can visualize maps, scatter plots, pie charts and others form of graphs from all Data scientist, " 
                    "analyst and engineer jobs openings. 2.5 millions of terabytes of data is created each day and thus the importance of analyzing it is crucial. " 
                    "We hope you find this interactive Dashboard interesting and useful. ",
                   className='ml-5 mr-5 mt-5 mb-5')
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card(
                 dcc.Graph(
                    id = "graph-1",
                    figure= job_bar(df)
                    ), body = True,color = "#4E8975" 
            )
        ],width={'size':6}, className="mb-3 mt-3"),
        
        dbc.Col([
            dbc.Card(
                dcc.Graph(
                    id = "graph-2",
                    figure= map(df)
                    ), body = True,color = "#4E8975"
            )
        ],width={'size':6}, className="mb-3 mt-3"),
     ]),
                       
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dcc.Graph(
                    id = "graph-3",
                    figure= location_bar(df)
                    ), body = True, color = "#4E8975"
            )
        ],width={'size':6}, className="mb-4 mt-3"),
        
        dbc.Col([
          dbc.Card(
              dcc.Graph(
                    id = "graph-4",
                    figure= salary_analysis(df)
                    ), body = True,color = "#4E8975"
          )  
        ],width={'size':6}, className="mb-4 mt-3")
    ])
],style={'background-color':'#f9fff0'} ,fluid = True)
            
