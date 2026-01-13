import os
import shutil

# Liste des dossiers à vider
folders = ["images", "tri_blanc", "tri_noir"]

for folder in folders:
    if os.path.exists(folder) and os.path.isdir(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # supprime fichier ou lien
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # supprime dossier
            except Exception as e:
                print(f"Erreur lors de la suppression de {file_path} : {e}")
        print(f"Dossier '{folder}' vidé.")
    else:
        print(f"Dossier '{folder}' introuvable.")

print("Nettoyage terminé.")