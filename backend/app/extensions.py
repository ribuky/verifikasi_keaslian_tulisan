import tensorflow as tf
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from siamese_model import l1_distance

# DB & Auth
db = SQLAlchemy()
jwt = JWTManager()
blocked_tokens = set()

# Model load
MODEL_PATH = "best_siamese.h5"
model = None

def load_simese_model():
    global model
    if model is None:
        model = tf.keras.models.load_model(
            MODEL_PATH,
            custom_objects={"l1_distance": l1_distance},
            compile=False
        )
        print("✅ Model Siamese berhasil dimuat dari best_siamese.h5")
