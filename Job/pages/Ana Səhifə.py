import dash
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.dash_table import DataTable
import io

dash.register_page(__name__, path='/', name='Ana Səhifə', title='İş Vakansiyası | Ana Səhifə')

df = pd.read_excel('job_vacancies_datasets.xlsx')
df['Qoyulma Tarixi'] = pd.to_datetime(df['Qoyulma Tarixi'], format='%d.%m.%Y')

df = df[['Vəzifə', 'Şirkət', 'Yer', 'Vakansiya Link', 'Qoyulma Tarixi',
       'İş Təsviri', 'İş bacarıqları', 'Son müraciət tarixi', 'Maaş',
       'Vəzifələr', 'Məşğulluq növü', 'Yaş', 'Cins']]

df.columns = ['Vəzifə', 'Şirkət', 'Yer', 'Link', 'Qoyulma Tarixi',
       'İşin Təsviri', 'İş bacarıqları', 'Son müraciət tarixi', 'Maaş',
       'Vəzifələr', 'Məşğulluq Növü', 'Yaş', 'Cins']

layout = dbc.Container([
    dbc.Row([
        dbc.Col([], width=4),
        dbc.Col([ 
            html.Div([
                html.Div([ 
                    html.Div([ 
                        html.H1("👥İş vakansiyalarının Analizi", style={"margin-left": "10px", "margin-top": "0px"}),  # Removed extra margin
                    ], style={"display": "flex", "align-items": "center"}),

                    html.Div([ 
                        html.H3("📋 Layihə Haqqında"),
                        html.P("Bu layihə iş vakansiyalarının təhlili və araşdırılması məqsədini güdür.")
                    ], style={"margin-top": "10px"}),

                    html.Div([ 
                        html.H3("📊 Verilənlər Haqqında (Dataset)"),
                        html.Div([ 
                            html.A("İş vakansiyaları", target="_blank", style={"text-decoration": "none", "color": "white", "font-size": "26px", "font-weight": "600", "margin-left": "10px"}) 
                        ], style={"display": "flex", "align-items": "center"}), 

                        html.P("- Layihədə istifadə olunan məlumat aşağıdakı sütunları əhatə edir:"),
                        html.Ul([
                            html.Li("Vəzifə: İşin adı."),
                            html.Li("Şirkət: İşin verən şirkət."),
                            html.Li("Yer: İşin yerinə aid məlumat."),
                            html.Li("Vakansiya Link: İşin vakansiyasına link."),
                            html.Li("Qoyulma Tarixi: Vakansiyanın yerləşdirilmə tarixi."),
                            html.Li("İşin Təsviri: Vakansiya haqqında ümumi məlumat."),
                            html.Li("İş Bacarıqları: Lazım olan bacarıqlar."),
                            html.Li("Son Müraciət Tarixi: Vakansiya üçün müraciət etmə tarixi."),
                            html.Li("Maaş: İşin maaş məlumatı."),
                            html.Li("Vəzifələr: İşdəki əsas vəzifələr."),
                            html.Li("Məşğulluq Növü: Tam zamanlı, yarım zamanlı və ya müvəqqəti."),
                            html.Li("Yaş: İş üçün tələb olunan yaş aralığı."),
                            html.Li("Cins: İş üçün tələb olunan cins.")
                        ]),

                        html.Div([
                            html.H3("🔍 Verilənlərə Baxış:"),
                            DataTable(
                                id='table',
                                columns=[{"name": col, "id": col} for col in df.columns],
                                data=df.head().to_dict('records'),
                                style_table={'height': '200px', 'overflowY': 'auto'},
                                style_data={'backgroundColor': 'rgb(2, 83, 92)', 'color': 'rgb(2, 83, 92)'},
                                style_header={'backgroundColor': 'rgb(0, 44, 48)', 'color': 'white', 'fontWeight': 'bold'}
                            ),
                        ], style={"margin-top": "5px"}),

                    ], style={"margin-top": "5px"}),

                    html.Div([ 
                        html.H3("🎯 Layihənin Məqsədi"),
                        html.P("İş vakansiyalarının təhlili və müxtəlif sektorlarda mövcud olan iş imkanlarının qiymətləndirilməsi."),
                        html.P("Verilən məlumatları istifadə edərək iş bazarında tələb və təklif arasındakı əlaqələri öyrənmək.")
                    ], style={"margin-top": "10px"}),

                    html.Div([ 
                        html.H3("🌟 Layihənin Faydaları"),
                        html.P("İş axtaranlar üçün üstünlüklər: İş imkanları haqqında ətraflı məlumat əldə etmək.")
                    ], style={"margin-top": "10px"}),

                    html.Div([ 
                        html.H3("📥 İş Vakansiyası Məlumatını Yükləyin:"),
                        html.Button("Yüklə (Excel)", id="download-excel", n_clicks=0, style={
                            'backgroundColor': 'rgb(2, 83, 92)',
                            'color': 'white',
                            'border': 'none',
                            'padding': '10px 20px',
                            'marginRight': '10px',
                            'cursor': 'pointer',
                            'borderRadius': '10px'
                        }),
                        html.Button("Yüklə (CSV)", id="download-csv", n_clicks=0, style={
                            'backgroundColor': 'rgb(2, 83, 92)',
                            'color': 'white',
                            'border': 'none',
                            'padding': '10px 20px',
                            'cursor': 'pointer',
                            'borderRadius': '10px'
                        }),
                        dcc.Download(id="download-dataframe-excel"),
                        dcc.Download(id="download-dataframe-csv"),
                    ], style={"margin-top": "10px"}),

                    html.Div([ 
                        html.H3("💡 Daha ətraflı məlumat üçün əlaqə saxlayın."),
                        html.P(["📧 Email: ", html.A("riyadehmedov03@gmail.com", href="mailto:riyadehmedov03@gmail.com", style={"color": "#007BFF", "textDecoration": "none"})]),
                        html.P("📞 Telefon: +994 55 551-98-18")
                    ], style={"margin-top": "10px"})
                ])
            ]) 

        ], width=8),
        dbc.Col([], width=1) 
    ]),

], fluid=True, style={"margin-top": "0px"})

@callback(
    Output("download-dataframe-excel", "data"),
    Input("download-excel", "n_clicks"),
    prevent_initial_call=True
)
def download_excel(n_clicks):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    output.seek(0)
    return dcc.send_bytes(output.read(), "job_vacancies.xlsx", index = False)

@callback(
    Output("download-dataframe-csv", "data"),
    Input("download-csv", "n_clicks"),
    prevent_initial_call=True
)
def download_csv(n_clicks):
    return dcc.send_data_frame(df.to_csv, "job_vacancies.csv", index=False)
