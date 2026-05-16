"""
Image Augmentation Tool for Brightness Adjustment.

This script reads image URLs from a text file, downloads them,
and generates multiple variations with different brightness levels
to enrich training datasets for computer vision models.
"""

import os
import sys
from urllib.parse import urlparse
import cv2
import numpy as np
import requests

# 1. Directory Setup
OUTPUT_DIR = "augmented_dataset"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Path to your text file containing the links
LINKS_FILE = "generated_links_4202.txt"


def adjust_and_save_brightness(image, base_name, percentage):
    """
    Adjusts the brightness of an image and saves it to the output directory.

    Args:
        image (numpy.ndarray): The input image array from OpenCV.
        base_name (str): The base filename without extension.
        percentage (int): The target brightness percentage (e.g., 100, 120).
    """
    # Convert percentage to scale factor
    alpha = percentage / 100.0

    # Adjust brightness using convertScaleAbs
    augmented_image = cv2.convertScaleAbs(image, alpha=alpha, beta=0)

    # Construct filename
    output_filename = f"{base_name}_br{percentage}.jpg"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    # Save image
    cv2.imwrite(output_path, augmented_image)


def process_image_from_url(image_url):
    """
    Downloads an image from a URL, decodes it, and applies brightness adjustment.

    Args:
        image_url (str): The direct web URL of the image.

    Returns:
        bool: True if processed successfully, False otherwise.
    """
    try:
        parsed_url = urlparse(image_url)
        filename = os.path.basename(parsed_url.path)
        base_name = os.path.splitext(filename)[0]

        response = requests.get(image_url, timeout=20)
        if response.status_code == 200:
            image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            if image is not None:
                # Targeted brightness levels: 100%, 120%, 150%
                brightness_levels = [100, 120, 150]
                for level in brightness_levels:
                    adjust_and_save_brightness(image, base_name, level)
                return True
    except requests.RequestException as req_err:
        print(f"Network error processing URL {image_url}: {req_err}")
    return False


# 4. Main Execution logic with range selection
if __name__ == "__main__":
    if not os.path.exists(LINKS_FILE):
        print(f"Error: {LINKS_FILE} not found!")
    else:
        # Load all links into a list specifying utf-8 encoding
        with open(LINKS_FILE, 'r', encoding='utf-8') as f:
            all_links = [line.strip() for line in f.readlines() if line.strip()]

        TOTAL_AVAILABLE = len(all_links)
        print(f"Total links found: {TOTAL_AVAILABLE}")

        # Ask user for preference
        choice = input("Do you want to process all images? (yes/no): ").strip().lower()

        links_to_process = []
        if choice == 'yes':
            links_to_process = all_links
            print(f"Processing all {TOTAL_AVAILABLE} images...")
        else:
            # Handle range input
            try:
                start_str = f"Enter the starting image number (1 to {TOTAL_AVAILABLE}): "
                start_index = int(input(start_str))
                end_str = f"Enter the ending image number ({start_index} to {TOTAL_AVAILABLE}): "
                end_index = int(input(end_str))

                # Slicing the list (adjusting for 0-based indexing)
                links_to_process = all_links[start_index - 1: end_index]
                print(f"Processing images from index {start_index} to {end_index}...")
            except ValueError:
                print("Invalid input! Please enter numbers only.")
                sys.exit()

        # Processing loop
        if links_to_process:
            SUCCESS_COUNT = 0
            COUNT_TO_PROCESS = len(links_to_process)

            for i, url in enumerate(links_to_process, 1):
                if process_image_from_url(url):
                    SUCCESS_COUNT += 1

                # Progress update every 10 images
                if i % 10 == 0 or i == COUNT_TO_PROCESS:
                    print(f"Progress: {i}/{COUNT_TO_PROCESS} images completed...")

            print("\nWork Completed!")
            print(f"Original images processed: {SUCCESS_COUNT}")
            print(f"Total augmented files created: {SUCCESS_COUNT * 3}")
        else:
            print("No images selected for processing.")