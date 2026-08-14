import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BASE_URL = "http://localhost:7860" # Use this for local testing within Codespaces. For external deployment, update this URL.

# Set the title of the Streamlit app
st.set_page_config(layout="wide")
st.title("Super Kart Sales Predictor")

# Section for online prediction
st.header("Online Prediction")

# Define the input fields for the model
# Categorical features with their unique values
PRODUCT_SUGAR_CONTENT_OPTIONS = ["Low Sugar", "Regular", "No Sugar", "rec"]
PRODUCT_TYPE_OPTIONS = ['Frozen Foods', 'Dairy', 'Canned', 'Baking Goods', 'Health and Hygiene',
                        'Snack Foods', 'Meat', 'Soft Drinks', 'Household', 'Fruits and Vegetables',
                        'Hard Drinks', 'Breakfast', 'Starchy Foods', 'Others', 'Seafood', 'Bread']
STORE_SIZE_OPTIONS = ["Medium", "High", "Small"]
STORE_LOCATION_CITY_TYPE_OPTIONS = ["Tier 1", "Tier 2", "Tier 3"]
STORE_TYPE_OPTIONS = ["Departmental Store", "Supermarket Type1", "Supermarket Type2", "Food Mart"]

# Create input widgets in columns for better layout
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Product Information")
    product_weight = st.number_input("Product Weight (kg)", min_value=4.0, max_value=22.0, value=12.66, step=0.01)
    product_sugar_content = st.selectbox("Product Sugar Content", PRODUCT_SUGAR_CONTENT_OPTIONS, index=PRODUCT_SUGAR_CONTENT_OPTIONS.index("Low Sugar"))
    product_allocated_area = st.number_input("Product Allocated Area", min_value=0.004, max_value=0.298, value=0.027, step=0.001)
    product_mrp = st.number_input("Product MRP", min_value=31.0, max_value=266.0, value=117.08, step=0.01)

with col2:
    st.subheader("Store Information")
    store_establishment_year = st.number_input("Store Establishment Year", min_value=1987, max_value=2009, value=2009, step=1)
    store_size = st.selectbox("Store Size", STORE_SIZE_OPTIONS, index=STORE_SIZE_OPTIONS.index("Medium"))
    store_location_city_type = st.selectbox("Store Location City Type", STORE_LOCATION_CITY_TYPE_OPTIONS, index=STORE_LOCATION_CITY_TYPE_OPTIONS.index("Tier 2"))
    store_type = st.selectbox("Store Type", STORE_TYPE_OPTIONS, index=STORE_TYPE_OPTIONS.index("Supermarket Type2"))

with col3:
    st.subheader("Additional Product Info")
    product_type = st.selectbox("Product Type", PRODUCT_TYPE_OPTIONS, index=PRODUCT_TYPE_OPTIONS.index("Frozen Foods"))

# Prepare input data for the API request
input_data = {
    "Product_Weight": product_weight,
    "Product_Sugar_Content": product_sugar_content,
    "Product_Allocated_Area": product_allocated_area,
    "Product_Type": product_type,
    "Product_MRP": product_mrp,
    "Store_Establishment_Year": store_establishment_year,
    "Store_Size": store_size,
    "Store_Location_City_Type": store_location_city_type,
    "Store_Type": store_type
}

# Make prediction when the "Predict" button is clicked
if st.button("Predict Sales", type="primary"):
    try:
        # Correct endpoint for single prediction
        response = requests.post(f"{BASE_URL}/v1/predict", json=input_data)
        if response.status_code == 200:
            prediction = response.json()
            st.success(f"Predicted Sales: ${prediction['predicted_sales']:.2f}")
        else:
            st.error(f"Error making prediction: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Connection Error: Could not connect to the backend API. Please ensure the backend is running and the BASE_URL is correct.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

st.markdown("--- ")

st.subheader("Batch Prediction (Upload CSV)")
uploaded_file = st.file_uploader("Choose a CSV file for batch prediction", type="csv")

if uploaded_file is not None:
    try:
        batch_df = pd.read_csv(uploaded_file)

        # Display a preview of the uploaded data
        st.write("Uploaded Data Preview:")
        st.dataframe(batch_df.head())

        if st.button("Run Batch Prediction"):
            # Convert DataFrame to CSV string and encode to bytes
            csv_file = batch_df.to_csv(index=False).encode('utf-8')
            files = {'file': ('batch_data.csv', csv_file, 'text/csv')}

            # Make request to batch prediction endpoint
            response = requests.post(f"{BASE_URL}/v1/predictbatch", files=files)

            if response.status_code == 200:
                predictions_json = response.json() # Corrected json() call
                predicted_df = pd.DataFrame(predictions_json)
                st.success("Batch predictions completed!")
                st.write("Predictions:")
                st.dataframe(predicted_df)
            else:
                st.error(f"Error in batch prediction: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"An error occurred during file processing or batch prediction: {e}")
