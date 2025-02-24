import os
import time
import logging
import imghdr
import requests
from PIL import Image
from landingai.predict import Predictor

# Configurar el registro de errores
logging.basicConfig(filename="image_processing_errors.log", level=logging.ERROR)

# Validación de red
def check_network_connection(url):
    try:
        response = requests.get(url, timeout=5)  # Timeout de 5 segundos
        if response.status_code == 200:
            print("Network connection is good.")
            return True
        else:
            print(f"Error: Failed to connect to the prediction service. Status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"Error: Unable to connect to the prediction service. Details: {e}")
        return False

# Validar que la carpeta existe
def validate_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return False
    if not os.access(folder_path, os.R_OK):
        print(f"Error: No read permission for the folder '{folder_path}'.")
        return False
    return True

# Validar tamaño de la imagen
def validate_image_size(image_path):
    MAX_SIZE_MB = 5  # Limitar el tamaño máximo de las imágenes a 5MB
    MIN_SIZE_MB = 0.1  # Tamaño mínimo de 0.1MB
    file_size = os.path.getsize(image_path) / (1024 * 1024)  # en MB
    if file_size > MAX_SIZE_MB:
        print(f"Warning: The image {image_path} is too large ({file_size:.2f} MB).")
        return False
    if file_size < MIN_SIZE_MB:
        print(f"Warning: The image {image_path} is too small ({file_size:.2f} MB).")
        return False
    return True

# Verificar si la imagen es válida
def is_valid_image(image_path):
    try:
        with Image.open(image_path) as img:
            img.verify()  # Verifica que la imagen no esté dañada
        return True
    except (IOError, SyntaxError):
        print(f"Error: The image '{image_path}' is corrupted or not a valid image.")
        return False

# Validar el tipo de archivo
def validate_image_file(image_path):
    file_type = imghdr.what(image_path)
    if file_type not in ['jpeg', 'png', 'gif', 'bmp', 'tiff']:
        print(f"Error: The file '{image_path}' is not a valid image type.")
        return False
    return True

# Función principal para procesar imágenes
def process_images(folder_path, predictor):
    # Contadores de imágenes procesadas correctamente y fallidas
    success_count = 0
    failure_count = 0

    # Verificar la carpeta
    if not validate_folder(folder_path):
        return

    # Verificar la conexión de red
    if not check_network_connection(predictor._url):
        return

    # Iterar a través de todos los archivos en la carpeta
    for root, dirs, files in os.walk(folder_path):
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'))]
        if not image_files:
            print(f"Warning: No valid image files found in the folder '{folder_path}'.")
            return

        for file in image_files:
            image_path = os.path.join(root, file)

            # Validar archivo de imagen
            if not validate_image_file(image_path) or not is_valid_image(image_path) or not validate_image_size(image_path):
                failure_count += 1
                continue

            try:
                # Cargar la imagen
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
                logging.error(f"Error processing {file}: {e}")
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

# Configuración del API
Predictor._url = "https://predict.app.staging.landing.ai/inference/v1/predict"
endpoint_id = "3f86f733-61ed-4508-81c3-598a7e8a2cd5"
api_key = "land_sk_QVAdd3LfTpUcqNPBIkS3a8eLSVEV9561v64et3uK3M8MdHffdW"
folder_path = r"/Users/kellycastrillon/DATASETS/Cloudinference- avi-common/OD project/train/Images"

# Crear el objeto predictor
predictor = Predictor(endpoint_id, api_key=api_key)

# Procesar las imágenes
process_images(folder_path, predictor)
