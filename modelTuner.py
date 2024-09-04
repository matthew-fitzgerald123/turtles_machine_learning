from tensorflow.keras.preprocessing import image
import numpy as np
import tensorflow as tf
from AppKit import NSOpenPanel
import os

# Load the model
model = tf.keras.models.load_model('turtle_model.keras')  # Ensure the best model is loaded

def fine_tune_model(model):
    """
    Unfreezes the last few layers of the model for fine-tuning.
    """
    # Unfreeze some layers of the base model for fine-tuning
    for layer in model.layers[-4:]:
        layer.trainable = True

    # Compile the model again with a smaller learning rate
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def predict_image(img_path):
    """
    Predicts whether a sea turtle is in the image.
    """
    if not os.path.exists(img_path):
        print("File not found. Please check the path and try again.")
        return

    # Resize image to 224x224 to match model input size
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Rescale to [0, 1]

    # Predict the class
    prediction = model.predict(img_array)
    score = prediction[0]  # Scores for each class (0: non-turtle, 1: turtle)

    # Class names for prediction output
    class_names = ['No sea turtle detected.', 'Sea turtle detected!']

    # Output prediction scores and class
    print(f"Prediction scores: {score}")
    predicted_class = np.argmax(score)  # Choose class with the highest probability
    print(class_names[predicted_class])

# Function to open native macOS file dialog
def open_file_dialog():
    """
    Opens a macOS file dialog to select an image file.
    """
    panel = NSOpenPanel.openPanel()
    panel.setCanChooseFiles_(True)
    panel.setCanChooseDirectories_(False)
    panel.setAllowsMultipleSelection_(False)
    panel.setAllowedFileTypes_(["jpg", "jpeg", "png", "bmp", "tiff"])
    
    if panel.runModal():
        return str(panel.URLs()[0].path())
    return None

# Main program to allow file selection through a native macOS dialog
if __name__ == "__main__":
    img_path = open_file_dialog()
    if img_path:
        # Fine-tune the model if necessary
        model = fine_tune_model(model)
        predict_image(img_path)
    else:
        print("No file selected. Please try again.")
