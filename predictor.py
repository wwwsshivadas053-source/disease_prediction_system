import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

model = load_model("static/models/disease_model.h5")

classes = [
    "Chickenpox",
    "Cowpox",
    "Healthy",
    "HFMD"
]

def predict_disease(img_path):

    img = image.load_img(
        img_path,
        target_size=(224,224)
    )

    img = image.img_to_array(img)

    img = img / 255.0

    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)

    idx = np.argmax(prediction)

    confidence = float(
        np.max(prediction)
    ) * 100

    return classes[idx], confidence