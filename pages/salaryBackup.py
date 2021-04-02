import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
#from utils import Header
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pathlib


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

server = app.server



PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../").resolve()
#-------------  Importing  ----------------
df = pd.read_csv(DATA_PATH.joinpath("final_df.csv"))

#-------------  Interactive components ----------------
type_of_job_options = [dict(label=job, value=job) for job in df['Type of Job'].unique()]

size_options = [dict(label=size, value=size) for size in df['Size'].unique()]

dropdown_type = dcc.Dropdown(
        id='type_drop',
        options=type_of_job_options,
        value=['Data Scientist', 'Business Analyst', 'Data Analyst',
       'Data Engineer'],
        multi=True
    )

dropdown_size = dcc.Dropdown(
        id='size_drop',
        options=size_options,
        value=['501 to 1000 employees', '1001 to 5000 employees',
       '1 to 50 employees', '201 to 500 employees', '51 to 200 employees',
       '10000+ employees', '5001 to 10000 employees'],
        multi=True
    )


app.layout = html.Div(
        [
            #row 1
            html.Div([
                html.Div(
                    [
                        html.Br(),
                        html.Div(
                            [
                            html.Label('Type of Job Choice'),
                            ], style={"height": "10%", 'background-color': '#228B22', 'font-weight': 'bolder',
                              'text-align': 'center', 'vertical-align': 'bottom', 'color': 'white'}, className="row",
                        ),
                        dropdown_type,

                        html.Br(),


                        html.Div(
                            [
                            html.Label('Company Size Choice'),
                            ], style={"height": "10%", 'background-color': '#228B22','font-weight':'bolder','text-align': 'center','vertical-align': 'middle','color':'white'}, className="row",
                        ),

                        dropdown_size,

                        html.Br(),
                    ],style={"width":"20%"}, className = ""),
                html.Div(
                    []
                    , style={"width": "5%"}, className=""),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label(id='min_salary'),
                            ], style={"height": "5%", 'background-color': '#228B22','font-weight':'bolder','text-align': 'center','vertical-align': 'middle','color':'white'}, className="row",
                        ),
                        html.Div(
                            []
                            , style={"height": "5%"}, className=""),
                        html.Div(
                            [
                                html.Label(id='max_salary'),
                            ], style={"height": "5%", 'background-color': '#228B22','font-weight':'bolder','text-align': 'center','vertical-align': 'middle','color':'white'}, className="row",
                        ),
                        html.Div(
                            []
                            , style={"height": "5%"}, className=""),
                        html.Div(
                            [
                                html.Label(id='avg_salary'),
                            ], style={"height": '5%', 'background-color': '#228B22','font-weight':'bolder','text-align': 'center','vertical-align': 'middle','color':'white'}, className="row"
                        ),
                        html.Div(
                            []
                            , style={"height": "5%"}, className=""),
                        ], style={"width": "20%"}, className=""),
                html.Div(
                    []
                , style={"width": "5%"}, className=""),
                html.Div(
                    [
                        dcc.Graph(id='cloro_graph')
                    ],style={"width":"60%"}, className = ""),
        ], style={"display": "flex"}),
            html.Div(
                [
                    dcc.Graph(id='size_tree')
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Label(id='top_company'),
                    html.Label(id='top_sal')
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Label(id='sec_company'),
                    html.Label(id='sec_sal')
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Label(id='tri_company'),
                    html.Label(id='tri_sal')
                ],
                className="row",
            ),
        ],
        className="page",
    )

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
                            colorscale='Greens'
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
    [
    Output('min_salary', 'children'),
    Output('max_salary', 'children'),
    Output('avg_salary', 'children')
    ],
    [
    Input('type_drop', 'value')
    ]
)

def indicator(job):
    df_sal = df[df['Type of Job'].isin(job)].describe().loc['mean',:]
    min_sal = round(df_sal[1],2)
    max_sal = round(df_sal[2],2)
    avg_sal = round(df_sal[3],2)

    return str('Average Minimum Salary: ')+ str(min_sal),\
           str('Average Maximum Salary:')+ str(max_sal),\
           str('Average Salary:')+ str(avg_sal),


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

    return str('Best Company in terms of Salary: ') + str(topcomp),\
           str('Second best Company in terms of Salary: ') + str(seccomp),\
           str('Third best Company in terms of Salary: ') + str(tricomp),\
           str(' | Salary: ') + str(topsal),\
           str(' | Salary: ') + str(secsal),\
           str(' | Salary: ') + str(trisal)

if __name__ == '__main__':
    app.run_server(debug=True)
