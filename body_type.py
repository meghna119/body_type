#!/usr/bin/env python
# coding: utf-8

# In[2]:


import csv
import os

# Function to get list of image files in a folder
def get_image_files(folder):
    image_files = []
    for file in os.listdir(folder):
        if file.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            # Removing file extension from image name
            image_name = os.path.splitext(file)[0]
            image_files.append((os.path.join(folder, file), image_name))
    return image_files

# Folder containing images
image_folder = r"images/women"

# Output CSV file
csv_file = 'Women.csv'

# Get list of image files
image_files = get_image_files(image_folder)

# Write image paths and their corresponding names into a CSV file
with open(csv_file, 'w', newline='') as csvfile:
    fieldnames = ['Image Path', 'Pattern']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for image_path, image_name in image_files:
        writer.writerow({'Image Path': image_path, 'Pattern': image_name})

print("CSV file created successfully.")


# In[ ]:


import csv
import os

# Function to get list of image files in a folder
def get_image_files(folder):
    image_files = []
    for file in os.listdir(folder):
        if file.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            # Removing file extension from image name
            image_name = os.path.splitext(file)[0]
            image_files.append((os.path.join(folder, file), image_name))
    return image_files

# Folder containing images
image_folder = "images"

# Output CSV file
csv_file = 'Men.csv'

# Get list of image files
image_files = get_image_files(image_folder)

# Write image paths and their corresponding names into a CSV file
with open(csv_file, 'w', newline='') as csvfile:
    fieldnames = ['Image Path', 'Pattern']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for image_path, image_name in image_files:
        writer.writerow({'Image Path': image_path, 'Pattern': image_name})

print("CSV file created successfully.")


# In[ ]:


import csv
import os
from PIL import Image

# Function to get list of image files in a folder
def get_image_files(folder):
    image_files = []
    for file in os.listdir(folder):
        if file.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            # Removing file extension from image name
            image_name = os.path.splitext(file)[0]
            image_files.append((os.path.join(folder, file), image_name))
    return image_files

# Function to open and display an image from its file path
def display_image(image_path):
    try:
        image = Image.open(image_path)
        image.show()
    except Exception as e:
        print(f"Error: {e}")

# Folder containing images
image_folder = r"images"  # Use raw string to handle backslashes

# Output CSV file
csv_file = 'Men.csv'

# Get list of image files
image_files = get_image_files(image_folder)

# Write image paths and their corresponding names into a CSV file
with open(csv_file, 'w', newline='') as csvfile:
    fieldnames = ['Image Path', 'Pattern']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for image_path, image_name in image_files:
        writer.writerow({'Image Path': image_path, 'Pattern': image_name})

print("CSV file created successfully.")

# Example usage: Display the first image from the dataset
if image_files:
    first_image_path = image_files[0][0]  # Assuming image_files is not empty
    display_image(first_image_path)
else:
    print("No images found in the dataset folder.")

