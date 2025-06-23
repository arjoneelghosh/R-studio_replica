import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta

# Title of the Streamlitstreamlit run xyz.py     app
st.title("🌍 Real-Time AQI Data with Visualizations")

# OpenWeatherMap API key
API_KEY = "51ae582e2c8e6e2c3a7703824ca9f4b4"

# Function to fetch AQI data
def fetch_aqi_data(city):
    GEO_API_URL = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    geo_response = requests.get(GEO_API_URL)

    if geo_response.status_code == 200:
        geo_data = geo_response.json()
        if geo_data:
            lat, lon = geo_data[0]['lat'], geo_data[0]['lon']
            AQI_API_URL = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
            aqi_response = requests.get(AQI_API_URL)

            if aqi_response.status_code == 200:
                return geo_data[0], aqi_response.json()
    return None, None

# Input for city name
city = st.text_input("Enter city name to check AQI:")

if city:
    st.write("Fetching AQI data...")
    location_data, aqi_data = fetch_aqi_data(city)

    if location_data and aqi_data:
        # Extract AQI and coordinates
        lat, lon = location_data['lat'], location_data['lon']
        aqi_value = aqi_data['list'][0]['main']['aqi']

        # Map AQI index to description
        aqi_description = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}

        # Display AQI information
        st.success(f"The AQI for **{city}** is **{aqi_description[aqi_value]}** (Index: {aqi_value}).")
        
        # Simulated historical data
        historical_data = [
            {"hour": i, "AQI": aqi_value + (i % 5)} for i in range(24)
        ]
        df = pd.DataFrame(historical_data)

        # Interactive Date Range Selector
        st.write("### Filter Historical AQI by Date Range")
        today = datetime.today()
        start_date = st.date_input("Start Date", today - timedelta(days=7))
        end_date = st.date_input("End Date", today)

        if start_date <= end_date:
            filtered_df = df  # Simulated data does not yet include dates
            st.write(f"Showing data from **{start_date}** to **{end_date}**")
        else:
            st.error("Error: Start Date must be before or equal to End Date.")

        # Interactive AQI Level Slider
        st.write("### Filter AQI Levels")
        aqi_min, aqi_max = st.slider("Select AQI Range", 0, 500, (0, 500))
        filtered_df = df[df["AQI"].between(aqi_min, aqi_max)]

        # Line Chart with Filtered Data
        st.write("### Hourly AQI Trends")
        line_chart = px.line(filtered_df, x="hour", y="AQI", title="Hourly AQI Levels", markers=True)
        st.plotly_chart(line_chart)

        # Compare AQI Across Cities
        st.write("### AQI Comparison Across Cities")
        available_cities = ["Kolkata", "Delhi", "Mumbai", "Chennai", "Bangalore"]
        selected_cities = st.multiselect("Select cities to compare", available_cities, default=available_cities)
        
        city_comparison = pd.DataFrame({
            "City": available_cities,
            "AQI": [aqi_value, aqi_value + 10, aqi_value - 5, aqi_value + 2, aqi_value + 8]
        })
        filtered_city_comparison = city_comparison[city_comparison["City"].isin(selected_cities)]
        
        bar_chart = px.bar(filtered_city_comparison, x="City", y="AQI", color="AQI", title="AQI Comparison")
        st.plotly_chart(bar_chart)

        # Heatmap: Geographical Representation
        st.write("### AQI Heatmap")
        m = folium.Map(location=[lat, lon], zoom_start=10)
        folium.CircleMarker(
            location=[lat, lon],
            radius=10,
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.7,
            tooltip=f"{city}: {aqi_description[aqi_value]} (AQI {aqi_value})"
        ).add_to(m)
        st_folium(m, width=700, height=500)

    else:
        st.error("Could not fetch AQI data. Please check the city name or API key.")

# Footer
st.write("---")
st.write("Powered by OpenWeatherMap API | Visualizations by Plotly and Folium")
