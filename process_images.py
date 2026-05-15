import os
import requests
import cv2
import numpy as np
from urllib.parse import urlparse

# 1. Directory Setup
OUTPUT_DIR = "augmented_dataset"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Path to your text file containing the links
LINKS_FILE = "generated_links_4202.txt"

# 2. Brightness Adjustment Function
def adjust_and_save_brightness(image, base_name, percentage):
    # Convert percentage to scale factor
    alpha = percentage / 100.0
    
    # Adjust brightness using convertScaleAbs
    augmented_image = cv2.convertScaleAbs(image, alpha=alpha, beta=0)
    
    # Construct filename
    output_filename = f"{base_name}_br{percentage}.jpg"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    # Save image
    cv2.imwrite(output_path, augmented_image)

# 3. Image Downloading and Processing Function
def process_image_from_url(url):
    try:
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        base_name = os.path.splitext(filename)[0]
        
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            
            if image is not None:
                # Targeted brightness levels: 100%, 120%, 150%
                brightness_levels = [100, 120, 150]
                for level in brightness_levels:
                    adjust_and_save_brightness(image, base_name, level)
                return True
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
    return False

# 4. Main Execution logic with range selection
if __name__ == "__main__":
    if not os.path.exists(LINKS_FILE):
        print(f"Error: {LINKS_FILE} not found!")
    else:
        # Load all links into a list
        with open(LINKS_FILE, 'r') as f:
            all_links = [line.strip() for line in f.readlines() if line.strip()]

        total_available = len(all_links)
        print(f"Total links found: {total_available}")

        # Ask user for preference
        choice = input("Do you want to process all images? (yes/no): ").strip().lower()

        links_to_process = []
        if choice == 'yes':
            links_to_process = all_links
            print(f"Processing all {total_available} images...")
        else:
            # Handle range input
            try:
                start_index = int(input(f"Enter the starting image number (1 to {total_available}): "))
                end_index = int(input(f"Enter the ending image number ({start_index} to {total_available}): "))
                
                # Slicing the list (adjusting for 0-based indexing)
                links_to_process = all_links[start_index-1 : end_index]
                print(f"Processing images from index {start_index} to {end_index}...")
            except ValueError:
                print("Invalid input! Please enter numbers only.")
                exit()

        # Processing loop
        if links_to_process:
            success_count = 0
            count_to_process = len(links_to_process)
            
            for i, url in enumerate(links_to_process, 1):
                if process_image_from_url(url):
                    success_count += 1
                
                # Progress update every 10 images
                if i % 10 == 0 or i == count_to_process:
                    print(f"Progress: {i}/{count_to_process} images completed...")

            print("\nWork Completed!")
            print(f"Original images processed: {success_count}")
            print(f"Total augmented files created: {success_count * 3}")
        else:
            print("No images selected for processing.")