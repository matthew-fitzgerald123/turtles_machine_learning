from PIL import Image, ImageFile, UnidentifiedImageError
from PIL.Image import DecompressionBombWarning, DecompressionBombError  # Correct imports for warnings and errors
import os
import warnings

# Set the maximum image pixels to avoid DecompressionBombError for large images
Image.MAX_IMAGE_PIXELS = 10**7  # Example limit, adjust as needed (10,000,000 pixels)

# Increase the safety margin to prevent decompression bombs
ImageFile.LOAD_TRUNCATED_IMAGES = True

def verify_and_cleanup_images(directory):
    """
    This function iterates through all files in the specified directory,
    checks if they are in JPG or JPEG format, verifies their integrity,
    and removes any corrupt or potentially harmful files.
    """
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Check if the file is a JPEG or JPG
        if not (filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg')):
            print(f"Removing non-JPG/JPEG file: {file_path}")
            os.remove(file_path)
            continue

        # Open and verify the image
        try:
            # First, check if it is a valid image file
            with Image.open(file_path) as img:
                img.verify()  # Verify that it is indeed an image
            
            # If the image is valid, open it again to fully load it
            with Image.open(file_path) as img:
                img.load()  # Load the image to catch any issues related to I/O or file corruption

        except (UnidentifiedImageError, IOError, AttributeError, ValueError) as e:
            print(f"Removing corrupt or unreadable file: {file_path} - Error: {e}")
            os.remove(file_path)
        except (DecompressionBombWarning, DecompressionBombError) as e:
            print(f"Removing file due to decompression bomb warning/error: {file_path} - Warning/Error: {e}")
            os.remove(file_path)

# Suppress DecompressionBombWarning for cleaner output
warnings.simplefilter('error', DecompressionBombWarning)

# Directories to verify
directories_to_check = ['non_turtle_images', 'turtle_images']

# Iterate over directories and clean up images
for directory in directories_to_check:
    print(f"Checking directory: {directory}")
    verify_and_cleanup_images(directory)
    print(f"Finished checking directory: {directory}\n")