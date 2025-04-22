import os
import cv2
import numpy as np
import pandas as pd

IMG_SIZE = 128
DATASET_PATH = "dataset"
CSV_FILE = "dataset_pairs.csv"

def load_image(image_path):
    """Memuat gambar, konversi ke grayscale, resize, normalisasi"""
    full_path = os.path.join(DATASET_PATH, image_path)

    if not os.path.exists(full_path):
        print(f"❌ Gambar tidak ditemukan: {full_path}")
        return None

    img = cv2.imread(full_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img.astype("float32") / 255.0

    return img

def augment_image(img):
    """Augmentasi ringan - rotasi & translasi"""
    rows, cols = img.shape

    # Rotasi
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), np.random.uniform(-5, 5), 1)
    img = cv2.warpAffine(img, M, (cols, rows), borderMode=cv2.BORDER_REFLECT)

    # Translasi
    tx = np.random.uniform(-5, 5)
    ty = np.random.uniform(-5, 5)
    M = np.float32([[1, 0, tx], [0, 1, ty]])
    img = cv2.warpAffine(img, M, (cols, rows), borderMode=cv2.BORDER_REFLECT)

    return img

def load_dataset():
    df = pd.read_csv(CSV_FILE)
    images1, images2, labels = [], [], []

    for _, row in df.iterrows():
        img1 = load_image(row["Image1"])
        img2 = load_image(row["Image2"])
        if img1 is not None and img2 is not None:
            if np.random.rand() < 0.5:
                img1 = augment_image(img1)
                img2 = augment_image(img2)
            images1.append(img1)
            images2.append(img2)
            labels.append(row["Label"])

    X1 = np.expand_dims(np.array(images1), axis=-1)
    X2 = np.expand_dims(np.array(images2), axis=-1)
    Y = np.array(labels).astype("float32")

    # Statistik
    pos = np.sum(Y)
    neg = len(Y) - pos
    print(f"Jumlah Pasangan Sama (1): {int(pos)}")
    print(f"Jumlah Pasangan Beda (0): {int(neg)}")

    return (X1, X2), Y
