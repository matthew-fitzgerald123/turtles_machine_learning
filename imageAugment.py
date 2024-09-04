import Augmentor
import os
from PIL import Image

# Function to check and correct crop coordinates
def safe_crop(image, left, upper, right, lower):
    """
    Safely crops an image, ensuring that the coordinates are valid.
    """
    width, height = image.size
    # Ensure the crop coordinates are within the image boundaries
    left = max(0, min(left, width))
    upper = max(0, min(upper, height))
    right = max(left, min(right, width))
    lower = max(upper, min(lower, height))

    if right <= left or lower <= upper:
        # If the corrected coordinates are invalid, return the original image
        return image
    return image.crop((left, upper, right, lower))

# Function to augment images
def augment_images(input_folder, output_folder, num_samples=1000):
    """
    Augments images in the input_folder and saves them to the output_folder.
    
    Parameters:
    - input_folder: Directory containing the original images.
    - output_folder: Directory to save augmented images.
    - num_samples: Number of augmented images to generate.
    """
    # Create a pipeline for augmentation
    p = Augmentor.Pipeline(source_directory=input_folder, output_directory=output_folder)

    # Augmentations with safer parameters
    p.rotate(probability=0.7, max_left_rotation=15, max_right_rotation=15)  # Reduced rotation angle
    p.zoom_random(probability=0.5, percentage_area=0.9)  # Reduced zoom percentage
    p.shear(probability=0.5, max_shear_left=5, max_shear_right=5)  # Reduced shear angle
    p.flip_left_right(probability=0.5)
    p.flip_top_bottom(probability=0.2)
    p.random_distortion(probability=0.5, grid_width=4, grid_height=4, magnitude=4)  # Reduced magnitude
    p.random_contrast(probability=0.5, min_factor=0.9, max_factor=1.1)
    p.random_brightness(probability=0.5, min_factor=0.9, max_factor=1.1)

    # Override the perform_operation function to use safe_crop
    for operation in p.operations:
        original_perform_operation = operation.perform_operation
        
        def perform_operation(images):
            augmented_images = []
            for image in images:
                try:
                    # Perform the original operation
                    augmented_image = original_perform_operation([image])[0]
                    
                    # If the operation was crop, ensure safe crop
                    if operation.method == "crop":
                        augmented_image = safe_crop(augmented_image, *operation.magnitudes)
                    
                    augmented_images.append(augmented_image)
                except Exception as e:
                    print(f"Error processing image: {e}")
                    augmented_images.append(image)  # Keep the original if there is an error
            return augmented_images
        
        operation.perform_operation = perform_operation

    # Generate the samples
    p.sample(num_samples)

# Directories for original images and augmented images
non_turtle_images_dir = "non_turtle_images"
turtle_images_dir = "turtle_images"
augmented_non_turtle_images_dir = "augmented_non_turtle_images"
augmented_turtle_images_dir = "augmented_turtle_images"

# Create directories for augmented images if they don't exist
os.makedirs(augmented_non_turtle_images_dir, exist_ok=True)
os.makedirs(augmented_turtle_images_dir, exist_ok=True)

# Augment images in both folders
print(f"Augmenting images in {non_turtle_images_dir}...")
augment_images(non_turtle_images_dir, augmented_non_turtle_images_dir)

print(f"Augmenting images in {turtle_images_dir}...")
augment_images(turtle_images_dir, augmented_turtle_images_dir)

print("Image augmentation completed!")