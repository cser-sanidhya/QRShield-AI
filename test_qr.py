import tensorflow as tf
import numpy as np
from tensorflow.keras.utils import load_img, img_to_array

model = tf.keras.models.load_model("qr_classifier.keras")

img = load_img("test_qr.png", target_size=(128, 128))

img_array = img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array = img_array / 255.0

prediction = model.predict(img_array)

print("Prediction:", prediction[0][0])

if prediction[0][0] > 0.5:
    print("MALICIOUS QR")
else:
    print("BENIGN QR")