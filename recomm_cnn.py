#!/usr/bin/env python
# coding: utf-8

# In[12]:


import tensorflow as tf


# In[17]:


import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint
from PIL import Image

# Constants
IMG_SIZE = (224, 224)
NUM_CLASSES = 10  # Assuming you have 10 cloth patterns

# Load and preprocess your dataset
@st.cache(allow_output_mutation=True)
def load_and_preprocess_dataset():
    dataset = pd.read_csv('dataset.csv')
    images = []
    labels = []

    for _, row in dataset.iterrows():
        image_path = row['Image Path']
        label = row['Cloth Pattern ']

        img = load_img(image_path, target_size=IMG_SIZE)
        img = img_to_array(img) / 255.0  # Normalize pixel values
        images.append(img)
        labels.append(label)

    images = np.array(images)
    labels = np.array(labels)

    train_images, test_images, train_labels, test_labels = train_test_split(images, labels, test_size=0.2, random_state=42)

    return train_images, train_labels, test_images, test_labels

# Define your CNN model
def create_cnn_model(input_shape, num_classes):
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    return model

# Train the CNN model
def train_cnn_model(train_images, train_labels, test_images, test_labels, num_classes, epochs=10, batch_size=32):
    input_shape = train_images.shape[1:]
    model = create_cnn_model(input_shape, num_classes)
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    checkpoint = ModelCheckpoint('best_model.h5', monitor='val_accuracy', mode='max', verbose=1, save_best_only=True)
    history = model.fit(train_images, train_labels, epochs=epochs, batch_size=batch_size, 
                        validation_data=(test_images, test_labels), callbacks=[checkpoint])
    return model, history

# Predict the class of an image
def predict_image_class(model, image):
    img = image.resize(IMG_SIZE)
    img = img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    prediction = model.predict(img)
    predicted_class = np.argmax(prediction, axis=1)[0]
    return predicted_class

# Streamlit app
st.title("Cloth Pattern Classifier")

# Load and preprocess the dataset
if st.button('Load and preprocess dataset'):
    train_images, train_labels, test_images, test_labels = load_and_preprocess_dataset()
    st.success("Dataset loaded and preprocessed successfully.")

# Train the CNN model
if st.button('Train CNN model'):
    if 'train_images' in locals():
        num_classes = len(set(train_labels))
        model, history = train_cnn_model(train_images, train_labels, test_images, test_labels, num_classes)
        st.success("Model trained successfully.")
        test_loss, test_accuracy = model.evaluate(test_images, test_labels)
        st.write(f'Test Accuracy: {test_accuracy:.4f}')
        model.save('your_cnn_model.h5')
        st.success("Model saved as your_cnn_model.h5")
    else:
        st.error("Dataset not loaded. Please load the dataset first.")

# Display images and classify
st.header("Display and Classify Image")
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("")
    st.write("Classifying...")

    try:
        model = load_model('your_cnn_model.h5')
        predicted_class = predict_image_class(model, image)
        st.write(f"Predicted Class: {predicted_class}")
    except Exception as e:
        st.error(f"Error loading model: {e}")

