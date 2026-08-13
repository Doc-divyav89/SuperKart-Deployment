import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BASE_URL = "http://localhost:7860"

# Set the title of the Streamlit app
st.title("Suoer Kart Predictor")

# Section for online prediction
st.header("Online Prediction")

# Collective Input
col1, col2, col3 = st.columns(3)

with col1:
    product_weight = st.number_input("Product Weight", min_value=0.0, step=0.01)
    product_sugar_content = st.selectbox("Product Sugar Content", ["Low Sugar", "Medium Sugar", "High Sugar"])
    product_allocated_area = st.number_input("Product Allocated Area", min_value=0.0, step=0.001
                                             
# Convert User input
  input_data = pd.DataFrame({
    "Product_Weight": [product_weight],
    "Product_Sugar_Content": [product_sugar_content],
    "Product_Allocated_Area": [product_allocated_area]})
  
# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/rental", json=input_data.to_dict(orient='records')[0])  # Send data to Flask API
    if response.status_code == 200: 
       prediction = response.jason()
       st.success("Batch predictions completed!")
       st.write(predictions)  # Display the predictions
      else
          st.error("Unable to connect to the prediction API.")                                                                               

                  
