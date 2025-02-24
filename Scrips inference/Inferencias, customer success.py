import os
from PIL import Image
from landingai.predict import SnowflakeNativeAppPredictor
import time
import logging  # Import logging to log errors

# Configure logging to log errors
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def process_images(folder_path, predictor):
    success_count = 0  # Initialize success counter
    failure_count = 0  # Initialize failure counter

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
                    # Print the predictions and processing time
                    print(f"Predictions for {file}: {predictions}")
                    print(f"Time taken for {file}: {time_taken:.2f} seconds")
                    # Increment the success counter
                    success_count += 1
                except Exception as e:
                    print(f"Error processing {file}: {e}")
                    logging.error(f"Error processing {file}: {e}")
                    # Increment the failure counter
                    failure_count += 1
    
    # Print a summary of the processing
    print("\nProcessing Summary:")
    print(f"Total images processed successfully: {success_count}")
    print(f"Total images failed: {failure_count}")

    if failure_count > 0:
        print("Some images failed to process.")
    else:
        print("All images processed successfully.")

# Define the necessary parameters
endpoint_id = "bf1a5877-17a4-4f1f-8252-7074a4d9c3a4"
url = "https://nlc4alkz-rpwerko-lai-snow-customer-success.snowflakecomputing.app/sso"
snowflake_account = "PVB66292"
snowflake_user = "csuccess_shared_account"
snowflake_password = "NativeApp5"
folder_path = r"/Users/kellycastrillon/DATASETS/Tests-do_not_delete/DATASET CON PASCAL-SEG/Butterflies-167665624291/Butterflies-167665624291/NoSplit/Images"
# Initialize the predictor
predictor = SnowflakeNativeAppPredictor(
    endpoint_id=endpoint_id,
    native_app_url=url,
    snowflake_account=snowflake_account,
    snowflake_user=snowflake_user,
    snowflake_password=snowflake_password,
)

# Process all images in the specified folder
process_images(folder_path, predictor)
