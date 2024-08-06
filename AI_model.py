import os
import tensorflow as tf
from tensorflow.keras import layers
import pathlib
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import camera as cam
from tkinter import messagebox

resize_height = 64
resize_width = 64
batch_size = 2


def edge_detection(event=None):
    plt.close('all')
    messagebox.showinfo('AI model info', 'AI is processing the dataset for edge detection images...')
    main('edge')


def grayscale(event=None):
    plt.close('all')
    messagebox.showinfo('AI model info', 'AI is processing the dataset for grayscale images...')
    main('gray')


def original(event=None):
    plt.close('all')
    messagebox.showinfo('AI model info', 'AI is processing the dataset for original images...')
    main('orig')


def create_datasets(train_directory, test_directory):
    ds_train = tf.data.Dataset.list_files(str(pathlib.Path(train_directory + '*.png')))
    ds_test = tf.data.Dataset.list_files(str(pathlib.Path(test_directory + '*.png')))
    ds_train = ds_train.map(lambda x: process_path(x, training=True)).batch(batch_size)
    ds_test = ds_test.map(lambda x: process_path(x, training=False)).batch(batch_size)
    return ds_train, ds_test


def process_path(file_path, training=True):
    image = tf.io.read_file(file_path)
    image = tf.image.decode_png(image, channels=1)
    image = tf.image.resize(image, [resize_height, resize_width])
    label = tf.strings.split(file_path, os.sep)
    label = tf.strings.substr(label[-1], pos=0, len=1)
    label = tf.strings.to_number(label, out_type=tf.int64)
    return image, label


def build_model():
    model = tf.keras.Sequential(
        [
            layers.Input((resize_height, resize_width, 1)),
            layers.Conv2D(16, 3, padding="same", activation='relu'),
            layers.Conv2D(32, 3, padding="same", activation='relu'),
            layers.MaxPooling2D(),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dense(2, activation='softmax')
        ]
    )
    model.compile(
        optimizer=tf.keras.optimizers.Adam(),
        loss=[tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False)],
        metrics=["accuracy"],
    )
    return model


def train_model(model, ds_train, epochs=1):
    model.fit(ds_train, epochs=epochs, verbose=2)
    return model


def evaluate_model(model, ds_test):
    predictions = model.predict(ds_test)
    return predictions


def preprocess_image(image_path):
    image = tf.io.read_file(image_path)
    image = tf.image.decode_png(image, channels=1)
    image = tf.image.resize(image, [resize_height, resize_width])
    image = tf.expand_dims(image, axis=0)
    return image


def load_and_predict(directory, model):
    image_paths = list(pathlib.Path(directory).glob('*.png'))
    predictions = []
    images = []
    for image_path in image_paths:
        processed_image = preprocess_image(str(image_path))
        prediction = model.predict(processed_image)
        predicted_label = tf.argmax(prediction, axis=1).numpy()[0]
        predictions.append(predicted_label)
        images.append(image_path)
    return images, predictions


def plot_results(images, predictions):
    plt.figure(figsize=(20, 10))
    for i, (image_path, prediction) in enumerate(zip(images, predictions)):
        plt.subplot(2, len(images)//2 + len(images)%2, i + 1)
        image = Image.open(image_path)
        plt.imshow(image, cmap='gray' if image.mode == 'L' else None)
        title = f"{os.path.basename(image_path)} - {'Not Oily' if prediction == 0 else 'Oily'}"
        plt.title(title)
        plt.axis('off')
    plt.tight_layout()

    unique, counts = np.unique(predictions, return_counts=True)
    labels = ['Not Oily', 'Oily']
    counts_dict = dict(zip(unique, counts))
    counts_list = [counts_dict.get(i, 0) for i in range(len(labels))]
    total = sum(counts_list)
    percentages = [count / total * 100 for count in counts_list]

    plt.figure(figsize=(8, 6))
    plt.pie(percentages, labels=labels, autopct='%1.1f%%', colors=['blue', 'green'])
    plt.title('Prediction Percentages')
    plt.show()


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def main(mode):
    train_directory = resource_path('data/' + mode + '/train/')
    test_directory = resource_path('data/' + mode + '/test/' + str(cam.respondent) + '/')

    ds_train, ds_test = create_datasets(train_directory, test_directory)

    model = build_model()
    model = train_model(model, ds_train)

    images, predictions = load_and_predict(test_directory, model)
    plot_results(images, predictions)
