
Import necessary libraries
import numpy as np import joblib # For loading the serialized model import pandas as pd # For data manipulation from flask import Flask, request, jsonify # For creating the Flask API

Initialize the Flask application
super_kart_api = Flask("Super Kart")

Load the trained machine learning model
model = joblib.load('superkart_model.joblib')

Define a route from the home page(GET Request)
@super_kart_api.route('/') def home(): return "Happy Shopping with Super Kart"

Define an endpoint for single prediction (POST Request)
@super_kart_api.post('/v1/predict') def predict(): # Get the input data from the request input_data = request.get_json()

#Extract revelent feture in JSON 

sample_input = pd.DataFrame([input_data])

# Convert the input data to a DataFrame
input_df = pd.DataFrame([input_data])

# Make a prediction using the loaded model
prediction = model.predict(input_df)

# Return Value post prediction
return jsonify({'prediction': prediction.tolist()})
Define an endpoint for batch prdiction (POST Request)
@super_kart_api.post('/v1/predictbatch') def predictbatch(): # Get the input data from the request input_data = request.files['file']

# Read the CSV file into a Pandas DataFrame
input_data = pd.read_csv(file)

# Make predictions for all properties in the DataFrame (get log_prices)
predicted_log_prices = model.predict(input_data).tolist()
Return the predictions dictionary as a JSON response
return output_dict
Run the Flask application in debug mode if this script is executed directly
if name == 'main': rental_price_predictor_api.run(debug=True)
