import tensorflow as tf
import numpy as np
from PIL import Image

model = tf.keras.models.load_model(
    "qr_classifier.keras"
)


def predict_qr(image):

    image = image.convert("RGB")
    image = image.resize((128, 128))

    image_array = np.array(image)
    image_array = image_array / 255.0

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    prediction = model.predict(
        image_array,
        verbose=0
    )

    score = float(prediction[0][0])

    if score > 0.5:

        label = "BENIGN"

        confidence = round(
            score * 100,
            2
        )

    else:

        label = "MALICIOUS"

        confidence = round(
            (1 - score) * 100,
            2
        )

    return {
        "prediction": label,
        "confidence": confidence
    }