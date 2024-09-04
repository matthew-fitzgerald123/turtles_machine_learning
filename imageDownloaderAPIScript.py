import os
import requests
import shutil
import time

# Function to download images using the Wikimedia Commons API
def download_images(query, num_images, save_folder):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Wikimedia Commons API URL
    api_url = "https://commons.wikimedia.org/w/api.php"

    # Parameters for the API request
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": query,
        "gsrlimit": num_images,
        "gsrnamespace": 6,  # Restrict search to the File namespace (which contains images)
        "prop": "imageinfo",
        "iiprop": "url",
    }

    headers = {
        "User-Agent": "MyImageDownloader/1.0 (Contact: youremail@example.com)"
    }

    try:
        print(f"Sending request to Wikimedia Commons API for query: {query}")
        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        pages = data.get("query", {}).get("pages", {})
        downloaded = 0

        for page_id, page_data in pages.items():
            imageinfo = page_data.get("imageinfo", [])
            if imageinfo:
                img_url = imageinfo[0].get("url")
                if img_url:
                    for attempt in range(3):  # Retry up to 3 times
                        try:
                            print(f"Downloading image: {img_url}")
                            img_response = requests.get(img_url, stream=True, headers=headers)
                            img_response.raise_for_status()

                            img_filename = os.path.join(save_folder, f"{query}{downloaded + 1}.jpg")
                            with open(img_filename, 'wb') as img_file:
                                shutil.copyfileobj(img_response.raw, img_file)

                            downloaded += 1
                            print(f"Downloaded {downloaded}/{num_images}: {img_filename}")
                            break  # Exit retry loop if successful
                        except Exception as e:
                            print(f"Attempt {attempt + 1} failed: {e}")
                            time.sleep(2)  # Wait before retrying

                    if downloaded >= num_images:
                        break

            time.sleep(1)  # Pause between requests to avoid being rate-limited

        if downloaded == 0:
            print("No images were downloaded. Check the API response for potential issues.")

    except Exception as e:
        print(f"Error retrieving data from Wikimedia Commons API: {e}")

# Download:
download_images("mountains", 100, "non_turtle_images")
download_images("caves", 100, "non_turtle_images")
download_images("hills", 100, "non_turtle_images")
download_images("roads", 100, "non_turtle_images")
download_images("valley", 100, "non_turtle_images")
download_images("turtle", 100, "turtle_images")
download_images("sea turtle", 100, "turtle_images")
download_images("green turtle", 100, "turtle_images")
download_images("big turtle", 100, "turtle_images")
download_images("small turtle", 100, "turtle_images")