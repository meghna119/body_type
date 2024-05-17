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
                    "Skirt": ["images/Women/a line skirt.png", "images/Women sketches/Skirts/wrap skirt .png","images/Women/handkerchief skirt .png", "images/Women/flip skirt .png", "images/Women/draped skirt .png"],
                    "Jumpsuits": ["images/Women/belted jumpsuit .png", "images/Women sketches/Jumpsuits /wide leg jumpsuit .png", "images/Women sketches/Jumpsuits /utility jumpsuit .png", "images/Women sketches/Jumpsuits /wrap jumpsuit .png", "images/Women/empire jumpsuit .png"],
                    "Pants": ["images/Women/harem pants .png", "images/Women/bootcut pants.png", "images/Women/Palazzo pants .png", "images/Women/pegged pants.png", "images/Women sketches/Pants women /wideleg jeans .png"],
                    "Necklines": ["images/Women sketches/Necklines /y neckline .png", "images/Women sketches/Necklines /v neckline.png", "images/Women sketches/Necklines /sweetheart neckline .png", "images/Women/scoop neckline .png", "images/Women/off shoulder neckline .png"],
                    "Tops": ["images/Women/off shoulder top .png", "images/Women/peplum top .png", "images/Women sketches/Tops women /wrap top.png", "images/Women/empire top.png", "images/Women/hoodie - top.png"],
                    "Sleeves": ["images/Women/cap sleeve .png", "images/Women/Bell sleeve.png", "images/Women/dolman sleeve.png", "images/Women/flutter sleeve .png", "images/Women/off shoulder sleeve .png"],
                    "TRADITIONAL WEAR": ["images/Women/aline kurta.png", "images/Women/anarkali kurta.png", "images/Women sketches/Traditional wear women /straight cut kurta.png", "images/Women/empire waist kurta.png", "images/Women sketches/Traditional wear women /sari.png"]
                }

            },
            "Male": {
                "TRIANGLE": {
                    "Collars": ["images/button down collar .png","images/Men sketches /Collars men /banded collar .png","images/Men sketches /Collars men /Mandarin collar .png","images/Men sketches /Collars men /spread collar .png","images/Men sketches /Collars men /pinned collar .png"],
                    "Shirts": ["images/Men sketches /Shirts men /vertical stripe shirt.png","images/Men sketches /Shirts men /linen shirt .png","images/Men sketches /Shirts men /tshirt .png","images/Men sketches /Shirts men /polo tshirt .png","images/Men sketches /Shirts men /henley shirt.png"],
                    "Pants": ["images/Men sketches /Pants /chinos.png","images/Men sketches /Pants /straight jeans .png","images/Men sketches /Pants /slim fit .png","images/Men sketches /Pants /cargo pants .png","images/Men sketches /Pants /shorts.png"]

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
