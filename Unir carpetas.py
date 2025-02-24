import os
import hashlib
from collections import defaultdict

def calculate_md5(file_path):
    """Calcula el hash MD5 de una imagen."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def find_and_remove_duplicates(directory):
    """Busca imágenes duplicadas en las subcarpetas de un directorio y elimina algunas."""
    hashes = defaultdict(list)  # Diccionario para almacenar las imágenes por su hash
    duplicates = defaultdict(list)  # Diccionario para almacenar duplicados por subcarpeta
    total_deleted = 0  # Contador de imágenes eliminadas

    # Recorre todas las subcarpetas y archivos
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                file_path = os.path.join(root, file)
                file_hash = calculate_md5(file_path)

                # Si el hash ya existe, es un duplicado
                if file_hash in hashes:
                    # Guardamos la ruta duplicada
                    duplicates[root].append(file_path)
                else:
                    hashes[file_hash].append(file_path)

    # Eliminar imágenes duplicadas y contar
    for folder, files in duplicates.items():
        if len(files) > 1:  # Si hay más de una imagen duplicada en la subcarpeta
            # Dejamos la primera y eliminamos las siguientes
            for file_to_delete in files[1:]:
                os.remove(file_to_delete)
                total_deleted += 1
                print(f"Imagen eliminada: {file_to_delete}")

    return total_deleted, duplicates

# Ruta al directorio principal
directory = '/Users/kellycastrillon/DATASETS/Tests-do_not_delete/Large dataset-animals/Animal Classification.v1i.folder/consolidated'

total_deleted, duplicates = find_and_remove_duplicates(directory)

if total_deleted > 0:
    print(f"\nSe eliminaron {total_deleted} imágenes duplicadas.")
else:
    print("\nNo se encontraron imágenes duplicadas.")

# Reporte de duplicados por subcarpeta
print("\nResumen de duplicados por subcarpeta:")
for folder, files in duplicates.items():
    if len(files) > 1:
        print(f"\nSubcarpeta: {folder}")
        print(f"Imágenes duplicadas encontradas: {len(files)}")
        for file in files:
            print(f"- {file}")
