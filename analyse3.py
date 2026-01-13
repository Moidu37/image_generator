import cv2
import os
from skimage.metrics import structural_similarity as ssim

IMAGE_REFERENCE = "image_ref.png"
DOSSIER_IMAGES = "images"
FICHIER_RAPPORT = "rapport_similarite.txt"
MAX_IMAGES = 100  # 🔹 nombre max d’images à analyser

# Charger l'image de référence (PNG)
ref = cv2.imread(IMAGE_REFERENCE, cv2.IMREAD_GRAYSCALE)
if ref is None:
    raise ValueError("Image de référence introuvable")

resultats = []

# Récupérer uniquement les PNG
fichiers_png = [
    f for f in os.listdir(DOSSIER_IMAGES)
    if f.lower().endswith(".png")
]

# Limite à 100 images
fichiers_png = fichiers_png[:MAX_IMAGES]

total = len(fichiers_png)
print(f"📸 {total} images à analyser\n")

# Parcours des images
for i, nom_fichier in enumerate(fichiers_png, start=1):
    print(f"Analyse {i}/{total} : {nom_fichier}")

    chemin = os.path.join(DOSSIER_IMAGES, nom_fichier)
    img = cv2.imread(chemin, cv2.IMREAD_GRAYSCALE)

    if img is None:
        continue

    # Redimensionnement
    img = cv2.resize(img, (ref.shape[1], ref.shape[0]))

    score, _ = ssim(ref, img, full=True)
    note = score * 10  # note de 0 à 10

    resultats.append((nom_fichier, note))

# Tri du + ressemblant au - ressemblant
resultats.sort(key=lambda x: x[1], reverse=True)

# Écriture du rapport TXT
with open(FICHIER_RAPPORT, "w", encoding="utf-8") as f:
    f.write("RAPPORT DE SIMILARITÉ D’IMAGES PNG\n")
    f.write("=" * 45 + "\n\n")

    f.write("TOP 10 DES IMAGES LES PLUS PROCHES\n\n")
    for i, (nom, note) in enumerate(resultats[:10], start=1):
        f.write(f"{i}. {nom} → {note:.20f}/10\n")

    f.write("\n" + "=" * 45 + "\n\n")
    f.write("CLASSEMENT COMPLET (du + ressemblant au - ressemblant)\n\n")

    for nom, note in resultats:
        f.write(f"{nom} → {note:.20f}/10\n")

print("\n✅ Rapport généré :", FICHIER_RAPPORT)