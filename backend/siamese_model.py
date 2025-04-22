import tensorflow as tf

IMG_SIZE = 128

def build_base_model():
    inputs = tf.keras.layers.Input(shape=(IMG_SIZE, IMG_SIZE, 1))

    x = tf.keras.layers.Conv2D(64, (3, 3), activation="relu", padding="same")(inputs)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(x)

    x = tf.keras.layers.Conv2D(128, (3, 3), activation="relu", padding="same")(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(x)

    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(128, activation="relu")(x)
    x = tf.keras.layers.Dropout(0.3)(x)

    model = tf.keras.models.Model(inputs, x)
    return model

@tf.keras.utils.register_keras_serializable()
def l1_distance(vectors):
    """L1 distance antara dua vektor embedding"""
    x, y = vectors
    return tf.math.abs(x - y)

def build_siamese_network():
    base_model = build_base_model()

    input_a = tf.keras.layers.Input(shape=(IMG_SIZE, IMG_SIZE, 1))
    input_b = tf.keras.layers.Input(shape=(IMG_SIZE, IMG_SIZE, 1))

    encoded_a = base_model(input_a)
    encoded_b = base_model(input_b)

    distance = tf.keras.layers.Lambda(l1_distance)([encoded_a, encoded_b])
    outputs = tf.keras.layers.Dense(1, activation="sigmoid")(distance)

    model = tf.keras.models.Model(inputs=[input_a, input_b], outputs=outputs)
    return model
