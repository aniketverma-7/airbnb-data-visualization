import numpy as np
import pandas as pd
import plotly.express as px
from dash import dash_table


def filter_by_range(df, price_range):
    return df[(df['price'] >= price_range[0]) & (df['price'] <= price_range[1])]


def get_map(df, colors_borough):
    fig = px.scatter_mapbox(
        df,
        lat='lat',
        lon='long',
        hover_name='name',
        hover_data={'lat': False, 'long': False, 'borough': True, 'price': True, 'room_type': True,
                    'number_of_reviews': True},
        color_discrete_map=colors_borough,
        color='borough',
        color_discrete_sequence=px.colors.qualitative.Set1,
        mapbox_style="carto-positron",
        zoom=10,
        height=800
    )

    fig.update_layout(
        showlegend=False,
        margin=dict(b=80),
    )

    fig.update_traces(
        hovertemplate="<b>%{hovertext}"
                      "<br>Price: $%{customdata[3]:.2f}"
                      "<br>Room Type: %{customdata[4]}"
                      "<br>Number of Reviews: %{customdata[5]}"

    )

    return fig


def get_bar_graph(df, unique_boroughs, color_map, price_range):
    step = (price_range[1] - price_range[0]) // 5
    price_ranges = [
        (price_range[0] + i * step + (1 if i != 0 else 0), price_range[0] + (i + 1) * step)
        for i in range(4)
    ]
    price_ranges.append(((price_range[0] + 4 * step), price_range[1]))
    price_data = []

    for borough in unique_boroughs:
        borough_df = df[df['borough'] == borough]

        for price_min, price_max in price_ranges:
            prices_in_range = borough_df[(borough_df['price'] >= price_min) &
                                         (borough_df['price'] <= price_max)]['price']

            count = len(prices_in_range)

            if count > 0:
                std_error = prices_in_range.std() / np.sqrt(count)
            else:
                std_error = 0

            if price_max == float('inf'):
                range_label = f'${price_min}+'
            else:
                range_label = f'${price_min}-${price_max}'

            price_data.append({
                'borough': borough,
                'price_range': range_label,
                'count': count,
                'error': std_error
            })

    price_counts_df = pd.DataFrame(price_data)
    fig = px.bar(price_counts_df,
                 x='price_range',
                 y='count',
                 color='borough',
                 barmode='group',
                 error_y='error',
                 labels={
                     'price_range': 'Price Range',
                     'count': 'Number of Listings',
                     'borough': 'Borough'
                 },
                 color_discrete_map=color_map,  # Custom colors
                 text='count'
                 )

    fig.update_layout(
        xaxis_title='Price Range',
        yaxis_title='Number of Listings',
        legend_title='Borough',
        xaxis={'tickangle': -45},
        margin=dict(b=80),
    )

    fig.update_traces(
        textposition='outside',
        textfont=dict(size=10),
        error_y=dict(
            thickness=1,
            width=4,
            color='#444'
        )
    )

    return fig


def get_filtered_table_df(df):
    selected_cols = ['name', 'host_identity_verified', 'host_name', 'borough',
                     'neighbourhood', 'cancellation_policy', 'room_type', 'price',
                     'service_fee', 'minimum_nights']
    df = df[selected_cols]
    df.columns = df.columns.str.replace('_', ' ').str.title()
    df.rename(columns={'Price': 'Price (in US dollar)', 'Service Fee': 'Service Fee (in US dollar)'}, inplace=True)
    return dash_table.DataTable(df.to_dict('records'),
                                [{"name": i, "id": i} for i in df.columns],
                                sort_action="native",
                                sort_mode="multi",
                                )
