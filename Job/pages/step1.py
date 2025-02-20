from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import dash

dash.register_page(__name__, name='Məlumatın təhlili', title='İş Vakansiyası | Məlumatın təhlili')

df = pd.read_excel('job_vacancies_datasets.xlsx')

df['Qoyulma Tarixi'] = pd.to_datetime(df['Qoyulma Tarixi'], format='%d.%m.%Y')
df['Il'] = df['Qoyulma Tarixi'].dt.year
df['Ay'] = df['Qoyulma Tarixi'].dt.month

def create_visualizations(filtered_df):
    # Vacancy Count by Year and Month
    grouped_data = filtered_df.groupby(['Il', 'Ay']).size().reset_index(name='Vakansiya Sayı')
    grouped_data['Tarix'] = pd.to_datetime(grouped_data['Il'].astype(int).astype(str) + '-' + grouped_data['Ay'].astype(int).astype(str))
    fig1 = px.line(
        grouped_data,
        x='Tarix',
        y='Vakansiya Sayı',
        title='İl və aylara görə vakansiya Sayı',
        labels={'Tarix': 'Date (Year-Month)', 'Vakansiya Sayı': 'Vacancy Count'},
        markers=True
    )
    fig1.update_traces(
        line=dict(color='white'),  
        marker=dict(color='white') 
    )
    fig1.update_layout(
        margin=dict(l=80, r=20),
        xaxis_title='Date (Year-Month)',
        yaxis_title='Vacancy Count',
        plot_bgcolor='rgb(0, 129, 143)', 
        paper_bgcolor='rgb(0, 129, 143)', 
        xaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'),  
            tickfont=dict(color='white')  
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'),
            tickfont=dict(color='white')  
        ),
        title_font=dict(color='white')  
    )

    # Average Vacancy Count by Month
    average_vacancy_count = grouped_data.groupby('Ay')['Vakansiya Sayı'].mean().reset_index()
    fig2 = px.line(
        average_vacancy_count,
        x='Ay',
        y='Vakansiya Sayı',
        title='Aylara görə ortalama vakansiya sayı',
        labels={'Ay': 'Tarix (Ay)', 'Vakansiya Sayı': 'Ortalama Vakansiya Sayı'},
        markers=True
    )
    fig2.update_traces(
        line=dict(color='white'), 
        marker=dict(color='white')  
    )
    fig2.update_layout(
        margin=dict(l=80, r=20), 
        xaxis_title='Date (Month)',
        yaxis_title='Average Vacancy Count',
        plot_bgcolor='rgb(0, 129, 143)', 
        paper_bgcolor='rgb(0, 129, 143)', 
        xaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'),  
            tickfont=dict(color='white')  
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'), 
            tickfont=dict(color='white')  
        ),
        title_font=dict(color='white')  
    )

    # Total Vacancy Count by Year
    total_year = grouped_data.groupby('Il')['Vakansiya Sayı'].sum().reset_index()
    fig3 = px.line(
        total_year,
        x='Il',
        y='Vakansiya Sayı',
        title='İllərə görə toplam vakansiya sayı',
        labels={'Il': 'Tarix (İl)', 'Vakansiya Sayı': 'Toplam Vakansiya Sayı'},
        markers=True
    )
    fig3.update_traces(
        line=dict(color='white'),  
        marker=dict(color='white')  
    )
    fig3.update_layout(
        margin=dict(l=80, r=20),  
        xaxis_title='Date (Year)',
        yaxis_title='Total Vacancy Count',
        plot_bgcolor='rgb(0, 129, 143)',  
        paper_bgcolor='rgb(0, 129, 143)',  
        xaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'),  
            tickfont=dict(color='white')  
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'), 
            tickfont=dict(color='white')  
        ),
        title_font=dict(color='white')  
    )

    # Average Vacancy Count by Season
    grouped_data['Fəsil'] = grouped_data['Ay'].apply(
        lambda x: 'Qış' if x in [12, 1, 2] else
                  'Yaz' if x in [3, 4, 5] else
                  'Yay' if x in [6, 7, 8] else
                  'Payız' if x in [9, 10, 11] else 'Unknown'
    )
    average_vacancy_count_season = grouped_data.groupby('Fəsil')['Vakansiya Sayı'].mean().reset_index()
    fig4 = px.line(
        average_vacancy_count_season,
        x='Fəsil',
        y='Vakansiya Sayı',
        title='Fəsillər üzrə ortalama vakansiya sayı',
        labels={'Fəsil': 'Fəsil', 'Vakansiya Sayı': 'Vakansiya Sayı'},
        markers=True
    )
    fig4.update_traces(
        line=dict(color='white'),  
        marker=dict(color='white')  
    )
    fig4.update_layout(
        margin=dict(l=80, r=20),  
        xaxis_title='Fəsil',
        yaxis_title='Average Vacancy Count',
        plot_bgcolor='rgb(0, 129, 143)',  
        paper_bgcolor='rgb(0, 129, 143)',  
        xaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'),  
            tickfont=dict(color='white')  
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'), 
            tickfont=dict(color='white')  
        ),
        title_font=dict(color='white')  
    )

    # Vacancy Count by Position
    grouped_data_position = filtered_df.groupby(['Il', 'Ay', 'Vəzifə']).size().reset_index(name='Vakansiya Sayı')
    grouped_data_position['Tarix'] = pd.to_datetime(grouped_data_position['Il'].astype(int).astype(str) + '-' + grouped_data_position['Ay'].astype(int).astype(str))

    fig5 = px.line(
        grouped_data_position,
        x='Tarix',
        y='Vakansiya Sayı',
        color='Vəzifə',
        title='Vəzifəyə görə vakansiya sayı',
        labels={'Tarix': 'Date (Year-Month)', 'Vakansiya Sayı': 'Vacancy Count'},
        markers=True
    )

    # Apply layout and customization
    fig5.update_layout(
        margin=dict(l=80, r=20),  
        xaxis_title='Date (Year-Month)',
        yaxis_title='Vacancy Count',
        plot_bgcolor='rgb(0, 129, 143)',  
        paper_bgcolor='rgb(0, 129, 143)',  
        title_font=dict(color='white'),  
        font=dict(color='white'),  
        xaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'),
            tickfont=dict(color='white')
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'),
            tickfont=dict(color='white')
        ),
        showlegend=False  
    )


    # Percentage Growth by Position
    grouped_data_position_growth = filtered_df.groupby(['Il', 'Vəzifə']).size().reset_index(name='Vakansiya Sayı')
    grouped_data_position_growth = grouped_data_position_growth.sort_values(by=['Vəzifə', 'Il'])
    grouped_data_position_growth['Faiz Artımı (%)'] = grouped_data_position_growth.groupby('Vəzifə')['Vakansiya Sayı'].pct_change() * 100
    grouped_data_position_growth_clean = grouped_data_position_growth.dropna(subset=['Faiz Artımı (%)'])

    fig6 = px.line(
        grouped_data_position_growth_clean,
        x='Il',
        y='Faiz Artımı (%)',
        color='Vəzifə',
        title='Vakansiya Saylarının Faiz Artımı (Vəzifəyə görə)',
        labels={'Il': 'Tarix (İl)', 'Faiz Artımı (%)': 'Faiz Artımı (%)'},
        markers=True
    )

    
    fig6.update_layout(
        margin=dict(l=80, r=20),  
        xaxis_title='Date (Year)',
        yaxis_title='Percentage Growth (%)',
        plot_bgcolor='rgb(0, 129, 143)',  
        paper_bgcolor='rgb(0, 129, 143)',  
        title_font=dict(color='white'),  
        font=dict(color='white'),  
        xaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'),
            tickfont=dict(color='white')
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'),
            tickfont=dict(color='white')
        ),
        showlegend=False  
    )
    # Vacancy Count by Company
    grouped_data_company = filtered_df.groupby(['Il', 'Ay', 'Şirkət']).size().reset_index(name='Vakansiya Sayı')
    grouped_data_company['Tarix'] = pd.to_datetime(grouped_data_company['Il'].astype(int).astype(str) + '-' + grouped_data_company['Ay'].astype(int).astype(str))

    fig7 = px.line(
        grouped_data_company,
        x='Tarix',
        y='Vakansiya Sayı',
        color='Şirkət',
        title='Şirkətə görə vakansiya sayı',
        labels={'Tarix': 'Date (Year-Month)', 'Vakansiya Sayı': 'Vacancy Count'},
        markers=True
    )

    # Update layout and legend properties
    fig7.update_layout(
        margin=dict(l=80, r=20),  
        xaxis_title='Date (Year-Month)',
        yaxis_title='Vacancy Count',
        plot_bgcolor='rgb(0, 129, 143)',  
        paper_bgcolor='rgb(0, 129, 143)',  
        title_font=dict(color='white'),  
        font=dict(color='white'),  
        xaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'),
            tickfont=dict(color='white')
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'),
            tickfont=dict(color='white')
        ),
        showlegend=False
    )


    # Percentage Growth by Company
    grouped_data_company_growth = filtered_df.groupby(['Il', 'Şirkət']).size().reset_index(name='Vakansiya Sayı')
    grouped_data_company_growth = grouped_data_company_growth.sort_values(by=['Şirkət', 'Il'])
    grouped_data_company_growth['Faiz Artımı (%)'] = grouped_data_company_growth.groupby('Şirkət')['Vakansiya Sayı'].pct_change() * 100
    grouped_data_company_growth_clean = grouped_data_company_growth.dropna(subset=['Faiz Artımı (%)'])

    fig8 = px.line(
        grouped_data_company_growth_clean,
        x='Il',
        y='Faiz Artımı (%)',
        color='Şirkət',
        title='Vakansiya Saylarının Faiz Artımı (Şirkətə görə)',
        labels={'Il': 'Tarix (İl)', 'Faiz Artımı (%)': 'Faiz Artımı (%)'},
        markers=True
    )

    # Set layout and line properties
    fig8.update_traces(
        line=dict(width=2),  
        marker=dict(size=5)  
    )

    fig8.update_layout(
        margin=dict(l=80, r=20),  
        xaxis_title='Date (Year)',
        yaxis_title='Percentage Growth (%)',
        plot_bgcolor='rgb(0, 129, 143)', 
        paper_bgcolor='rgb(0, 129, 143)', 
        title_font=dict(color='white'),  
        font=dict(color='white'),  
        xaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'),
            tickfont=dict(color='white')
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'),
            tickfont=dict(color='white')
        ),
        showlegend=False
    )

    # Average Vacancy Period
    filtered_df['Son müraciət tarixi'] = pd.to_datetime(
        filtered_df['Son müraciət tarixi'], 
        format='%d.%m.%Y',  
        errors='coerce'    
    )
    filtered_df['Vakansiya müddəti'] = (filtered_df['Son müraciət tarixi'] - filtered_df['Qoyulma Tarixi']).dt.days
    result_df = filtered_df[filtered_df['Vakansiya müddəti'] > 5] 
    average_vacancy_period = result_df.groupby(['Il', 'Ay'])['Vakansiya müddəti'].mean().reset_index()
    average_vacancy_period['Tarix'] = pd.to_datetime(average_vacancy_period['Il'].astype(int).astype(str) + '-' + average_vacancy_period['Ay'].astype(int).astype(str))
    fig9 = px.line(
        average_vacancy_period,
        x='Tarix',
        y='Vakansiya müddəti',
        title='Ortalama vakansiya müddəti',
        labels={'Tarix': 'Date (Year-Month)', 'Vakansiya müddəti': 'Average Vacancy Period'},
        markers=True
    )
    fig9.update_traces(
        line=dict(color='white'),  
        marker=dict(color='white')  
    )
    fig9.update_layout(
        margin=dict(l=80, r=20),  
        xaxis_title='Date (Year-Month)',
        yaxis_title='Average Vacancy Period (Days)',
        plot_bgcolor='rgb(0, 129, 143)',  
        paper_bgcolor='rgb(0, 129, 143)',  
        xaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'),  
            tickfont=dict(color='white')  
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'), 
            tickfont=dict(color='white')  
        ),
        title_font=dict(color='white')  
    )

    # Average Salary
    filtered_df['Maaş_l'] = filtered_df['Maaş'].apply(lambda x: str(x).split('-')[0])
    filtered_df['Maaş_u'] = filtered_df['Maaş'].apply(lambda x: str(x).split('-')[-1])
    filtered_df['Maaş_l'] = pd.to_numeric(filtered_df['Maaş_l'], errors='coerce')
    filtered_df['Maaş_u'] = pd.to_numeric(filtered_df['Maaş_u'], errors='coerce')
    result_df = filtered_df[filtered_df['Maaş_l'] > 100]
    result_df.loc[:, 'Maaş_avg'] = result_df.apply(lambda x: (x['Maaş_l'] + x['Maaş_u']) / 2, axis=1)
    # result_df['Maaş_avg'] = result_df.apply(lambda x: (x['Maaş_l'] + x['Maaş_u']) / 2, axis=1)
    average_salary = result_df.groupby(['Il', 'Ay'])['Maaş_avg'].mean().reset_index()
    average_salary['Tarix'] = pd.to_datetime(average_salary['Il'].astype(int).astype(str) + '-' + average_salary['Ay'].astype(int).astype(str))
    fig10 = px.line(
        average_salary,
        x='Tarix',
        y='Maaş_avg',
        title='İllər və Aylar üzrə Ortalama əmək haqqı',
        labels={'Tarix': 'Date (Year-Month)', 'Maaş_avg': 'Average Salary'},
        markers=True
    )
    fig10.update_traces(
        line=dict(color='white'),  
        marker=dict(color='white')  
    )
    fig10.update_layout(
        margin=dict(l=80, r=20),  
        xaxis_title='Date (Year-Month)',
        yaxis_title='Average Salary',
        plot_bgcolor='rgb(0, 129, 143)',  
        paper_bgcolor='rgb(0, 129, 143)',  
        xaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'),  
            tickfont=dict(color='white')  
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'), 
            tickfont=dict(color='white')  
        ),
        title_font=dict(color='white')  
    )

    # Employment Type Distribution
    grouped_data_employment = filtered_df.groupby(['Il', 'Ay', 'Məşğulluq növü']).size().reset_index(name='Count')
    grouped_data_employment['Tarix'] = pd.to_datetime(grouped_data_employment['Il'].astype(int).astype(str) + '-' + grouped_data_employment['Ay'].astype(int).astype(str))
    grouped_data_employment['Percentage'] = grouped_data_employment.groupby('Tarix')['Count'].transform(lambda x: round(x / x.sum() * 100, 2))

    fig11 = px.pie(
        grouped_data_employment,
        names='Məşğulluq növü',  
        values='Count',  
        title='Məşğulluq növünə görə paylanma',
        labels={'Məşğulluq növü': 'Employment Type', 'Count': 'Row Count'},
        color_discrete_sequence=px.colors.sequential.Tealgrn 
    )

    fig11.update_layout(
        plot_bgcolor='rgb(0, 129, 143)', 
        paper_bgcolor='rgb(0, 129, 143)',  
        title_font=dict(color='white'),  
        font=dict(color='white') 
    )

    # Average Age
    filtered_df['Yaş_l'] = filtered_df['Yaş'].apply(lambda x: str(x).split('-')[0])
    filtered_df['Yaş_u'] = filtered_df['Yaş'].apply(lambda x: str(x).split('-')[-1])
    filtered_df['Yaş_l'] = pd.to_numeric(filtered_df['Yaş_l'], errors='coerce').fillna(0).astype(int)
    filtered_df['Yaş_u'] = pd.to_numeric(filtered_df['Yaş_u'], errors='coerce').fillna(0).astype(int)
    result_df = filtered_df[filtered_df['Yaş_l'] > 18]
    result_df['Yaş_avg'] = result_df.apply(lambda x: (x['Yaş_l'] + x['Yaş_u']) / 2, axis=1)
    average_age = result_df.groupby(['Il', 'Ay'])['Yaş_avg'].mean().reset_index()
    average_age['Tarix'] = pd.to_datetime(average_age['Il'].astype(int).astype(str) + '-' + average_age['Ay'].astype(int).astype(str))
    fig12 = px.line(
        average_age,
        x='Tarix',
        y='Yaş_avg',
        title='Ortalama yaş',
        labels={'Tarix': 'Date (Year-Month)', 'Yaş_avg': 'Average Age'},
        markers=True
    )
    fig12.update_traces(
        line=dict(color='white')  
    )
    fig12.update_layout(
        margin=dict(l=80, r=20),  
        xaxis_title='Date (Year-Month)',
        yaxis_title='Average Age',
        plot_bgcolor='rgb(0, 129, 143)',  
        paper_bgcolor='rgb(0, 129, 143)',  
        xaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'),  
            tickfont=dict(color='white')  
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'), 
            tickfont=dict(color='white')  
        ),
        title_font=dict(color='white')  
    )

    # Gender Distribution
    count_cins = filtered_df.groupby(['Il', 'Ay', 'Cins']).size().reset_index(name='Count')
    count_cins = count_cins[count_cins['Cins'].isin(['Qadın', 'Kişi'])]
    count_cins['Tarix'] = pd.to_datetime(count_cins['Il'].astype(int).astype(str) + '-' + count_cins['Ay'].astype(int).astype(str))
    count_cins['Percentage'] = count_cins.groupby('Tarix')['Count'].transform(lambda x: round(x / x.sum() * 100, 2))

    fig13 = px.bar(
        count_cins,
        x='Tarix',
        y='Count',
        color='Cins',
        title='Cinsə görə paylanma',
        labels={'Tarix': 'Date (Year-Month)', 'Percentage': 'Percentage of Row Count'},
        text='Percentage',
        barmode='stack',
        color_discrete_map={'Kişi': 'blue', 'Qadın': 'red'}  
    )

    fig13.update_layout(
        margin=dict(l=80, r=20),  
        xaxis_title='Date (Year-Month)',
        yaxis_title='Count',
        plot_bgcolor='rgb(0, 129, 143)',  
        paper_bgcolor='rgb(0, 129, 143)',  
        xaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'),  
            tickfont=dict(color='white')  
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'), 
            tickfont=dict(color='white')  
        ),
        title_font=dict(color='white')  
    )


    # Average Salary by Gender
    result_df = filtered_df[filtered_df['Maaş_l'] > 100]
    result_df.loc[:, 'Maaş_avg'] = result_df.apply(lambda x: (x['Maaş_l'] + x['Maaş_u']) / 2, axis=1)
    # result_df['Maaş_avg'] = result_df.apply(lambda x: (x['Maaş_l'] + x['Maaş_u']) / 2, axis=1)
    count_cins_salary = result_df.groupby(['Il', 'Ay', 'Cins'])['Maaş_avg'].mean().reset_index()
    count_cins_salary = count_cins_salary[count_cins_salary['Cins'].isin(['Qadın', 'Kişi'])]
    count_cins_salary['Tarix'] = pd.to_datetime(count_cins_salary['Il'].astype(int).astype(str) + '-' + count_cins_salary['Ay'].astype(int).astype(str))
    fig14 = px.bar(
        count_cins_salary,
        x='Tarix',
        y='Maaş_avg',
        color='Cins',
        title='Cinsə görə ortalama əmək haqqı',
        labels={'Tarix': 'Date (Year-Month)', 'Maaş_avg': 'Average Salary'},
        barmode='group',
        color_discrete_map={'Kişi': 'blue', 'Qadın': 'red'}  
    )
    fig14.update_layout(
        margin=dict(l=80, r=20),  
        xaxis_title='Date (Year-Month)',
        yaxis_title='Average Salary',
        plot_bgcolor='rgb(0, 129, 143)',  
        paper_bgcolor='rgb(0, 129, 143)',  
        xaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'),  
            tickfont=dict(color='white')  
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0)',  
            title_font=dict(color='white'), 
            tickfont=dict(color='white')  
        ),
        title_font=dict(color='white')  
    )

    return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, fig11, fig12, fig13, fig14

# Get unique values for each filter
job_titles = df['Vəzifə'].unique().tolist()
companies = df['Şirkət'].unique().tolist()
locations = df['Yer'].unique().tolist()
salaries = df['Maaş'].unique().tolist()
employment_types = df['Məşğulluq növü'].unique().tolist()
genders = df['Cins'].unique().tolist()
years = df['Il'].unique().tolist()

# Layout Setup
layout = dbc.Container([ 
    dbc.Row([ 
        dbc.Col(width=4),  
        dbc.Col([ 
            html.H1("Məlumatın təhlili", className="mb-4 text-right"),  
            html.Hr(),
            dcc.Dropdown(
                id='job-title-filter',
                options=[{'label': title, 'value': title} for title in job_titles],
                multi=True,
                placeholder="Vəzifə seçin",
                searchable=True,
                style={'margin-bottom': '15px'} 
            ),
            dcc.Dropdown(
                id='company-filter',
                options=[{'label': company, 'value': company} for company in companies],
                multi=True,
                placeholder="Şirkət seçin",
                searchable=True,
                style={'margin-bottom': '15px'}  
            ),
            dcc.Dropdown(
                id='year-filter',
                options=[{'label': year, 'value': year} for year in years],
                multi=True,
                placeholder="İl seçin",
                searchable=True,
                style={'margin-bottom': '15px'}  
            ),
            dcc.Dropdown(
                id='location-filter',
                options=[{'label': location, 'value': location} for location in locations],
                multi=True,
                placeholder="Yer seçin",
                searchable=True,
                style={'margin-bottom': '15px'} 
            ),
            dcc.Dropdown(
                id='salary-filter',
                options=[{'label': salary, 'value': salary} for salary in salaries],
                multi=True,
                placeholder="Əmək haqqı seçin",
                searchable=True,
                style={'margin-bottom': '15px'}
            ),
            dcc.Dropdown(
                id='employment-type-filter',
                options=[{'label': emp_type, 'value': emp_type} for emp_type in employment_types],
                multi=True,
                placeholder="Məşğulluq növü seçin",
                searchable=True,
                style={'margin-bottom': '15px'} 
            ),
            dcc.Dropdown(
                id='gender-filter',
                options=[{'label': gender, 'value': gender} for gender in genders],
                multi=True,
                placeholder="Cins seçin",
                searchable=True,
                style={'margin-bottom': '15px'}  
            ),
            # Graphs
            html.H3("İl və aylara görə vakansiya sayı", className="mb-2"),
            html.P("Bu qrafik hər il və ayda yerləşdirilən vakansiyaların ümumi sayını göstərir."),
            dcc.Graph(id='graph-id', style={'margin-left': '0px', 'margin-right': '0px'}),  # Graph to be updated by callback
            html.P("Trend artan yöndədir, lakin 2020-ci ildə kəskin düşüş var bunun da səbəbi virusun ölkəmizdə başlaması ilə əlaqəlidir."),

            html.H3("Aylara görə ortalama vakansiya sayı", className="mt-4"),
            html.P("Bu qrafik hər ay üçün ortalama vakansiya sayını göstərir."),
            dcc.Graph(id='graph-average-vacancy'),
            html.P("Görünür ki, ilin əvvəli və ortalarında daha çox vakansiya mövcüddur. Mart ayında düşüş müşahidə edilib."),
            
            html.H3("İllərə görə toplam vakansiya sayı", className="mt-4"),
            html.P("Bu qrafik hər il üçün toplam vakansiya sayını göstərir."),
            dcc.Graph(id='graph-total-vacancy'),
            html.P("İllərə görə toplam vakansiya sayına baxsaq artan trend görə bilərik. 2020-ci ildə düşüş görünür."),
            
            html.H3("Fəsillər üzrə ortalama vakansiya sayı", className="mt-4"),
            html.P("Bu qrafik hər fəsil üçün ortalama vakansiya sayını göstərir."),
            dcc.Graph(id='graph-average-vacancy-season'),
            html.P("Fəsillər üzrə ortalama vakansiya sayına baxsaq, payız aylarında daha çox artım olduğu görünür.  "),

            html.H3("Vəzifəyə görə vakansiya sayı", className="mt-4"),
            html.P("Bu qrafik hər vəzifə üçün vakansiya sayını göstərir."),
            dcc.Graph(id='graph-vacancy-by-position'),
            html.P("Vəzifələr üzrə vakansiya sayına baxsaq, mühasib vakansiyası üstünlük təşkil edir."),

            html.H3("Vakansiya Saylarının Faiz Artımı (Vəzifəyə görə)", className="mt-4"),
            html.P("Bu qrafik hər vəzifə üçün vakansiya saylarının faiz artımını göstərir."),
            dcc.Graph(id='graph-percentage-growth-position'),
            html.P("Faizin uniform olaraq artması bu vakansiyanın bazarda sabitliyinin göstəricisidir."),

            html.H3("Şirkətə görə vakansiya sayı", className="mt-4"),
            html.P("Bu qrafik hər şirkət üçün vakansiya sayını göstərir."),
            dcc.Graph(id='graph-vacancy-by-company'),
            html.P("Adətən bank sektorundan daha çox vakansiyalar paylaşılıb."),

            html.H3("Vakansiya Saylarının Faiz Artımı (Şirkətə görə)", className="mt-4"),
            html.P("Bu qrafik hər şirkət üçün vakansiya saylarının faiz artımını göstərir."),
            dcc.Graph(id='graph-percentage-growth-company'),

            html.H3("Ortalama vakansiya müddəti", className="mt-4"),
            html.P("Bu qrafik ortalama vakansiya müddətini göstərir."),
            dcc.Graph(id='graph-average-vacancy-period'),
            html.P("Ortalama vakansiya müddətinə baxsaq 25-30 gün arasında dəyişir. Son ildə isə 15 gün aralığında olub."),

            html.H3("Ortalama əmək haqqı", className="mt-4"),
            html.P("Bu qrafik ortalama əmək haqqını göstərir."),
            dcc.Graph(id='graph-average-salary'),
            html.P("Ortalama əmək haqqı 2019-cu ildən sonra 800-1000 aralığında dəyişir və artan yöndədir. Düşünsək ki ondan əvvəlki illərdə vakansiya sayı az olub və bu səbəbdən dəqiq rəqəmlər olmaya bilər. Sample sayı nə qədər çox olarsa bir o qədər daha doğru nəticəyə çata bilərik."),

            html.H3("Məşğulluq növünə görə paylanma", className="mt-4"),
            html.P("Bu qrafik məşğulluq növünə görə paylanmanı göstərir."),
            dcc.Graph(id='graph-employment-type-distribution'),
            html.P("Məşğulluq növünə görə vakansiyaları təhlil etsək, vakansiyaların 99.2%-i tam ştat işə aiddir."),

            html.H3("Ortalama yaş", className="mt-4"),
            html.P("Bu qrafik ortalama yaşı göstərir."),
            dcc.Graph(id='graph-average-age'),
            html.P("Qrafikdən görünür ki, şirkətlər vakansiyaları üçün tələb etdikləri ortalama yaş artan tendensiya göstərir."),

            html.H3("Cinsə görə paylanma", className="mt-4"),
            html.P("Bu qrafik cinsə görə paylanmanı göstərir."),
            dcc.Graph(id='graph-gender-distribution'),
            html.P("Kişi cinsinə nisbətən, qadınlar üçün daha çox vakansiya şansının olduğunu görünür. Burda digər məqam var ki, bəzi vakansiyalarda bu məhdudiyyət yoxdur."),

            html.H3("Cinsə görə ortalama əmək haqqı", className="mt-4"),
            html.P("Bu qrafik cinsə görə ortalama əmək haqqını göstərir."),
            dcc.Graph(id='graph-average-salary-gender'),
            html.P("Aydın şəkildə görünür ki, kişi cinsindən olan işçilərə qadınlara nisbətdə daha çox əmək haqqı verilir."),
        ], width=8)  # Content column width
    ])
], fluid=True)

@callback(
    [Output('graph-id', 'figure'),
     Output('graph-average-vacancy', 'figure'),
     Output('graph-total-vacancy', 'figure'),
     Output('graph-average-vacancy-season', 'figure'),
     Output('graph-vacancy-by-position', 'figure'),
     Output('graph-percentage-growth-position', 'figure'),
     Output('graph-vacancy-by-company', 'figure'),
     Output('graph-percentage-growth-company', 'figure'),
     Output('graph-average-vacancy-period', 'figure'),
     Output('graph-average-salary', 'figure'),
     Output('graph-employment-type-distribution', 'figure'),
     Output('graph-average-age', 'figure'),
     Output('graph-gender-distribution', 'figure'),
     Output('graph-average-salary-gender', 'figure')],
    [Input('job-title-filter', 'value'),
     Input('company-filter', 'value'),
     Input('year-filter', 'value'),
     Input('location-filter', 'value'),
     Input('salary-filter', 'value'),
     Input('employment-type-filter', 'value'),
     Input('gender-filter', 'value')]
)

def update_graph(selected_job_titles, selected_companies, selected_year, selected_locations, selected_salaries, selected_emp_types, selected_genders):

    filtered_df = df.copy()

    if selected_job_titles:
        filtered_df = filtered_df[filtered_df['Vəzifə'].isin(selected_job_titles)]
    if selected_companies:
        filtered_df = filtered_df[filtered_df['Şirkət'].isin(selected_companies)]
    if selected_year:
        filtered_df = filtered_df[filtered_df['Il'].isin(selected_year)]
    if selected_locations:
        filtered_df = filtered_df[filtered_df['Yer'].isin(selected_locations)]
    if selected_salaries:
        filtered_df = filtered_df[filtered_df['Maaş'].isin(selected_salaries)]
    if selected_emp_types:
        filtered_df = filtered_df[filtered_df['Məşğulluq növü'].isin(selected_emp_types)]
    if selected_genders:
        filtered_df = filtered_df[filtered_df['Cins'].isin(selected_genders)]

    return create_visualizations(df)
