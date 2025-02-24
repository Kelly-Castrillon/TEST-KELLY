import os
import time
import logging
from PIL import Image
import requests
from landingai.predict import SnowflakeNativeAppPredictor

# Configuración de logging para capturar errores
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def process_images(folder_path, predictor):
    success_count = 0  # Contador de éxitos
    failure_count = 0  # Contador de fallos

    # Verificar si la carpeta existe
    if not os.path.exists(folder_path):
        print(f"Error: La carpeta {folder_path} no existe.")
        return

    # Iterar sobre todos los archivos en la carpeta especificada
    for root, dirs, files in os.walk(folder_path):
        image_files = [file for file in files if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'))]
        
        if not image_files:
            print(f"No se encontraron imágenes válidas en {folder_path}.")
            return
        
        for file in image_files:
            image_path = os.path.join(root, file)
            try:
                # Cargar la imagen
                image = Image.open(image_path)
                # Medir el tiempo de procesamiento
                start_time = time.perf_counter()
                # Realizar la predicción
                predictions = predictor.predict(image)
                # Medir el tiempo de finalización
                end_time = time.perf_counter()
                time_taken = end_time - start_time
                
                # Mostrar las predicciones y el tiempo de procesamiento
                print(f"Predicciones para {file}: {predictions}")
                print(f"Tiempo de procesamiento para {file}: {time_taken:.2f} segundos")
                
                # Incrementar el contador de éxitos
                success_count += 1
            except IOError as e:
                print(f"Error al abrir la imagen {file}: {e}")
                logging.error(f"Error al abrir la imagen {file}: {e}")
                failure_count += 1
            except ConnectionError as e:
                print(f"Error de conexión con el predictor para {file}: {e}")
                logging.error(f"Error de conexión con el predictor para {file}: {e}")
                failure_count += 1
            except Exception as e:
                print(f"Error inesperado al procesar {file}: {e}")
                logging.error(f"Error inesperado al procesar {file}: {e}")
                failure_count += 1
    
    # Resumen del procesamiento
    print("\nResumen del procesamiento:")
    print(f"Total de imágenes procesadas exitosamente: {success_count}")
    print(f"Total de imágenes fallidas: {failure_count}")

    if failure_count > 0:
        print("Algunas imágenes no pudieron ser procesadas.")
    else:
        print("Todas las imágenes fueron procesadas exitosamente.")

# Definir los parámetros necesarios para Snowflake
endpoint_id = "322bd3c9-15f5-48ba-a974-a864e914aa16"
native_app_url = "https://adn4gc-rpwerko-azure-us-west-dev-acc-native-app.snowflakecomputing.app/"
snowflake_account = "DI56480.AZURE_WESTUS2.AZURE"
snowflake_user = "LANDING_LIBRARY_USER"

# Ruta de la carpeta que contiene las imágenes
folder_path = r"/Users/kellycastrillon/DATASETS/Tests-do_not_delete/DATASET- CON PASCAL OD/handsx-ray-170544090241/Others images"

# Inicializar el predictor
predictor = SnowflakeNativeAppPredictor(
    endpoint_id=endpoint_id,
    native_app_url=native_app_url,  # Usando 'native_app_url'
    snowflake_account=snowflake_account,
    snowflake_user=snowflake_user,
    snowflake_private_key=snowflake_private_key
)

# Procesar todas las imágenes de la carpeta especificada
process_images(folder_path, predictor)

# Realizar una solicitud de prueba para verificar la conexión
url = "https://RPWERKO.snowflakecomputing.com/session/v1/login-request"
response = requests.post(url, data={})

# Comprobar el estado de la respuesta
if response.status_code == 200:
    print("Solicitud de inicio de sesión exitosa.")
else:
    print(f"Error con la solicitud de inicio de sesión: {response.status_code}, {response.text}")
