import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from pages import analysisLocation,overall,analysisCompany,analysisSalary


nav_item_overall = dbc.NavItem(dbc.NavLink("Overall ", href="/overall", active="exact"))
nav_item_location = dbc.NavItem(dbc.NavLink("Location Analysis ", href="/analysis_location", active="exact"))
nav_item_salary = dbc.NavItem(dbc.NavLink("Salary Analysis ", href="/analysis_salary", active="exact"))
nav_item_job = dbc.NavItem(dbc.NavLink("Company Analysis ", href="/analysis_company", active="exact"))

logo = dbc.Navbar(
    dbc.Container(
        [
            
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=app.get_asset_url("glassdoor-stacked-rgb.png"), height="70px", className="mr-auto")),
                    ],
                    align="center",
                    className = 'align-self-center',
                    no_gutters=True,
                ),
            ),
            
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    [nav_item_overall, nav_item_location, nav_item_salary, nav_item_job], 
                    className="ml-auto", 
                    navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ],fluid=True,
    ),
   
    color="#91c788",
    dark=True,
    className="mb-2 mr-0",
)

content = html.Div(id="page-content")

app.layout = html.Div(
    [dcc.Location(id="url"), logo, content],
)

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/":
        return overall.layout
    elif pathname == '/analysis_salary':
        return analysisSalary.layout
    elif pathname == '/analysis_location':
        return analysisLocation.layout
    elif pathname == '/analysis_company':
        return analysisCompany.layout
    else:
        return overall.layout


if __name__ == '__main__':
    app.run_server(debug=True)

