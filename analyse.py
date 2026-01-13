import cv2
import os
import numpy as np

# --- Configuration ---
IMAGE_REFERENCE = "image_ref.png"
DOSSIER_IMAGES = "images"
FICHIER_RAPPORT = "rapport_similarite5x5.txt"


def preparer_image(chemin_image):
    """Charge, redimensionne en 5x5 et binarise l'image sans interface graphique."""
    img = cv2.imread(chemin_image, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None
    # Redimensionnement minimal pour l'analyse structurelle
    img_5x5 = cv2.resize(img, (5, 5))
    # Binarisation (0 ou 1)
    _, img_bw = cv2.threshold(img_5x5, 50, 1, cv2.THRESH_BINARY)
    return img_bw

def analyser():
    FICHIER_TESTES = 0
    deja_execute = False
    """Analyse les images et enregistre les résultats dans un fichier."""
    ref = preparer_image(IMAGE_REFERENCE)
    if ref is None:
        print(f"❌ Erreur : Impossible de charger la référence {IMAGE_REFERENCE}")
        return

    resultats = []

    if not os.path.exists(DOSSIER_IMAGES):
        print(f"❌ Erreur : Le dossier '{DOSSIER_IMAGES}' n'existe pas.")
        return

    print("🔍 Analyse en cours...")

    for nom_fichier in os.listdir(DOSSIER_IMAGES):
        if nom_fichier.lower().endswith((".png", ".jpg", ".jpeg")):
            # Construction du chemin correct vers l'image dans le sous-dossier
            chemin_complet = os.path.join(DOSSIER_IMAGES, nom_fichier)
            
            img_cible = preparer_image(chemin_complet)
            
            if img_cible is not None:
                # Comparaison logique (True/False converti en 1/0)
                correct = (ref == img_cible).astype(int)
                score_total = np.sum(correct)
                note = (score_total / 25) * 10
                FICHIER_TESTES += 1
                
                if note >= 8.5:
                    print(f"🎯 Image trouvée : {nom_fichier} au bout de {FICHIER_TESTES} images testées, note de : {note}/10")
                    

                # Si match parfait, on informe l'utilisateur et on sauvegarde une copie
                if note == 10 and deja_execute == False:
                    print(f"🎯 Première image trouvée : {nom_fichier} au bout de {FICHIER_TESTES} images testées.")
                    deja_execute = True

                resultats.append((nom_fichier, round(note, 2)))

    # Tri par score décroissant
    resultats.sort(key=lambda x: x[1], reverse=True)

    # Écriture du rapport final
    with open(FICHIER_RAPPORT, "w", encoding="utf-8") as f:
        f.write("CLASSEMENT DE SIMILARITÉ (Grille 5x5)\n\n")
        f.write(f"{FICHIER_TESTES} images testées\n\n")
        f.write("=" * 55 + "\n")
        for i, (nom, note) in enumerate(resultats, start=1):
            f.write(f"{i:02d}. {nom:<25} -> {note:>5}/10\n")
    
    print(f"\n✅ Analyse terminée avec succès.")
    print(f"📄 Rapport disponible : {FICHIER_RAPPORT}")

if __name__ == "__main__":
    analyser()