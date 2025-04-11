import os
import tensorflow as tf
import pandas as pd
import numpy as np
from tensorflow import keras
from metpy.calc import wet_bulb_temperature
from metpy.units import units


print("TensorFlow version:", tf.__version__)

# Initialize global variables
model = None
data_ref = None


def __init__() -> tuple:
    """
    Initialise the model and data reference.
    This function loads the pre-trained model and the cleaned weather data reference.
    """
    # Load the model
    model = keras.models.load_model("./data/trained_model.keras")
    print("Model loaded successfully.")
    data_ref = pd.read_csv("./data/cleaned_weather_data.csv")
    print("Data reference loaded.")
    return model, data_ref


# Initialize the model and data reference globally
model, data_ref = __init__()


def normalize_data(input_data: pd.DataFrame, data_ref: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize the input data using the same scaling logic as the training data.
    Args:
        input_data (pd.DataFrame): The input data to normalize.
        data_ref (pd.DataFrame): The reference data used for scaling.
    Returns:
        pd.DataFrame: The normalized input data.
    """
    for feature in input_data.columns:
        if feature in ["rel_hum"]:
            input_data[feature] = input_data[feature] / 100  # Scale relative humidity
        elif feature in ["wind_dir_deg"]:
            input_data[feature] = input_data[feature] / 360  # Scale wind direction
        else:
            min_val = data_ref[feature].min()
            max_val = data_ref[feature].max()
            input_data[feature] = (input_data[feature] - min_val) / (max_val - min_val)
        input_data[feature] = input_data[feature].clip(0, 1)

    # Convert input data to NumPy array with consistent dtype
    input_data = input_data.astype(np.float32)

    return input_data


def predict(json_data: dict) -> dict:
    """
    Predict the target variables using the pre-trained model and the provided features.
    Args:
        json_data (dict): A dictionary containing the input features for prediction.
    Returns:
        dict: The predicted target variables.
    """
    global model, data_ref  # Ensure global variables are used

    # Extract and validate the features from the JSON data
    try:
        air_temp = float(json_data.get("air_temp", 0) or 0)
        dewpt = float(json_data.get("dewpt", 0) or 0)
        rel_hum = float(json_data.get("rel_hum", 0) or 0)
        press = float(json_data.get("press", 0) or 0)
        apparent_t = float(json_data.get("apparent_t", 0) or 0)
    except ValueError as e:
        print(f"Invalid input data: {e}")
        return {"error": "Invalid input data"}

    # Calculate additional features
    rain_trace = 0.0
    rain_ten = 0.0
    rain_hour = 0.0
    delta_t = 3.0

    press_wet = press * units.hPa
    air_temp_wet = air_temp * units.degC
    dewpt_wet = dewpt * units.degC

    # Calculate the wet bulb temperature
    wet_bulb_temp = wet_bulb_temperature(press_wet, air_temp_wet, dewpt_wet)
    wet_bulb_temp = wet_bulb_temp.to(units.degC).magnitude  # Extract magnitude
    wet_bulb_temp = round(wet_bulb_temp, 1)

    # Create a DataFrame with all required input features
    input_data = pd.DataFrame(
        {
            "air_temp": [air_temp],
            "dewpt": [dewpt],
            "rel_hum": [rel_hum],
            "press": [press],
            "apparent_t": [apparent_t],
            "rain_trace": [rain_trace],
            "rain_ten": [rain_ten],
            "rain_hour": [rain_hour],
            "delta_t": [delta_t],
            "wet_bulb_temperature": [wet_bulb_temp],
        }
    )

    # Ensure the input data has the same columns as the model was trained on
    required_columns = [
        "air_temp",
        "dewpt",
        "rel_hum",
        "press",
        "apparent_t",
        "rain_trace",
        "rain_ten",
        "rain_hour",
        "delta_t",
        "wet_bulb_temperature",
    ]
    input_data = input_data.reindex(columns=required_columns, fill_value=0)
    print("Input data shape:", input_data.shape)
    print("Input data columns:", input_data.columns)

    # Normalize the input data
    input_data = normalize_data(input_data, data_ref)

    # Convert input data to NumPy array with consistent dtype
    input_data = input_data.astype(np.float32)

    # Make the prediction
    predictions = model.predict(input_data)
    print("Raw predictions:", predictions[0])
    # wind_dir_deg, wind_spd_kmh, gust_kmh = predictions[0]
    wind_spd_kmh, gust_kmh, wind_dir_deg = predictions[0]

    # Denormalize the predictions
    wind_dir_deg = float(wind_dir_deg * 360)  # Convert back to degrees
    wind_dir_deg = max(0, min(wind_dir_deg, 360))  # Clip to valid range

    # Use the absolute maximum and minimum values for denormalization
    wind_spd_min = data_ref["wind_spd_kmh"].min()
    gust_min = data_ref["gust_kmh"].min()
    wind_spd_max = data_ref["wind_spd_kmh"].max()
    gust_max = data_ref["gust_kmh"].max()

    wind_spd_kmh = float(wind_spd_kmh * (wind_spd_max - wind_spd_min) + wind_spd_min)
    gust_kmh = float(gust_kmh * (gust_max - gust_min) + gust_min)

    # Return the predictions as a dictionary
    return {
        "wind_spd_kmh": round(wind_spd_kmh, 1),
        "gust_kmh": round(gust_kmh, 1),
        "wind_dir_deg": round(wind_dir_deg, 1),
    }


if __name__ == "__main__":
    print("Starting prediction...")
    print("Data reference shape:", data_ref.shape)
    print("Data reference columns:", data_ref.columns)
