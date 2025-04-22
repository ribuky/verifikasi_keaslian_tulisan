import tensorflow as tf
import numpy as np
from load_dataset import load_dataset
from siamese_model import build_siamese_network
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# Load dataset
(X1, X2), Y = load_dataset()

# Split data (80% train, 20% test)
X1_train, X1_test, X2_train, X2_test, Y_train, Y_test = train_test_split(X1, X2, Y, test_size=0.2, random_state=42)

# Build model
model = build_siamese_network()

# Load weights
model.load_weights("siamese_model_weights.h5")
print("✅ Bobot model berhasil dimuat.")

# Compile ulang (tidak wajib tapi direkomendasikan)
model.compile(loss="binary_crossentropy", optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), metrics=["accuracy"])

# Evaluasi pada data test
loss, accuracy = model.evaluate([X1_test, X2_test], Y_test)
print(f"📊 Eval Loss: {loss:.4f}, Accuracy: {accuracy:.4f}")

# Prediksi untuk metrik lanjutan
Y_pred_prob = model.predict([X1_test, X2_test])
Y_pred = (Y_pred_prob > 0.5).astype("int32")

# Skor klasifikasi
print("\n🧠 Classification Report:")
print(classification_report(Y_test, Y_pred, digits=4))

# Confusion matrix
print("📉 Confusion Matrix:")
print(confusion_matrix(Y_test, Y_pred))
