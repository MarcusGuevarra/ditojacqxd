import os
import tensorflow as tf
from tensorflow.keras import layers
import pathlib
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import camera as cam

# Constants
resize_height = 64
resize_width = 64
batch_size = 2

# Functions
def edge_detection():
    plt.close('all')
    main('edge')

def grayscale():
    plt.close('all')
    main('gray')

def original():
    plt.close('all')
    main('orig')


def create_datasets(train_directory, test_directory):
    """Creates training and testing datasets."""
    ds_train = tf.data.Dataset.list_files(str(pathlib.Path(train_directory + '*.png')))
    ds_test = tf.data.Dataset.list_files(str(pathlib.Path(test_directory + '*.png')))
    ds_train = ds_train.map(lambda x: process_path(x, training=True)).batch(batch_size)
    ds_test = ds_test.map(lambda x: process_path(x, training=False)).batch(batch_size)
    return ds_train, ds_test

def process_path(file_path, training=True):
    """Processes a single image file path into a resized image tensor and a label."""
    image = tf.io.read_file(file_path)
    image = tf.image.decode_png(image, channels=1)
    image = tf.image.resize(image, [resize_height, resize_width])
    label = tf.strings.split(file_path, os.sep)
    label = tf.strings.substr(label[-1], pos=0, len=1)
    label = tf.strings.to_number(label, out_type=tf.int64)
    return image, label

def build_model():
    """Builds and compiles the Keras model."""
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
    """Trains the model."""
    model.fit(ds_train, epochs=epochs, verbose=2)
    return model

def evaluate_model(model, ds_test):
    """Evaluates the model and returns predictions."""
    predictions = model.predict(ds_test)
    return predictions

def preprocess_image(image_path):
    """Preprocesses a single image for prediction."""
    image = tf.io.read_file(image_path)
    image = tf.image.decode_png(image, channels=1)
    image = tf.image.resize(image, [resize_height, resize_width])
    image = tf.expand_dims(image, axis=0)  # Add batch dimension
    return image

def load_and_predict(directory, model):
    """Loads images from a directory, preprocesses them, and makes predictions."""
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
    """Plots the results using Matplotlib."""
    plt.figure(figsize=(20, 10))
    for i, (image_path, prediction) in enumerate(zip(images, predictions)):
        plt.subplot(2, len(images)//2 + len(images)%2, i + 1)
        image = Image.open(image_path)
        plt.imshow(image, cmap='gray' if image.mode == 'L' else None)
        title = f"{os.path.basename(image_path)} - {'Not Oily' if prediction == 0 else 'Oily'}"
        plt.title(title)
        plt.axis('off')
    plt.tight_layout()

    # Create a pie chart for prediction percentages
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

# Main Execution

def main(mode):
    # Paths
    train_directory = './data/' + mode + '/train/'
    test_directory = './data/' + mode + '/survey_data/' + str(cam.respondent) + '/'

    # Create datasets
    ds_train, ds_test = create_datasets(train_directory, test_directory)

    # Build and train the model
    model = build_model()
    model = train_model(model, ds_train)

    # Evaluate the model
    predictions = evaluate_model(model, ds_test)
    print(predictions)

    # Load images and predict
    images, predictions = load_and_predict(test_directory, model)

    # Plot the results
    plot_results(images, predictions)
