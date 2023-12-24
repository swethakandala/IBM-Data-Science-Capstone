# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into a pandas dataframe
spacex_df = pd.read_csv("spacex_launch.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# Define custom colors
colors = {
    'background': '#F3F6FA',
    'text': '#333333',
    'plot_bg': '#FFFFFF',
    'border_color': '#DDDDDD',
    'pie_chart_colors': ['#0077B6', '#00B4D8', '#48CAE4', '#90E0EF', '#ADE8F4'],  # Custom colors for the pie chart
    'scatter_chart_colors': ['#4CAF50', '#FF5722'],  # Custom colors for the scatter chart
}

# Create an app layout
app.layout = html.Div(
    style={'backgroundColor': colors['background'], 'padding': '20px'},
    children=[
        html.H1(
            'SpaceX Launch Dashboard',
            style={'textAlign': 'center', 'color': colors['text'], 'font-size': 40},
        ),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        dcc.Dropdown(
            id='site-dropdown',
            options=[
                {'label': 'ALL SITES', 'value': 'ALL'},
                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            ],
            value='ALL',
            placeholder="Select a Launch Site here",
            searchable=True,
            style={'width': '50%'},
        ),
        html.Br(),
        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        html.Div(
            dcc.Graph(
                id='success-pie-chart',
                config={'displayModeBar': False},
                style={'border': f'2px solid {colors["border_color"]}'},
            ),
            style={'backgroundColor': colors['plot_bg']},
        ),
        html.Br(),
        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(
            id='payload-slider',
            min=0,
            max=10000,
            step=1000,
            value=[min_payload, max_payload],
            marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
        ),
        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(
            dcc.Graph(
                id='success-payload-scatter-chart',
                config={'displayModeBar': False},
                style={'border': f'2px solid {colors["border_color"]}'},
            ),
            style={'backgroundColor': colors['plot_bg']},
        ),
    ],
)

# Callback for the pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
)
def build_graph(site_dropdown):
    if site_dropdown == 'ALL':
        piechart = px.pie(data_frame=spacex_df, names='Launch Site', values='class', title='Total Launches for All Sites',
                          color_discrete_sequence=colors['pie_chart_colors'])  # Apply custom colors
        return piechart
    else:
        specific_df = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        piechart = px.pie(data_frame=specific_df, names='class', title=f'Total Launch for a Specific Site',
                          color_discrete_sequence=colors['pie_chart_colors'])  # Apply custom colors
        return piechart

# Callback for the scatter chart
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')],
)
def update_graph(site_dropdown, payload_slider):
    if site_dropdown == 'ALL':
        filtered_data = spacex_df[
            (spacex_df['Payload Mass (kg)'] >= payload_slider[0])
            & (spacex_df['Payload Mass (kg)'] <= payload_slider[1])
        ]
        scatterplot = px.scatter(
            data_frame=filtered_data,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            color_discrete_sequence=colors['scatter_chart_colors'],  # Apply custom colors
            title='Correlation between Payload and Launch Success',
        )
        return scatterplot
    else:
        specific_df = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        filtered_data = specific_df[
            (specific_df['Payload Mass (kg)'] >= payload_slider[0])
            & (specific_df['Payload Mass (kg)'] <= payload_slider[1])
        ]
        scatterplot = px.scatter(
            data_frame=filtered_data,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            color_discrete_sequence=colors['scatter_chart_colors'],  # Apply custom colors
            title=f'Correlation between Payload and Launch Success for {site_dropdown}',
        )
        return scatterplot

# Run the app
if __name__ == '__main__':
    app.run_server()
