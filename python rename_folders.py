import os

# Mapeo de los animales en italiano a inglés
animal_mapping = {
    "cane": "dog",
    "cavallo": "horse",
    "elefante": "elephant",
    "farfalla": "butterfly",
    "gallina": "hen",
    "gatto": "cat",
    "mucca": "cow",
    "pecora": "sheep",
    "ragno": "spider",
    "scoiattolo": "squirrel"  # Corregido el nombre aquí
}

# Función para renombrar las carpetas
def rename_folders(base_path):
    # Recorre las carpetas dentro del directorio base
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        
        # Verifica si es una carpeta
        if os.path.isdir(folder_path):
            # Convierte el nombre de la carpeta a minúsculas
            folder_name_lower = folder_name.lower()
            
            # Busca si el nombre de la carpeta coincide con algún animal
            for italian, english in animal_mapping.items():
                if italian in folder_name_lower:
                    new_folder_name = folder_name.replace(italian, english)
                    new_folder_path = os.path.join(base_path, new_folder_name)
                    
                    # Renombra la carpeta
                    os.rename(folder_path, new_folder_path)
                    print(f'Renamed "{folder_name}" to "{new_folder_name}"')
                    break  # Sale del bucle una vez que encuentra un reemplazo

# Rutas de las carpetas
folders = [
    '/Users/kellycastrillon/DATASETS/Tests-do_not_delete/Large dataset-animals/Animal Classification.v1i.folder/test',
    '/Users/kellycastrillon/DATASETS/Tests-do_not_delete/Large dataset-animals/Animal Classification.v1i.folder/train',
    '/Users/kellycastrillon/DATASETS/Tests-do_not_delete/Large dataset-animals/Animal Classification.v1i.folder/valid'
]

# Renombra las carpetas en cada ruta
for folder_path in folders:
    rename_folders(folder_path)

print("Renaming process completed!")

