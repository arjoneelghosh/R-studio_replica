
import streamlit as st

st.title("Air Quality Index (AQI) Dashboard")
st.write("This is a simple data visualization app for AQI analysis.")

# Example input and output
city = st.text_input("Enter your city:")
if city:
    st.write(f"You entered: {city}")
