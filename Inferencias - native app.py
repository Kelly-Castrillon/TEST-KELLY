import os
from PIL import Image
from landingai.predict import SnowflakeNativeAppPredictor
import time  # Import the time module

def process_images(folder_path, predictor):
    # Iterate through all files in the specified folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Check if the file is an image based on its extension
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')):
                image_path = os.path.join(root, file)
                try:
                    # Load the image
                    image = Image.open(image_path)
                    # Measure the start time
                    start_time = time.time()
                    # Run the prediction
                    predictions = predictor.predict(image)
                    # Measure the end time
                    end_time = time.time()
                    # Calculate the time taken for the request
                    time_taken = end_time - start_time
                    # Print the predictions
                    print(f"Predictions for {file}: {predictions}")
                    print(f"Time taken for {file}: {time_taken:.2f} seconds")
                except Exception as e:
                    print(f"Error processing {file}: {e}")

# Define the necessary parameters
endpoint_id = "a04f3c45-e9da-45df-b176-5cf4b945a0b5"
url = "https://mk6qoakr-rpwerko-staging-acc-native-app.snowflakecomputing.app/sso"
snowflake_account = "CWB73596"
snowflake_user = "KellyCastrillon"
snowflake_password = "QATeam123*-SF"
folder_path = r"/Users/kellycastrillon/DATASETS/Tests-do_not_delete/DATASET CON PASCAL-SEG/Butterflies-167665624291/Butterflies-167665624291/NoSplit/Images"
predictor = SnowflakeNativeAppPredictor(
    endpoint_id=endpoint_id, 
    native_app_url=url,
    snowflake_account=snowflake_account, 
    snowflake_user=snowflake_user, 
    snowflake_password=snowflake_password, 
)

# Process all images in the specified folder
process_images(folder_path, predictor)