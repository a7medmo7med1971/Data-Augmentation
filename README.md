Image Augmentation Tool (Brightness Adjustment)
This Python tool is designed to download images from a provided list of URLs and generate multiple versions of each image with different brightness levels. This is specifically useful for Deep Learning and Object Detection tasks (like YOLO) to perform Data Augmentation.

Features
URL-based processing: Reads image links directly from a .txt file.

Brightness Levels: Automatically generates 3 versions of each image:

100% (Original)

120% (Slightly Brighter)

150% (Very Bright)

Flexible Execution: Allows processing the entire dataset or a specific range of images.

Automatic Organization: Saves all generated images in a dedicated folder with clear naming conventions.

Project Structure
Plaintext
Augmentation_project/
├── generated_links_4202.txt  # Your file containing 4202 URLs
├── main.py                   # The Python script
├── README.md                 # Project documentation
└── augmented_dataset/        # Created automatically (Contains 12,606 images)
Naming Convention
For every image processed (e.g., image_01.jpg), the tool creates:

image_01_br100.jpg

image_01_br120.jpg

image_01_br150.jpg

Prerequisites
Make sure you have Python installed, then install the required libraries:

Bash
pip install opencv-python requests numpy
How to Use
Place your links file generated_links_4202.txt in the same directory as the script.

Run the script:

Bash
python main.py
The script will ask: Do you want to process all images? (yes/no):

Type yes to process all 4202 images.

Type no to specify a custom range (e.g., from image 1 to 100).

Technical Details
Library: OpenCV (cv2) for image manipulation.

Method: convertScaleAbs for efficient pixel-wise scaling.

Timeout: 20-second timeout per download to prevent hanging on broken links.
