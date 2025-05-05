#!/usr/bin/env python3

import cv2
import logging
import sys

def resize_image(filename: str, target_ratio: float):
    # Bild laden
    image = cv2.imread(filename)
    height, width = image.shape[:2]
    logging.debug(f"Image size: {width}x{height}")

    h, w, x, y = check_for_main_motive_bounding_box(image)

    center_x, center_y = x + w // 2, y + h // 2
    logging.debug(f"Center: {center_x}, {center_y}")
    new_h, new_w = correct_bounding_box_to_image_ratio(h, height, target_ratio, w, width)

    x1, x2, y1, y2 = calculate_to_image_pixels(center_x, center_y, height, new_h, new_w, width)

    # Bild zuschneiden und speichern
    cropped = image[y1:y2, x1:x2]
    cv2.imwrite(filename, cropped)


def correct_bounding_box_to_image_ratio(h, height, target_ratio, w, width):
    if w / h < target_ratio:
        if w / target_ratio < height:
            new_w = w
            new_h = int(w / target_ratio)
        else:
            new_h = h
            new_w = int(h * target_ratio)
    else:
        if h * target_ratio < width:
            new_h = int(w / target_ratio)
            new_w = w
        else:
            new_h = h
            new_w = int(h * target_ratio)

    logging.debug(f"New size: {new_w}x{new_h}")

    return new_h, new_w


def calculate_to_image_pixels(center_x, center_y, height, new_h, new_w, width):
    # Begrenzungen sicherstellen
    x1 = max(0, center_x - (new_w // 2))
    y1 = max(0, center_y - new_h // 2)
    x2 = min(width, center_x + new_w // 2)
    y2 = min(height, center_y + new_h // 2)

    logging.debug(f"New coordinates: {x1}:{x2}x{y1}:{y2}")

    return x1, x2, y1, y2

def check_for_main_motive_bounding_box(image):
    # Salienz-Erkennung (OpenCV Deep Learning)
    saliency = cv2.saliency.StaticSaliencyFineGrained_create()
    (success, saliencyMap) = saliency.computeSaliency(image)
    saliencyMap = (saliencyMap * 255).astype("uint8")
    # Konturen finden und groesste Komponente als Hauptelement waehlen
    contours, _ = cv2.findContours(saliencyMap, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    logging.debug(f"Bounding box: {x}x{y}, width: {w}, height: {h}")
    return h, w, x, y


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
    if len(sys.argv) < 2:
        print("Usage: imageCrop.py <image_path> <image_path>..." )
        sys.exit(0)

    paths = sys.argv[1:]
    for image_path in paths:
        resize_image(image_path, 16/9)
