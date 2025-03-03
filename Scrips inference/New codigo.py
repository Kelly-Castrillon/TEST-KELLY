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