import tensorflow as tf
import numpy as np
import cv2
from tensorflow.keras.models import Model


def make_gradcam_heatmap(img_array, model, last_conv_layer_name):

    grad_model = Model(
        [model.inputs],
        [
            model.get_layer(last_conv_layer_name).output,
            model.output
        ]
    )

    with tf.GradientTape() as tape:

        conv_outputs, predictions = grad_model(img_array)

        pred_index = tf.argmax(predictions[0])

        class_channel = predictions[:, pred_index]

    grads = tape.gradient(
        class_channel,
        conv_outputs
    )

    pooled_grads = tf.reduce_mean(
        grads,
        axis=(0, 1, 2)
    )

    conv_outputs = conv_outputs[0]

    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]

    heatmap = tf.squeeze(heatmap)

    heatmap = tf.maximum(heatmap, 0)

    heatmap /= tf.math.reduce_max(heatmap)

    return heatmap.numpy()

def save_gradcam(
        image_path,
        model,
        last_conv_layer_name,
        output_path
):

    img = tf.keras.preprocessing.image.load_img(
        image_path,
        target_size=(224,224)
    )

    img_array = tf.keras.preprocessing.image.img_to_array(img)

    img_array = np.expand_dims(
        img_array,
        axis=0
    ) / 255.0

    heatmap = make_gradcam_heatmap(
        img_array,
        model,
        last_conv_layer_name
    )

    image = cv2.imread(image_path)

    heatmap = cv2.resize(
        heatmap,
        (image.shape[1], image.shape[0])
    )

    heatmap = np.uint8(255 * heatmap)

    heatmap = cv2.applyColorMap(
        heatmap,
        cv2.COLORMAP_JET
    )

    superimposed_img = cv2.addWeighted(
        image,
        0.6,
        heatmap,
        0.4,
        0
    )

    cv2.imwrite(
        output_path,
        superimposed_img
    )