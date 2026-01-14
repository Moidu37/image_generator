import numpy as np
import png  # pip install pypng
import os
import uuid
from datetime import datetime

heure_debut = datetime.now()

width, height = 5, 5
num_images = 1000000
folder = "images"
os.makedirs(folder, exist_ok=True)

for _ in range(num_images):
    # Générer image 0 ou 255
    data = np.random.randint(0, 2, (height, width), dtype=np.uint8) * 255

    # Nom unique
    filename = f"image_{uuid.uuid4().hex}.png"
    filepath = os.path.join(folder, filename)

    # Sauvegarder PNG directement
    with open(filepath, 'wb') as f:
        writer = png.Writer(width, height, greyscale=True)
        writer.write(f, data.tolist())

heure_fin = datetime.now()
temps_total = heure_fin - heure_debut
print(f"{num_images} images générées dans '{folder}' !")
print(f"Code exécuté en {temps_total} !")
