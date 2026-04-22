# modules/predictor.py

import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk


from modules.feature_builder import build_features
from modules.aqi_utils import get_cpcb_aqi
import modules.ui_components as ui

# VERDICT FUNCTIONS
def get_cpcb_verdict_emoji(aqi):
    if aqi <= 50:
        return "🟢 Good"
    elif aqi <= 100:
        return "🟡 Satisfactory"
    elif aqi <= 200:
        return "🟠 Moderate"
    elif aqi <= 300:
        return "🔴 Poor"
    elif aqi <= 400:
        return "🟣 Very Poor"
    else:
        return "⚫ Severe"

season_matrix = pd.DataFrame(
    {
        "Jan": ["Winter", "Winter", "Winter", "Winter", "Winter", "Winter", "Winter"],
        "Feb": ["Winter", "Winter", "Winter", "Winter", "Winter", "Winter", "Winter"],
        "Mar": ["Summer", "Pre-Monsoon", "Summer", "Summer", "Summer", "Summer", "Summer"],
        "Apr": ["Summer", "Pre-Monsoon", "Summer", "Summer", "Summer", "Summer", "Summer"],
        "May": ["Summer", "Extended Monsoon", "Summer", "Summer", "Summer", "Summer", "Summer"],
        "Jun": ["SW Monsoon", "Extended Monsoon", "Summer", "Summer", "Summer", "Summer", "Summer"],
        "Jul": ["SW Monsoon", "Extended Monsoon", "Summer", "Summer", "Monsoon", "Monsoon", "Summer"],
        "Aug": ["SW Monsoon", "Extended Monsoon", "Monsoon", "Monsoon", "Monsoon", "Monsoon", "Monsoon"],
        "Sep": ["SW Monsoon", "Extended Monsoon", "Monsoon", "Monsoon", "Monsoon", "Monsoon", "Monsoon"],
        "Oct": ["Retreating Monsoon", "Extended Monsoon", "Post-Monsoon", "Post-Monsoon", "Post-Monsoon", "Post-Monsoon", "Post-Monsoon"],
        "Nov": ["Retreating Monsoon", "Post-Monsoon", "Post-Monsoon", "Post-Monsoon", "Post-Monsoon", "Post-Monsoon", "Post-Monsoon"],
        "Dec": ["Retreating Monsoon", "Winter", "Winter", "Winter", "Winter", "Winter", "Winter"],
    },
    index=["South", "Northeast", "North", "Central", "East", "West", "NCR"],
)

df = season_matrix.copy()

# Color mapping
def color_map(val):
    colors = {
        "Winter": "rgba(79, 195, 247, 0.15)",
        "Summer": "rgba(255, 112, 67, 0.15)",
        "Monsoon": "rgba(38, 166, 154, 0.15)",
        "SW Monsoon": "rgba(38, 166, 154, 0.15)",
        "Extended Monsoon": "rgba(38, 166, 154, 0.15)",
        "Pre-Monsoon": "rgba(149, 117, 205, 0.15)",
        "Post-Monsoon": "rgba(255, 202, 40, 0.15)",
        "Retreating Monsoon": "rgba(240, 98, 146, 0.15)",
    }

    borders = {
        "Winter": "#4FC3F7",
        "Summer": "#FF7043",
        "Monsoon": "#26A69A",
        "SW Monsoon": "#26A69A",
        "Extended Monsoon": "#26A69A",
        "Pre-Monsoon": "#9575CD",
        "Post-Monsoon": "#FFCA28",
        "Retreating Monsoon": "#F06292",
    }

    return f"""
        background-color: {colors.get(val, "rgba(255,255,255,0.05)")};
        color: #EAEAEA;
        border: 1px solid {borders.get(val, "#444")};
        border-radius: 10px;
        text-align: center;
        padding: 6px;
        font-size: 12px;
    """

# MAIN FUNCTION
def run():
    resources = st.session_state.resources

    model_pm25 = resources["pm25_model"]
    model_pm10 = resources["pm10_model"]
    cols25 = resources["pm25_cols"]
    cols10 = resources["pm10_cols"]
    metrics25 = resources["pm25_metrics"]
    metrics10 = resources["pm10_metrics"]


    st.header("AQI Predictor (Weather Based)")
    st.caption("Predict air quality based on environmental conditions")
    st.divider()

    # CENTERED LAYOUT
    left, icenter, right = st.columns([2, 6, 2])

    with icenter:
        city = st.selectbox("📍 Select City", [
            'Agartala','Aizawl','Amaravati','Bengaluru','Bhopal','Bhubaneswar',
            'Chandigarh','Chennai','Dehradun','Delhi','Dispur','Faridabad',
            'Gandhinagar','Gangtok','Gurugram','Hyderabad','Imphal','Itanagar',
            'Jaipur','Kohima','Kolkata','Lucknow','Mumbai','Noida','Panaji',
            'Patna','Raipur','Ranchi','Shillong','Shimla','Thiruvananthapuram']
            ,accept_new_options=False)
        
        with st.container(border=True):
            st.markdown('<div id="weather-marker"></div>', unsafe_allow_html=True)
            ui.style_container("weather-marker")
            st.markdown('<div style="border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 0.5rem; margin-bottom: 1.5rem;"><span class="card-label" style="font-size: 1.1rem;">Weather & Wind Parameters</span></div>', unsafe_allow_html=True)
            ileft,iright = st.columns(2)

            with ileft:    
                with st.expander("View Weather Verdict Guide"):
                    st.image("images/weather_verdict.png", width=400)
                
                with st.container():
                    temp = st.slider("Temperature (°C)", 0, 50, 25)
                    humidity = st.slider("Humidity (%)", 0, 100, 60)
                    precip = st.slider("Precipitation (mm)", 0, 10, 0)
                    pressure = st.slider("Pressure (hPa)", 980, 1050, 1010)
            
            with iright:
                with st.expander("View Wind Direction guide"):
                    st.caption("Degree to Direction")
                    colA, colB, colC = st.columns([1, 2, 1])
                    with colB:
                        st.image("images/compass.png", width=200)
                    st.caption("Ex- 350° means Wind is coming from 350° and going towards opposite to that.")
                
                with st.container():
                    wind_dir = st.slider("Wind Direction (°)", 0, 360, 90)
                    wind = st.slider("Wind Speed (km/h)", 0, 20, 6)

        with st.container(border=True):
            st.markdown('<div id="date-marker"></div>', unsafe_allow_html=True)
            ui.style_container("date-marker")
            st.markdown('<div style="border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 0.5rem; margin-bottom: 1.5rem;"><span class="card-label" style="font-size: 1.1rem;">Date Parameters</span></div>', unsafe_allow_html=True)
            with st.expander("View Detailed Seasonal Patterns by Region"):
                styled_df = df.style.map(color_map)
                st.dataframe(styled_df, use_container_width=True, height=280)
                st.caption("Note: This matrix helps align predictions with India's specific meteorological cycles.")

            col3, col4, col5 = st.columns(3)
            with col3:
                month = st.slider("Month", 1, 12, 5)
            with col4:
                day = st.slider("Day", 1, 30, 15)
            with col5:
                dow = st.slider("Day (0=Mon)", 0, 6, 2)

        st.divider()

        # PREDICTION BUTTON
        if st.button("Predict AQI", use_container_width=True):

            input_data = {
                "city": city,
                'temperature_2m': temp,
                'relative_humidity_2m': humidity,
                'wind_speed_10m': wind,
                'precipitation': precip,
                'surface_pressure': pressure,
                'month': month,
                'day': day,
                'day_of_week': dow,
                'wind_direction_10m': wind_dir
            }

            df25, df10 = build_features(input_data, cols25, cols10)

            pm25 = model_pm25.predict(df25)[0]
            ratio = model_pm10.predict(df10)[0]
            pm10 = pm25 * ratio

            cpcb = get_cpcb_aqi(pm25, pm10)
            who25  = round(pm25/15,2)
            who10  = round(pm10/45,2)



            # RESULTS
            st.subheader("Air Quality Prediction Summary")

            r1, r2 = st.columns(2)

            with r1:
                ci_margin = 1.96 * metrics25["RMSE"]
                lower25 = pm25 - ci_margin
                if lower25 <0: lower25 =0
                upper25 = pm25 + ci_margin
                
                status_class = "status-safe" if who25 < 1 else "status-danger"
                status_text = f"Below limit by {who25}x" if who25 < 1 else f"Limit Exceeded By {who25}x"
                
                st.markdown(f"""
                <div class="custom-card">
                    <span class="card-label">Predicted PM2.5 (µg/m³)</span>
                    <span class="card-value">{pm25:.2f}</span>
                    <span class="card-subtext">95% CI: {lower25:.2f} – {upper25:.2f}</span>
                    <span class="status-badge {status_class}">WHO: {status_text}</span>
                </div>
                """, unsafe_allow_html=True)

            with r2:
                ci_margin = 1.96 * metrics10["RMSE"]
                lower10 = ratio - ci_margin
                if lower10 <0: lower10=0
                upper10 = ratio + ci_margin
                lower10 = pm25*lower10
                upper10 = pm25*upper10
                
                status_class10 = "status-safe" if who10 < 1 else "status-warn"
                status_text10 = f"Below limit by {who10}x" if who10 < 1 else f"Limit Exceeded By {who10}x"
                
                st.markdown(f"""
                <div class="custom-card">
                    <span class="card-label">Predicted PM10 (µg/m³)</span>
                    <span class="card-value">{pm10:.2f}</span>
                    <span class="card-subtext">95% CI: {lower10:.2f} – {upper10:.2f}</span>
                    <span class="status-badge {status_class10}">WHO: {status_text10}</span>
                </div>
                """, unsafe_allow_html=True)
                
            aqi_lower = get_cpcb_aqi(lower25, lower10)
            aqi_upper = get_cpcb_aqi(upper25, upper10)
            verdict = get_cpcb_verdict_emoji(cpcb)
            
            st.markdown(f"""
            <div class="custom-card" style="text-align: center; background: rgba(56, 189, 248, 0.05); border-color: rgba(56, 189, 248, 0.2);">
                <span class="card-label">Estimated CPCB AQI</span>
                <span class="card-value" style="font-size: 4rem; background: -webkit-linear-gradient(45deg, #38bdf8, #e879f9); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{cpcb:.0f}</span>
                <span style="font-size: 1.5rem; font-weight: 700; margin-top: 10px;">{verdict}</span>
                <span class="card-subtext" style="margin-top: 10px;">Expected AQI range (95% CI): {aqi_lower:.0f} – {aqi_upper:.0f}</span>
            </div>
            """, unsafe_allow_html=True)


            
    with left:
        city_coords = {
    "Amaravati": {"lat": 16.5412, "lon": 80.5154},
    "Itanagar": {"lat": 27.1004, "lon": 93.6166},
    "Dispur": {"lat": 26.1445, "lon": 91.7362},
    "Patna": {"lat": 25.5941, "lon": 85.1376},
    "Raipur": {"lat": 21.2444, "lon": 81.6306},
    "Panaji": {"lat": 15.4909, "lon": 73.8278},
    "Gandhinagar": {"lat": 23.2156, "lon": 72.6369},
    "Chandigarh": {"lat": 30.7333, "lon": 76.7794},
    "Shimla": {"lat": 31.1048, "lon": 77.1734},
    "Ranchi": {"lat": 23.3600, "lon": 85.3300},
    "Bengaluru": {"lat": 12.9716, "lon": 77.5946},
    "Thiruvananthapuram": {"lat": 8.5241, "lon": 76.9366},
    "Bhopal": {"lat": 23.2599, "lon": 77.4126},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Imphal": {"lat": 24.8170, "lon": 93.9368},
    "Shillong": {"lat": 25.5788, "lon": 91.8933},
    "Aizawl": {"lat": 23.7271, "lon": 92.7176},
    "Kohima": {"lat": 25.6701, "lon": 94.1077},
    "Bhubaneswar": {"lat": 20.2961, "lon": 85.8245},
    "Jaipur": {"lat": 26.9124, "lon": 75.7873},
    "Gangtok": {"lat": 27.3389, "lon": 88.6065},
    "Chennai": {"lat": 13.0827, "lon": 80.2707},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867},
    "Agartala": {"lat": 23.8315, "lon": 91.2868},
    "Lucknow": {"lat": 26.8467, "lon": 80.9462},
    "Dehradun": {"lat": 30.3165, "lon": 78.0322},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639},
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
    "Gurugram": {"lat": 28.4595, "lon": 77.0266},
    "Noida": {"lat": 28.5355, "lon": 77.3910},
    "Faridabad": {"lat": 28.4089, "lon": 77.3178},
    "Ghaziabad": {"lat": 28.6692, "lon": 77.4538}
}
        lat=city_coords[city]["lat"]
        lon=city_coords[city]["lon"]
        map_df = pd.DataFrame({
        "lat": [lat],
        "lon": [lon]
    })



        st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=22.5,      # India center
        longitude=78.9,
        zoom=3.2
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=[{"lat": lat, "lon": lon}],
            get_position='[lon, lat]',
            get_radius=40000,
            get_fill_color=[255, 0, 0],
        )
    ]
    ))
