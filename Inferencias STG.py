import os
from PIL import Image
from landingai.predict import Predictor
import time  # Import time for measuring execution time

def process_images(folder_path, predictor):
    # Contadores de imágenes procesadas correctamente y fallidas
    success_count = 0
    failure_count = 0
    
    # Iterar a través de todos los archivos en la carpeta especificada
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Comprobar si el archivo es una imagen por su extensión
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')):
                image_path = os.path.join(root, file)
                try:
                    # Intentar cargar la imagen
                    image = Image.open(image_path)
                    # Medir el tiempo de inicio
                    start_time = time.time()
                    # Ejecutar la predicción
                    predictions = predictor.predict(image)
                    # Medir el tiempo de finalización
                    end_time = time.time()
                    # Calcular el tiempo de ejecución
                    time_taken = end_time - start_time
                    # Imprimir las predicciones
                    print(f"Predictions for {file}: {predictions}")
                    print(f"Time taken for {file}: {time_taken:.2f} seconds")
                    # Incrementar contador de imágenes procesadas exitosamente
                    success_count += 1
                except Exception as e:
                    print(f"Error processing {file}: {e}")
                    # Incrementar contador de imágenes fallidas
                    failure_count += 1

    # Imprimir resumen del procesamiento
    print("\nProcessing Summary:")
    print(f"Total images processed successfully: {success_count}")
    print(f"Total images failed: {failure_count}")
    
    if failure_count > 0:
        print("Some images failed to process.")
    else:
        print("All images processed successfully.")

# Enter your API Key
Predictor._url = "https://predict.app.staging.landing.ai/inference/v1/predict"
endpoint_id = "d35dc833-f7f5-4d10-bbfd-ae0141ffa273"
api_key = "land_sk_7CeQ1rFer6iUKoQLLf5ai82rRT9Oy90sqGq87s3u45zwWE6GwJ"
folder_path = r"/Users/kellycastrillon/DATASETS/Tests-do_not_delete/DATASET CON PASCAL-SEG/Butterflies-167665624291/Butterflies-167665624291/train/Images"

# Cargar la imagen y ejecutar la predicción
predictor = Predictor(endpoint_id, api_key=api_key)

# Procesar las imágenes
process_images(folder_path, predictor)

