import tensorflow as tf
import cv2
import numpy as np
import os
from siamese_model import build_siamese_network  # Pastikan model bisa dipanggil

IMG_SIZE = 128
DATASET_PATH = "dataset"

def load_image(image_path):
    """Preprocessing gambar sebelum dimasukkan ke model"""
    full_path = os.path.join(DATASET_PATH, image_path)

    if not os.path.exists(full_path):
        print(f"❌ ERROR: File tidak ditemukan -> {full_path}")
        return None

    img = cv2.imread(full_path, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        print(f"❌ ERROR: Gagal membaca gambar -> {full_path}")
        return None

    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img.astype("float32") / 255.0
    return np.expand_dims(img, axis=[0, -1])

# Buat ulang arsitektur model Siamese
model = build_siamese_network()

# Load bobot model
model.load_weights("siamese_model_weights.h5")
print("Bobot model berhasil dimuat!")

# Kompilasi ulang model sebelum pengujian
model.compile(loss="binary_crossentropy", optimizer=tf.keras.optimizers.Adam(learning_rate=0.001))
print("Model berhasil dikompilasi ulang!")

# Tes dengan gambar baru
img1 = load_image("test/5.png")
img2 = load_image("test/6.png")

prediction = model.predict([img1, img2])[0][0]
print(f"Similarity Score: {prediction:.4f}")

# Interpretasi hasil
if prediction > 0.75:
    print("✅ Gambar berasal dari siswa yang SAMA.")
else:
    print("❌ Gambar berasal dari siswa yang BERBEDA.")
