#!/usr/bin/env python3
from PIL import Image
import sys

# Funktion zum Vergleichen mit Toleranz
def is_near(a, b, tol=0.05):
    return abs(a - b) < tol

# Dateipfad aus Argument
if len(sys.argv) < 2:
    print("Usage: checkPicOrientation.py <image_path> <image_path>..." )
    sys.exit(0)

paths = sys.argv[1:]
wrong_images = []
for image_path in paths:

    # Ziel-Seitenverhältnisse (Breite/Höhe)
    target_ratios = [(4, 3), (16, 9)]

    # Bild öffnen
    image = Image.open(image_path)
    width, height = image.size
    ratio = width / height

    # Überprüfen, ob das Bild im gewünschten Querformat liegt
    format_false = False
    for w, h in target_ratios:
        if not is_near(ratio, w / h):
            format_false = True

    if format_false:
        wrong_images.append(image_path)


if len(wrong_images) != 0:
    imageString = ""
    for image in wrong_images:
        imageString += image + " "
    print(f"wrong_sized_images={imageString}")
