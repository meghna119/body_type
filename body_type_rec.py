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
                    "Skirt": [("A-line Skirt", "images/women/a line skirt .png"), 
                              ("Wrap Skirt", "images/women/wrap skirt .png"),
                              ("Handkerchief Skirt", "images/women/handkerchief skirt .png"), 
                              ("Flip Skirt", "images/women/flip skirt .png"), 
                              ("Draped Skirt", "images/women/draped skirt .png")],
                    "Jumpsuits": [("Belted Jumpsuit", "images/women/belted jumpsuit .png"), 
                                  ("Wide Leg Jumpsuit", "images/women/wide leg jumpsuit .png"), 
                                  ("Utility Jumpsuit", "images/women/utility jumpsuit .png"), 
                                  ("Wrap Jumpsuit", "images/women/wrap jumpsuit .png"), 
                                  ("Empire Jumpsuit", "images/women/empire jumpsuit .png")],
                    "Pants": [("Harem Pants", "images/women/harem pants .png"), 
                              ("Bootcut Pants", "images/women/bootcut pants.png"), 
                              ("Palazzo Pants", "images/women/Palazzo pants .png"), 
                              ("Pegged Pants", "images/women/pegged pants.png"), 
                              ("Wide-leg Jeans", "images/women/wideleg jeans .png")],
                    "Necklines": [("Y Neckline", "images/women/y neckline .png"), 
                                  ("V Neckline", "images/women/v neckline.png"), 
                                  ("Sweetheart Neckline", "images/women/sweetheart neckline .png"), 
                                  ("Scoop Neckline", "images/women/scoop neckline .png"), 
                                  ("Off Shoulder Neckline", "images/women/off shoulder neckline .png")],
                    "Tops": [("Off Shoulder Top", "images/women/off shoulder top .png"), 
                             ("Peplum Top", "images/women/peplum top .png"), 
                             ("Wrap Top", "images/women/wrap top.png"), 
                             ("Empire Top", "images/women/empire top.png"), 
                             ("Hoodie", "images/women/hoodie .png")],
                    "Sleeves": [("Cap Sleeve", "images/women/cap sleeve .png"), 
                                ("Bell Sleeve", "images/women/Bell sleeve.png"), 
                                ("Dolman Sleeve", "images/women/dolman sleeve.png"), 
                                ("Flutter Sleeve", "images/women/flutter sleeve .png"), 
                                ("Off Shoulder Sleeve", "images/women/off shoulder sleeve .png")],
                    "TRADITIONAL WEAR": [("A-line Kurta", "images/women/aline kurta.png"), 
                                         ("Anarkali Kurta", "images/women/anarkali kurta.png"), 
                                         ("Straight Cut Kurta", "images/women/straight cut kurta.png"), 
                                         ("Empire Waist Kurta", "images/women/empire waist kurta.png"), 
                                         ("Georgette Saree", "images/women/Georgette saree .png")]
                },
                "RECTANGLE": {
                    "Skirt": [("A-line Skirt", "images/women/a line skirt .png"), 
                              ("Pencil Skirt", "images/women/pencil skirt .png"),
                              ("Tulip Skirt", "images/women/tulip skirt.png"), 
                              ("Flip Skirt", "images/women/flip skirt .png"), 
                              ("Wrap Skirt", "images/women/wrap skirt .png")],
                    "Jumpsuits": [("Belted Jumpsuit", "images/women/belted jumpsuit .png"), 
                                  ("Peplum Jumpsuit", "images/women/peplum jumpsuit .png"), 
                                  ("Ruffled Jumpsuit", "images/women/ruffled jumpsuit .png"), 
                                  ("Basic Jumpsuit", "images/women/basic jumpsuit .png"), 
                                  ("Empire Jumpsuit", "images/women/empire jumpsuit .png")],
                    "Pants": [("Cargo Pants", "images/women/cargo pants .png"), 
                              ("Bootcut Pants", "images/women/bootcut pants.png"), 
                              ("Palazzo Pants", "images/women/Palazzo pants .png"), 
                              ("Pegged Pants", "images/women/pegged pants.png"), 
                              ("Wide-leg Jeans", "images/women/wideleg jeans .png")],
                    "Necklines": [("Halter Neckline", "images/women/halter neckline .png"), 
                                  ("V Neckline", "images/women/v neckline.png"), 
                                  ("Sweetheart Neckline", "images/women/sweetheart neckline .png"), 
                                  ("Scoop Neckline", "images/women/scoop neckline .png"), 
                                  ("Halter Strap Neckline", "images/women/halter strap neckline .png")],
                    "Tops": [("Halter Top", "images/women/halter top.png"), 
                             ("Peplum Top", "images/women/peplum top .png"), 
                             ("Belted Top", "images/women/belted top.png"), 
                             ("Empire Top", "images/women/empire top.png"), 
                             ("Hoodie", "images/women/hoodie .png")],
                    "Sleeves": [("Cap Sleeve", "images/women/cap sleeve .png"), 
                                ("Puff Sleeves", "images/women/puff sleeves .png"), 
                                ("Dolman Sleeve", "images/women/dolman sleeve.png"), 
                                ("Flutter Sleeve", "images/women/flutter sleeve .png"), 
                                ("3/4 Sleeve", "images/women/3_4 th sleeve .png")],
                    "TRADITIONAL WEAR": [("Chiffon Saree", "images/women/chiffon saree .png"), 
                                         ("Anarkali Kurta", "images/women/anarkali kurta.png"), 
                                         ("Flared Kurta", "images/women/flared kurta.png"), 
                                         ("Empire Waist Kurta", "images/women/empire waist kurta.png"), 
                                         ("Pleated Kurta", "images/women/pleated kurta .png")]
                },
                "PEAR": {
                    "Skirt": [("A-line Skirt", "images/women/a line skirt .png"), 
                              ("Midi Skirt", "images/women/midi skirt .png"),
                              ("Knee Length Skirt", "images/women/knee length skirt.png"), 
                              ("Flip Skirt", "images/women/flip skirt .png"), 
                              ("Wrap Skirt", "images/women/wrap skirt .png")],
                    "Jumpsuits": [("Belted Jumpsuit", "images/women/belted jumpsuit .png"), 
                                  ("Striped Jumpsuit", "images/women/striped jumpsuit .png"), 
                                  ("Ruffled Jumpsuit", "images/women/ruffled jumpsuit .png"), 
                                  ("Flared Jumpsuit", "images/women/flared jumpsuit.png"), 
                                  ("Ruffled Jumpsuit", "images/women/ruffled jumpsuit .png")],
                    "Pants": [("Flared Jeans", "images/women/flared jeans.png"), 
                              ("Bootcut Pants", "images/women/bootcut pants.png"), 
                              ("Palazzo Pants", "images/women/Palazzo pants .png"), 
                              ("Trouser", "images/women/trouser.png"),
                              ("Wide-leg Jeans", "images/women/wideleg jeans .png")],
                    "Necklines": [("Halter Neckline", "images/women/halter neckline .png"), 
                                  ("Bardot Neckline", "images/women/bardot neckline .png"), 
                                  ("Off Shoulder Neckline", "images/women/off shoulder neckline .png"), 
                                  ("Scoop Neckline", "images/women/scoop neckline .png"), 
                                  ("Halter Strap Neckline", "images/women/halter strap neckline .png")],
                    "Tops": [("Halter Top", "images/women/halter top.png"), 
                             ("Bardot Neck Top", "images/women/bardot neck top .png"), 
                             ("Belted Top", "images/women/belted top.png"), 
                             ("Off Shoulder Top", "images/women/off shoulder top .png"), 
                             ("Scoop Neck Tops", "images/women/scoop neck tops.png")],
                    "Sleeves": [("Cap Sleeve", "images/women/cap sleeve .png"), 
                                ("Puff Sleeves", "images/women/puff sleeves .png"), 
                                ("Bell Sleeve", "images/women/Bell sleeve.png"), 
                                ("Flutter Sleeve", "images/women/flutter sleeve .png"), 
                                ("Angel Sleeves", "images/women/angel sleeves .png")],
                    "TRADITIONAL WEAR": [("Chanderi Saree", "images/women/chanderi saree.png"), 
                                         ("Anarkali Kurta", "images/women/anarkali kurta.png"), 
                                         ("Flared Kurta", "images/women/flared kurta.png"), 
                                         ("Empire Waist Kurta", "images/women/empire waist kurta.png"), 
                                         ("Straight Cut Kurta", "images/women/straight cut kurta.png")]
                },
                "HOURGLASS": {
                    "Skirt": [("Pencil Skirt", "images/women/pencil skirt .png"), 
                              ("Mermaid Skirt", "images/women/mermaid skirt.png"),
                              ("Tulip Skirt", "images/women/tulip skirt.png"), 
                              ("Flip Skirt", "images/women/flip skirt .png"), 
                              ("Wrap Skirt", "images/women/wrap skirt .png")],
                    "Jumpsuits": [("Belted Jumpsuit", "images/women/belted jumpsuit .png"), 
                                  ("Wrap Jumpsuit", "images/women/wrap jumpsuit .png"), 
                                  ("Strapless Jumpsuit", "images/women/strapless jumpsuit .png"), 
                                  ("Wide Leg Jumpsuit", "images/women/wide leg jumpsuit .png"), 
                                  ("Utility Jumpsuit", "images/women/utility jumpsuit .png")],
                    "Pants": [("Skinny Jeans", "images/women/skinny jeans .png"), 
                              ("Bootcut Pants", "images/women/bootcut pants.png"), 
                              ("Palazzo Pants", "images/women/Palazzo pants .png"), 
                              ("Pegged Pants", "images/women/pegged pants.png"), 
                              ("Wide-leg Jeans", "images/women/wideleg jeans .png")],
                    "Necklines": [("Halter Neckline", "images/women/halter neckline .png"), 
                                  ("V Neckline", "images/women/v neckline.png"), 
                                  ("Sweetheart Neckline", "images/women/sweetheart neckline .png"), 
                                  ("Scoop Neckline", "images/women/scoop neckline .png"), 
                                  ("Off Shoulder Neckline", "images/women/off shoulder neckline .png")],
                    "Tops": [("Fitted Top", "images/women/fitted top.png"), 
                             ("Peplum Top", "images/women/peplum top .png"), 
                             ("Sweetheart Neckline Tops", "images/women/sweetheart neckline tops .png"), 
                             ("Wrap Top", "images/women/wrap top.png"), 
                             ("Hoodie", "images/women/hoodie .png")],
                    "Sleeves": [("Cap Sleeve", "images/women/cap sleeve .png"), 
                                ("Puff Sleeves", "images/women/puff sleeves .png"), 
                                ("Bell Sleeve", "images/women/Bell sleeve.png"), 
                                ("Flutter Sleeve", "images/women/flutter sleeve .png"), 
                                ("3/4 Sleeve", "images/women/3_4 th sleeve .png")],
                    "TRADITIONAL WEAR": [("Lehanga Choli", "images/women/lehanga choli .png"), 
                                         ("Anarkali Kurta", "images/women/anarkali kurta.png"), 
                                         ("A-line Kurta", "images/women/aline kurta.png"), 
                                         ("Salwar Kameez", "images/women/salwar kameez .png"), 
                                         ("Kanjivaram Saree", "images/women/kanjivaram saree.png")]
                },
                "INVERTED TRIANGLE": {
                    "Skirt": [("A-line Skirt", "images/women/a line skirt .png"), 
                              ("Pegged Skirt", "images/women/pegged skirt .png"),
                              ("Midi Skirt", "images/women/midi skirt .png"), 
                              ("Above Calf Skirt", "images/women/above calf skirt.png"), 
                              ("Wrap Skirt", "images/women/wrap skirt .png")],
                    "Jumpsuits": [("Belted Jumpsuit", "images/women/belted jumpsuit .png"), 
                                  ("Peplum Jumpsuit", "images/women/peplum jumpsuit .png"), 
                                  ("Off Shoulder Jumpsuit", "images/women/off shoulder jumpsuit .png"), 
                                  ("Wide Leg Jumpsuit", "images/women/wide leg jumpsuit .png"), 
                                  ("Flared Jumpsuit", "images/women/flared jumpsuit.png")],
                    "Pants": [("Flared Jeans", "images/women/flared jeans.png"), 
                              ("Bootcut Pants", "images/women/bootcut pants.png"), 
                              ("Palazzo Pants", "images/women/Palazzo pants .png"), 
                              ("Straight Jeans", "images/women/straight jeans.png"), 
                              ("Wide-leg Jeans", "images/women/wideleg jeans .png")],
                    "Necklines": [("Halter Neckline", "images/women/halter neckline .png"), 
                                  ("V Neckline", "images/women/v neckline.png"), 
                                  ("Bardot Neckline", "images/women/bardot neckline .png"), 
                                  ("Scoop Neckline", "images/women/scoop neckline .png"), 
                                  ("Off Shoulder Neckline", "images/women/off shoulder neckline .png")],
                    "Tops": [("Asymmetric Top", "images/women/asymmetric_top.png"), 
                             ("Peplum Top", "images/women/peplum_top.png"), 
                             ("Empire Top", "images/women/empire_top.png"), 
                             ("Wrap Top", "images/women/wrap_top.png"), 
                             ("Off Shoulder Top", "images/women/off_shoulder_top.png")],
                    "Sleeves": [("Cap Sleeve", "images/women/cap_sleeve.png"), 
                                ("Puff Sleeves", "images/women/puff_sleeves.png"), 
                                ("Bell Sleeve", "images/women/bell_sleeve.png"), 
                                ("Flutter Sleeve", "images/women/flutter_sleeve.png"), 
                                ("3/4th Sleeve", "images/women/3_4th_sleeve.png")],
                    "TRADITIONAL WEAR": [("Palazzo Kurta Set", "images/women/palazzo_kurta_set.png"), 
                                         ("Anarkali Kurta", "images/women/anarkali_kurta.png"), 
                                         ("A-line Kurta", "images/women/aline_kurta.png"), 
                                         ("Straight Cut Kurta", "images/women/straight_cut_kurta.png"), 
                                         ("Bandhani Saree", "images/women/bandhani_saree.png")]
                        }
                },

            "Male": {
                "TRIANGLE": {
                    "Collars": [("Button Down Collar", "images/button_down_collar.png"),
                                ("Banded Collar", "images/banded_collar.png"),
                                ("Mandarin Collar", "images/Mandarin_collar.png"),
                                ("Spread Collar", "images/spread_collar.png"),
                                ("Pinned Collar", "images/pinned_collar.png")],
                    "Shirts": [("Vertical Stripe Shirt", "images/vertical_stripe_shirt.png"),
                               ("Linen Shirt", "images/linen_shirt.png"),
                               ("T-Shirt", "images/tshirt.png"),
                               ("Polo T-Shirt", "images/polo_tshirt.png"),
                               ("Henley Shirt", "images/henley_shirt.png")],
                    "Pants": [("Chinos", "images/chinos.png"),
                              ("Straight Jeans", "images/straight_jeans.png"),
                              ("Slim Fit", "images/slim_fit.png"),
                              ("Cargo Pants", "images/cargo_pants.png"),
                              ("Shorts", "images/shorts.png")]
                },
                "OVAL": {
                    "Collars": [("Button Down Collar", "images/button_down_collar.png"),
                                ("Tab Collar", "images/tab_collar.png"),
                                ("Mandarin Collar", "images/Mandarin_collar.png"),
                                ("Spread Collar", "images/spread_collar.png"),
                                ("One Piece Collar", "images/one_piece_collar.png")],
                    "Shirts": [("Vertical Stripe Shirt", "images/vertical_stripe_shirt.png"),
                               ("Knit Shirt", "images/knit_shirt.png"),
                               ("Denim Shirt", "images/denim_shirt.png"),
                               ("Polo T-Shirt", "images/polo_tshirt.png"),
                               ("Flannel Shirt", "images/flannel_shirt.png")],
                    "Pants": [("Sweatpants", "images/sweatpants.png"),
                              ("Straight Jeans", "images/straight_jeans.png"),
                              ("Slim Fit", "images/slim_fit.png"),
                              ("Cargo Pants", "images/cargo_pants.png"),
                              ("Pleated Pants", "images/pleated_pants.png")]
                },
                "TRAPEZOID": {
                    "Collars": [("Button Down Collar", "images/button_down_collar.png"),
                                ("Cuban Collar Shirt", "images/cuban_collar_shirt.png"),
                                ("Hidden Button Down Collar", "images/hidden_button_down_collar.png"),
                                ("Spread Collar", "images/spread_collar.png"),
                                ("Tab Collar", "images/tab_collar.png")],
                    "Shirts": [("Tuxedo Shirt", "images/tuxedo_shirt.png"),
                               ("Linen Shirt", "images/linen_shirt.png"),
                               ("T-Shirt", "images/tshirt.png"),
                               ("Short Sleeve T-Shirt", "images/short_sleeve_tshirt.png"),
                               ("Flap Pocket Shirt", "images/flap_pocket_shirt.png")],
                    "Pants": [("Linen Trousers", "images/linen_trousers.png"),
                              ("Straight Jeans", "images/straight_jeans.png"),
                              ("Slim Fit", "images/slim_fit.png"),
                              ("Joggers", "images/joggers.png"),
                              ("Shorts", "images/shorts.png")]
                    
                    }
                }
            }




                

                  

    def load_rf_model(self):
        # Load the trained model from a pickle file
        with open('random_forest_model.pkl', 'rb') as file:
            model = pickle.load(file)
        return model

    def classify(self, gender, age, measurements):
        try:
            data = pd.DataFrame(columns=['Gender', 'Age', 'Shoulder', 'Waist', 'Hips', 'Bust', 'Chest'])
            data.loc[0] = [FEMALE_GENDER if gender == "Female" else MALE_GENDER, age] + measurements
            body_type = self.rf_model.predict(data)[0]
            return body_type
        except Exception as e:
            st.error(f"An error occurred during classification: {e}")
            return None

    def display_recommendations(self, gender, body_type):
        st.write(f"Recommendations for {body_type} body type:")
        recommendations = self.recommendation_images[gender][body_type]

        feedback = {}
        for category, images in recommendations.items():
            st.write(f"Category: {category}")
            for img_name, img_path in images:
                col1, col2 = st.columns(2)
                with col1:
                    st.image(img_path, use_column_width=True, caption=img_name)
                with col2:
                    feedback[img_path] = st.button("👍", key=f"{img_path}_like") or st.button("👎", key=f"{img_path}_dislike")

        return feedback

    def run(self):
        st.title("Recommendation of Cloth pattern using Body type")

        gender = st.radio("Select your gender:", ("Female", "Male"))
        age = st.number_input("Enter your age:", min_value=0)
        shoulder = st.number_input("Enter your shoulder measurement (in inches):", min_value=0)
        waist = st.number_input("Enter your waist measurement (in inches):", min_value=0)
        hips = st.number_input("Enter your hips measurement (in inches):", min_value=0)
        bust_chest_label = "bust" if gender == "Female" else "chest"
        bust_chest = st.number_input(f"Enter your {bust_chest_label} measurement (in inches):", min_value=0)

        if st.button("Get Recommendations"):
            measurements = [shoulder, waist, hips, bust_chest]
            body_type = self.classify(gender, age, measurements)
            if body_type:
                feedback = self.display_recommendations(gender, body_type)
                st.write("Thank you for your feedback!")

if __name__ == "__main__":
    app = BodyClassifierApp()
    app.run()
