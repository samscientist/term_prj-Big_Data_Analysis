import api_request
import pandas as pd
import plotly.express as px
import asyncio
from constant_data import congest_lvl_mapping, area_polygons

# Convert API response to geojson formmat for plotting
def create_geojson(area_polygons):
    features = []
    for area_name, coordinates in area_polygons.items():
        polygon = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [coordinates]
            },
            "properties": {
                "name": area_name
            }
        }
        features.append(polygon)
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    return geojson


def filter_data(data):
    if 'CITYDATA' in data and 'LIVE_PPLTN_STTS' in data['CITYDATA']:
        return data['CITYDATA']['LIVE_PPLTN_STTS']
    return []


def map_congestion_to_intensity(congestion_level):
    return congest_lvl_mapping.get(congestion_level, 0)


def prepare_data_for_choropleth(data, area_name):
    processed_data = []
    for item in data:
        if 'AREA_CONGEST_LVL' in item:
            intensity = map_congestion_to_intensity(item['AREA_CONGEST_LVL'])
            processed_data.append({
                'area_name': area_name,
                'intensity': intensity
            })
        else:
            print(f"'{area_name}'의 '장소 혼잡도 지표' 정보가 없습니다.")
    return pd.DataFrame(processed_data)


def plot_choropleth(df, geojson):
    if df.empty:
        print("비어있는 데이터프레임. 시각화 불가.")
        return None

    fig = px.choropleth_mapbox(
        df,
        geojson=geojson,
        locations='area_name',
        featureidkey="properties.name",
        color='intensity',
        color_continuous_scale="Viridis",
        range_color=(0, 4),
        mapbox_style="open-street-map",
        center={"lat": 37.5665, "lon": 126.9780},
        zoom=10,
        opacity=0.6,
    )
    
    return fig


async def update_plot():
    combined_df = pd.DataFrame()
    
    for location_name, coordinates in area_polygons.items():
        data = await api_request.fetch_data(location_name)
        if data:
            filtered_data = filter_data(data)
            df = prepare_data_for_choropleth(filtered_data, location_name)
            combined_df = pd.concat([combined_df, df])
    
    print("시각화 위한 통합 데이터프레임 출력:\n", combined_df)  # Debug print to inspect combined DataFrame content
    if not combined_df.empty:
        geojson = create_geojson(area_polygons)
        fig = plot_choropleth(combined_df, geojson)
        if fig:
            fig.show()


# Looping for every 5 minutes
async def main_loop():
    while True:
        await update_plot()
        await asyncio.sleep(300)


# Run the main loop
asyncio.run(main_loop())
