from dash import html
import dash_bootstrap_components as dbc
import dash

_nav = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src="/assets/logo.png", className="logo", style={"height": "90px"})
            ], style={"margin-right": "140px", "margin-bottom": "30px"})
        ], width=2, align="center"),

        dbc.Col([html.H1(['İş Vakansiyaları'], className='app-brand', style={"font-weight": "bold", "font-size": "24px", "margin-left": "40px"})], width=2)
    ], align="center"),  # Use align center for vertical centering

    dbc.Row([
        dbc.Nav(
            [dbc.NavLink(page["name"], active='exact', href=page["path"]) for page in dash.page_registry.values()],
            vertical=True, pills=True, class_name='my-nav'
        )
    ])
])
