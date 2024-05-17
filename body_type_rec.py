import streamlit as st
import pandas as pd
import pickle
from PIL import Image

# Constants
FEMALE_GENDER = 1
MALE_GENDER = 2

class BodyClassifierApp:
    def __init__(self):
        # Load the trained model
        self.rf_model = self.load_rf_model()
        self.recommendation_images = {
            "Female": {
                "APPLE": {
                    "Skirt": ["images/women/a line skirt .png", "images/women/wrap skirt .png","images/women/handkerchief skirt .png", "images/women/flip skirt .png", "images/women/draped skirt .png"],
                    "Jumpsuits": ["images/women/belted jumpsuit .png", "images/women/wide leg jumpsuit .png", "images/women/utility jumpsuit .png", "images/women/wrap jumpsuit .png", "images/women/empire jumpsuit .png"],
                    "Pants": ["images/women/harem pants .png", "images/women/bootcut pants.png", "images/women/Palazzo pants .png", "images/women/pegged pants.png", "images/women/wideleg jeans .png"],
                    "Necklines": ["images/women/y neckline .png", "images/women/v neckline.png", "images/women/sweetheart neckline .png", "images/women/scoop neckline .png", "images/women/off shoulder neckline .png"],
                    "Tops": ["images/women/off shoulder top .png", "images/women/peplum top .png", "images/women/wrap top.png", "images/women/empire top.png", "images/women/hoodie .png"],
                    "Sleeves": ["images/women/cap sleeve .png", "images/women/Bell sleeve.png", "images/women/dolman sleeve.png", "images/women/flutter sleeve .png", "images/women/off shoulder sleeve .png"],
                    "TRADITIONAL WEAR": ["images/women/aline kurta.png", "images/women/anarkali kurta.png", "images/women/straight cut kurta.png", "images/women/empire waist kurta.png", "images/women/sari.png"]

                }, "RECTANGLE": {
                    "Skirt": ["images/women/a line skirt .png", "images/women/pencil skirt .png","images/women/tulip skirt.png", "images/women/flip skirt .png", "images/women/wrap skirt .png"],
                    "Jumpsuits": ["images/women/belted jumpsuit .png", "images/women/peplum jumpsuit .png", "images/women/ruffled jumpsuit .png", "images/women/basic jumpsuit .png", "images/women/empire jumpsuit .png"],
                    "Pants": ["images/women/cargo pants .png", "images/women/bootcut pants.png", "images/women/Palazzo pants .png", "images/women/pegged pants.png", "images/women/wideleg jeans .png"],
                    "Necklines": ["images/women/halter neckline .png", "images/women/v neckline.png", "images/women/sweetheart neckline .png", "images/women/scoop neckline .png", "images/women/halter strap neckline .png"],
                    "Tops": ["images/women/halter top.png", "images/women/peplum top .png", "images/women/belted top.png", "images/women/empire top.png", "images/women/hoodie .png"],
                    "Sleeves": ["images/women/cap sleeve .png", "images/women/puff sleeves .png", "images/women/dolman sleeve.png", "images/women/flutter sleeve .png", "images/women/3_4 th sleeve .png"],
                    "TRADITIONAL WEAR": ["images/women/bandhani saree.png", "images/women/anarkali kurta.png", "images/women/flared kurta.png", "images/women/empire waist kurta.png", "images/women/pleated kurta .png"]}
                

               
                


            },
            "Male": {
                "TRIANGLE": {
                    "Collars": ["images/button down collar .png","images/banded collar .png","images/Mandarin collar .png","images/spread collar .png","images/pinned collar .png"],
                    "Shirts": ["images/vertical stripe shirt.png","images/linen shirt .png","images/tshirt .png","images/polo tshirt .png","images/henley shirt.png"],
                    "Pants": ["images/chinos.png","images/straight jeans .png","images/slim fit .png","images/cargo pants .png","images/shorts.png"]

                    

                }
                
                
                }
            }
        

    def load_rf_model(self):
        try:
            with open('random_forest_model.pkl', 'rb') as file:
                model = pickle.load(file, encoding='utf-8')
            return model
        except Exception as e:
            st.error(f"Failed to load the RandomForestClassifier model: {e}")
            return None

    def classify(self, gender, age, measurements):
        try:
            data = pd.DataFrame(columns=['Gender', 'Age', 'Shoulder', 'Waist', 'Hips', 'Bust', 'Chest'])
            data.loc[0] = [FEMALE_GENDER if gender == "Female" else MALE_GENDER, age] + measurements

            if self.rf_model:
                body_type = self.rf_model.predict(data)[0]
                st.success(f"Predicted Body Type: {body_type}")
                self.provide_recommendations(body_type, gender)
            else:
                st.error("RandomForestClassifier Model not loaded.")
        except Exception as e:
            st.error(str(e))

    def provide_recommendations(self, body_type, gender):
        try:
            recommendations = self.recommendation_images[gender].get(body_type, {})
            self.display_recommendations(recommendations)
        except Exception as e:
            st.error(str(e))

    def display_recommendations(self, recommendations):
        try:
            for cloth_pattern, image_paths in recommendations.items():
                st.subheader(f"Top 5 images for {cloth_pattern}:")
                for image_path in image_paths:
                    st.image(image_path, caption=image_path, use_column_width=True)
        except Exception as e:
            st.error(f"Error loading image: {e}")

# Initialize the app
body_classifier = BodyClassifierApp()

st.title("Body Measurement Classifier")

# Gender selection
gender = st.selectbox("Gender:", ["Female", "Male"])

# Age input
age = st.number_input("Age:", min_value=0)

# Measurement inputs
measurement_labels = ["Shoulder", "Waist", "Hips", "Bust", "Chest"]
measurements = []
for label in measurement_labels:
    measurement = st.number_input(f"{label}:", min_value=0.0)
    measurements.append(measurement)

if st.button("Classify"):
    body_classifier.classify(gender, age, measurements)

