import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
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
type_of_job_options = [dict(label=job, value=job) for job in df['Type of Job'].unique()]

size_options = [dict(label=size, value=size) for size in df['Size'].unique()]

dropdown_type = dcc.Dropdown(
        id='type_drop',
        options=type_of_job_options,
        value=['Data Scientist', 'Business Analyst', 'Data Analyst','Data Engineer'],
        multi = True
    )

dropdown_size = dcc.Dropdown(
        id='size_drop',
        options=size_options,
        value=['501 to 1000 employees', '1001 to 5000 employees',
       '1 to 50 employees', '201 to 500 employees', '51 to 200 employees',
       '10000+ employees', '5001 to 10000 employees'],
        multi=True,
    )


layout = dbc.Container([
    dbc.Row([
       dbc.Col([
            html.H2('Salary Analysis',className = 'text-center')
        ],width=12)
    ]),
   dbc.Row([
        dbc.Col([
            html.H5('Type of Job Choice',className='text-center mb-2'),
            dropdown_type
        ],width=6),
        
        dbc.Col([
            html.H5('Company Size Choice',className='text-center mb-2'),
            dropdown_size
        ],width=6)
   ]),
   
   dbc.Row([
        dbc.Col([                             
            dbc.Row([
                dbc.Card([
                    dbc.CardBody([
                    html.H4(id='top_company',className='text-white'),
                        dbc.ListGroup([
                            dbc.ListGroupItem(id='top_sal')
                        ])
                    ])
                ],color = "#4E8975",style={"height":171,"width":400})
            ],className="mb-3"),
            
              dbc.Row([
                  dbc.Card([
                    dbc.CardBody([
                        html.H4(id='sec_company', className='text-white'),
                        dbc.ListGroup([
                            dbc.ListGroupItem(id='sec_sal')
                        ])
                    ])
                ],color = "#4E8975",style={"height":171,"width":400})
            ],className='mt-3 mb-3'),
            
            dbc.Row([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='tri_company',className='text-white'),
                        dbc.ListGroup([
                            dbc.ListGroupItem(id='tri_sal')
                        ])
                    ])
                ],color = "#4E8975",style={"height":171,"width":400})
            ],className='mt-3'),
        ],width={'size': 3},className='ml-5 mb-5 mt-3'),
        
        dbc.Col([                             
            dbc.Row([
                dbc.Card([
                    dbc.CardBody([
                    html.H4(id='max_salary',className='mt-5 text-white'),
                        dbc.ListGroup([
                            dbc.ListGroupItem(id='max_salary_value')
                        ],className='mt-5')
                    ])
                ],color = "#4E8975",style={"height":171, "width":400})
            ],className="mt-3, mb-3"),
            
              dbc.Row([
                  dbc.Card([
                    dbc.CardBody([
                        html.H4(id='min_salary',className='mt-5 text-white'),
                        dbc.ListGroup([
                            dbc.ListGroupItem(id='min_salary_value')
                        ],className='mt-5')
                    ])
                ],color = "#4E8975",style={"height":171, "width":400})
            ],className="mb-3 mt-3"),
            
            dbc.Row([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='avg_salary',className='mt-5 text-white'),
                        dbc.ListGroup([
                            dbc.ListGroupItem(id='avg_salary_value')
                        ],className='mt-5')
                    ])
                ],color = "#4E8975",style={"height":171, "width":400})
            ]),
        ],width={'size': 2},className='ml-3 mt-3 mb-5'),
        
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='cloro_graph')
            ],body=True,color = "#4E8975")
        ],width=6, className='mt-5 ml-5')
   ])
   
],style={'background-color':'#f9fff0'} ,fluid = True)


"""     

        
        dbc.Col([
            dbc.Row([
                dbc.Card([
                    dcc.Graph(id='cloro_graph')
                ],body=True,color = "#4E8975")
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4(id='max_salary'),
                            dbc.ListGroup([
                                dbc.ListGroupItem(id='max_salary_value')
                            ])
                        ])
                    ],color = "#4E8975",style={"width":250})
                ],className='mr-3'),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4(id='min_salary'),
                            dbc.ListGroup([
                                dbc.ListGroupItem(id='min_salary_value')
                            ])
                        ])
                    ],color = "#4E8975",style={"width":250})
                ]),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4(id='avg_salary'),
                            dbc.ListGroup([
                                dbc.ListGroupItem(id='avg_salary_value')
                            ])
                        ])
                    ],color = "#4E8975",style={"width":200  })
                ])
            ])
        ],width={'size': 7},className='ml-5 mb-5 mt-0 mr-5')
    ])
"""



#-------------  Callbacks --------------------------------------------------------------------------------------------------

@app.callback(
    Output('cloro_graph', 'figure'),
    [
    Input('type_drop', 'value')
    ]
)

def plots(job):
    df_map = df[df['Type of Job'].isin(job)].groupby('State Code').size().to_frame().reset_index().rename(columns = {0:'Number of postings'})
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

    layout_choropleth = dict(geo=dict(scope='usa',  # default
                                      ),

                             title=dict(
                                 text='Job Postings by States per Type of Job',
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
    [
    Output('min_salary', 'children'),
    Output('min_salary_value', 'children'),
    Output('max_salary', 'children'),
    Output('max_salary_value', 'children'),
    Output('avg_salary', 'children'),
    Output('avg_salary_value', 'children')
    ],
    [
    Input('type_drop', 'value')
    ]
)

def indicator(job):
    min_sal = round(df[df['Type of Job'].isin(job)]['Avg Salary'].min(),2)
    max_sal = round(df[df['Type of Job'].isin(job)]['Avg Salary'].max(),2)
    avg_sal = round(df[df['Type of Job'].isin(job)]['Avg Salary'].mean(),2)

    return str('Minimum Salary '),\
           str(min_sal),\
           str('Maximum Salary '),\
           str(max_sal),\
           str('Average Salary '),\
           str(avg_sal)


@app.callback(
    Output('size_tree', 'figure'),
    [
    Input('size_drop', 'value')
    ]
)

def tree(size):
    series2 = df[df['Size'].isin(size)].groupby("Size")["Company Name"].value_counts()
    df2 = pd.DataFrame(series2).rename(columns={"Company Name": "count"}).reset_index()
    # removing data for which Employee Size is not given(unknown)
    df2.drop(df2.loc[df2['Size'] == "Unknown"].index, inplace=True)
    # removing data for which the number of job is only 1
    df2.drop(df2.loc[df2['count'] == 1].index, inplace=True)

    tree = px.treemap(df2, path=['Size', 'Company Name'], values='count', color='count',
                      color_continuous_scale='mint',
                      title=('Companies with their Size and Job Counts'))
    tree.update_layout(title_x=0.5)

    return tree

@app.callback(
    [
    Output('top_company', 'children'),
    Output('sec_company', 'children'),
    Output('tri_company', 'children'),
    Output('top_sal', 'children'),
    Output('sec_sal', 'children'),
    Output('tri_sal', 'children'),
    ],
    [
    Input('type_drop', 'value'),
    Input('size_drop', 'value')
    ]
)

def best_companies(job,size):
    order = df[df['Type of Job'].isin(job)][df['Size'].isin(size)].loc[:,
            ['Company Name', 'Avg Salary']].groupby('Company Name').size().reset_index().sort_values(by=0,ascending=False)
    values = df[df['Type of Job'].isin(job)][df['Size'].isin(size)].loc[:,
             ['Company Name', 'Avg Salary']].groupby('Company Name').max().reset_index()
    top = values.merge(order, left_on=['Company Name'], right_on= ['Company Name']).sort_values(by=['Avg Salary',0],ascending=False).reset_index(drop=True)
    topcomp = top['Company Name'][0]
    seccomp = top['Company Name'][1]
    tricomp = top['Company Name'][2]
    topsal = top['Avg Salary'][0]
    secsal = top['Avg Salary'][1]
    trisal = top['Avg Salary'][2]

    return str('Best Company in terms of Salary '),\
           str('Second best Company in terms of Salary '),\
           str('Third best Company in terms of Salary '),\
           str(topcomp) + ' | ' + str(topsal),\
           str(seccomp) + ' | ' + str(secsal),\
           str(tricomp) + ' | ' + str(trisal)

