import os
from PIL import Image

def check_images(directory):
    """
    Checks all images in the given directory to identify any that cause errors.

    Args:
    - directory (str): The path to the directory containing the images.
    """
    valid_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}
    problematic_images = []

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Check for valid file extension
            if not any(file.lower().endswith(ext) for ext in valid_extensions):
                continue

            # Check if the file is a valid image
            try:
                with Image.open(file_path) as img:
                    img.verify()  # Verify that the image is not corrupted
                    img.close()   # Close the image file

                # Reload image to ensure it can be properly opened
                with Image.open(file_path) as img:
                    img.load()  # Ensure image can be loaded
                    img.close()
                    
                # Try converting the image to another format (e.g., to ensure it's not corrupted)
                with Image.open(file_path) as img:
                    img.convert('RGB')
            
            except (IOError, SyntaxError, ValueError, Image.DecompressionBombError, Image.UnidentifiedImageError) as e:
                print(f"Problematic image: {file_path} - Error: {e}")
                problematic_images.append(file_path)

    return problematic_images

# Check both datasets
non_turtle_issues = check_images('non_turtle_images')
turtle_issues = check_images('turtle_images')

# Report problematic images
if non_turtle_issues:
    print(f"Problematic images in non_turtle_images: {len(non_turtle_issues)}")
    for img in non_turtle_issues:
        print(img)

if turtle_issues:
    print(f"Problematic images in turtle_images: {len(turtle_issues)}")
    for img in turtle_issues:
        print(img)

print("Image checking completed.")