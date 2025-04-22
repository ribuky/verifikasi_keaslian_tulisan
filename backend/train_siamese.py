import os
import argparse
import tensor as tf
import matplotlib.pyplot as plt
from datetime import datetime

from load_dataset import load_dataset
from siamese_model import build_siamese_network

def plot_training(history, out_dir="logs"):
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(history.history["loss"], label="Train Loss")
    plt.plot(history.history["val_loss"], label="Val Loss")
    plt.title("Loss Curve")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(history.history["accuracy"], label="Train Accuracy")
    plt.plot(history.history["val_accuracy"], label="Val Accuracy")
    plt.title("Accuracy Curve")
    plt.legend()

    os.makedirs(out_dir, exist_ok=True)
    plt.savefig(os.path.join(out_dir, "training_plot.png"))
    plt.show()

def main(args):
    print("🚀 Memuat dataset...")
    (X1, X2), Y = load_dataset()

    print("🔧 Membuat model Siamese...")
    model = build_siamese_network()
    model.compile(
        loss="binary_crossentropy",
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        metrics=["accuracy"]
    )

    log_dir = os.path.join("logs", "fit", datetime.now().strftime("%Y%m%d-%H%M%S"))
    tensorboard_cb = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

    callbacks = [
        tf.keras.callbacks.ModelCheckpoint("best_siamese.h5", monitor="val_loss", save_best_only=True),
        tf.keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True),
        tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, verbose=1),
        tensorboard_cb
    ]

    print("🎯 Training mulai...")
    history = model.fit(
        [X1, X2], Y,
        batch_size=args.batch_size,
        epochs=args.epochs,
        validation_split=args.val_split,
        callbacks=callbacks
    )

    print("📈 Menyimpan grafik pelatihan...")
    plot_training(history)

    if args.save_model:
        model.save("best_siamese.h5")
        print("✅ Model architecture + weights saved as 'best_siamese.h5'")
    else:
        model.save_weights("siamese_model.weights.h5")
        print("✅ Model weights only saved as 'siamese_model_weights.h5'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a Siamese Neural Network on handwriting pairs.")
    parser.add_argument("--epochs", type=int, default=50, help="Jumlah epoch training (default: 50)")
    parser.add_argument("--batch-size", type=int, default=16, help="Ukuran batch training (default: 16)")
    parser.add_argument("--val-split", type=float, default=0.2, help="Rasio data untuk validation (default: 0.2)")
    parser.add_argument("--save-model", action="store_true", help="Simpan seluruh model (bukan hanya bobot)")

    args = parser.parse_args()
    main(args)
