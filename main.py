import pandas as pd
import gdown
from dash import Dash, dcc, html, Input, Output
from pathlib import Path

from helper import *
from constant import ID

file_1 = "1JmyAQI3bBnLnPe_-dIJyAmHxxc9H2K5u"

url1 = f"https://drive.google.com/uc?id={file_1}"

output = "airbnb.csv"

file = Path(output)

if not file.is_file():
    gdown.download(url1, output, quiet=False)

airbnb_df = pd.read_csv('airbnb.csv')

airbnb_df = airbnb_df[airbnb_df['country'] == 'United States']

airbnb_df = airbnb_df.rename(columns={'neighbourhood group': 'Borough'})

airbnb_df.drop(['id', 'country code', 'license'], inplace=True, axis=1)

airbnb_df["Borough"].value_counts()

airbnb_df['Borough'] = airbnb_df['Borough'].replace(['brookln'], 'Brooklyn')
airbnb_df['Borough'] = airbnb_df['Borough'].replace(['manhatan'], 'Manhattan')

airbnb_df.columns = airbnb_df.columns.str.replace(' ', '_', regex=False).str.lower()

airbnb_df.dropna(subset=["borough", "price"], inplace=True)
airbnb_df['price'] = airbnb_df['price'].str.replace(r'[$,\s]', '', regex=True).astype(float).round(2)
airbnb_df['service_fee'] = airbnb_df['service_fee'].str.replace(r'[$,\s]', '', regex=True).astype(float).round(2)

airbnb_df.dropna(subset=["borough", 'price'], inplace=True)

unique_boroughs = airbnb_df['borough'].unique()

filter_borough = {}
colors = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00']
colors_borough = {}
for borough in unique_boroughs:
    filter_borough[borough] = airbnb_df[airbnb_df['borough'] == borough]
    colors_borough[borough] = colors.pop()

price = sorted(airbnb_df['price'])
room_type = airbnb_df['room_type'].unique()

app = Dash(__name__)


@app.callback(
    [Output(ID.MAP.value, 'figure'),
     Output(ID.PRICE_RANGE_NAME.value, 'children'),
     Output(ID.BELL.value, 'figure'),
     Output(ID.TABLE.value, 'children')],
    [Input('borough-dropdown', 'value'),
     Input(ID.SLIDER.value, 'value'),
     Input('room-type-dropdown', 'value')]
)
def update_map(selected_borough, price_range, selected_room_type):
    if selected_borough == 'All':
        filtered_df = airbnb_df
    else:
        filtered_df = filter_borough[selected_borough]

    filtered_df = filter_by_range(filtered_df, price_range)

    if selected_room_type != 'All':
        filtered_df = filtered_df[(filtered_df['room_type'] == selected_room_type)]

    fig = get_map(filtered_df, colors_borough)
    price_text = "Min: {} Max: {}".format(price_range[0], price_range[1])
    return fig, price_text, get_bar_graph(filtered_df, unique_boroughs, colors_borough, price_range), get_filtered_table_df(
        filtered_df)


app.layout = html.Div([
    # Main Title
    html.H1(
        "Airbnb in New York City: Insights by Neighborhood",
        className="title",
        style={
            'fontSize': '36px',
            'textAlign': 'center',
            'color': '#1f3c88',
            'marginBottom': '20px',
            'fontFamily': 'Arial, sans-serif'
        }
    ),

    # Main container with background color and rounded corners
    html.Div(style={
        'display': 'flex',
        'gap': '15px',
        'padding': '20px',
        'height': 'calc(100vh - 110px)',  # Adjust height for layout
        'marginBottom': '30px',  # Bottom margin for spacing
        'backgroundColor': '#f3f6fb',  # Light background color for contrast
        'borderRadius': '15px',  # Rounded corners for modern look
        'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.1)'  # Subtle shadow for depth
    }, children=[

        # Left column with map and filtering options
        html.Div(id='left-column', style={
            'flex': '1',
            'display': 'flex',
            'flexDirection': 'column',
            'gap': '15px',
            'padding': '10px',
            'backgroundColor': '#ffffff',  # White for contrast
            'borderRadius': '10px',
            'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.08)',
            'overflowY': 'auto'
        }, children=[
            html.H3(
                "Airbnb Listings Distribution Across New York City",
                style={
                    'fontSize': '24px',
                    'color': '#1f3c88',
                    'textAlign': 'center',
                    'fontFamily': 'Arial, sans-serif'
                }
            ),
            dcc.Graph(id=ID.MAP.value, figure={}, style={'height': '100vh', 'flex': '1', 'margin': '-40px'}),

            # Filter Options
            html.Div(children=[
                html.Label("Filter by Borough", style={'fontSize': '16px', 'color': '#4a4a4a'}),
                dcc.Dropdown(
                    id='borough-dropdown',
                    options=[{'label': 'All', 'value': 'All'}] + [{'label': borough, 'value': borough} for borough in
                                                                  unique_boroughs],
                    value='All',
                    clearable=False,
                    style={'fontSize': '14px', 'marginBottom': '15px'}
                ),

                html.Label([], id=ID.PRICE_RANGE_NAME.value, style={'fontSize': '16px', 'color': '#4a4a4a'}),
                dcc.RangeSlider(
                    price[0], price[-1],
                    value=[price[0], price[-1]],
                    id=ID.SLIDER.value,
                    tooltip={'always_visible': False},
                    marks={int(price[0]): f'${int(price[0])}', int(price[-1]): f'${int(price[-1])}'},
                    className="range-slider"
                ),

                html.Label("Filter by Room Type", style={'fontSize': '16px', 'color': '#4a4a4a'}),
                dcc.Dropdown(
                    id='room-type-dropdown',
                    options=[{'label': 'All', 'value': 'All'}] + [{'label': room, 'value': room} for room in room_type],
                    value='All',
                    clearable=False,
                    style={'fontSize': '14px'}
                )
            ])
        ]),

        # Right column with histogram and table
        html.Div(id='right-column', style={
            'flex': '1',
            'display': 'flex',
            'flexDirection': 'column',
            'gap': '15px',
            'padding': '10px',
            'backgroundColor': '#ffffff',
            'borderRadius': '10px',
            'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.08)',
            'overflowY': 'auto'
        }, children=[

            # Histogram Section with Title
            html.H3(
                "Airbnb Listings by Price Range and Borough",
                style={
                    'fontSize': '24px',
                    'color': '#1f3c88',
                    'textAlign': 'center',
                    'fontFamily': 'Arial, sans-serif'
                }
            ),
            html.P(
                "Error bars represent standard error",
                style={
                    'fontSize': '18px',
                    'color': '#1f3c88',
                    'textAlign': 'center',
                    'fontFamily': 'Arial, sans-serif',
                    'marginTop': '-40px'
                }
            ),
            html.Div(style={'flex': '1 1 auto', 'height': '30vh'}, children=[
                dcc.Graph(id=ID.BELL.value, figure={}, style={'height': '100%'})
            ]),

            # Table Section with Title
            html.H3("Available Listings", style={
                'fontSize': '20px',
                'color': '#1f3c88',
                'marginBottom': '10px',
                'fontFamily': 'Arial, sans-serif'
            }),
            html.Div(id=ID.TABLE.value, style={
                'flex': '1 1 auto',
                'height': '30vh',
                'overflowY': 'auto',
                'padding': '10px',
                'border': '1px solid #ddd',  # Light border for separation
                'borderRadius': '8px'
            }, children=[
                # Add your table component here, e.g., dash_table.DataTable
            ])
        ])
    ])
], style={'height': '100vh', 'overflow': 'hidden', 'marginBottom': '20px',
          'backgroundColor': '#eaeef3'})  # Apply a light background color for overall contrast

if __name__ == '__main__':
    app.run_server(debug=True)
