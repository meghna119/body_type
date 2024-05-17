import pickletools

with open('random_forest_model.pkl', 'rb') as file:
    pickletools.dis(file)
