# Image Augmentation Tool (Brightness Adjustment)

This Python tool downloads images from a list of URLs and generates multiple brightness variations for each image. It is designed for Deep Learning and Object Detection workflows such as YOLO Data Augmentation.

## Features

- Reads image URLs directly from a `.txt` file
- Generates 3 brightness versions for every image:
  - 100% (Original)
  - 120% (Slightly Brighter)
  - 150% (Very Bright)
- Supports processing:
  - The full dataset
  - A custom image range
- Automatically creates and organizes output files
- Uses clear and consistent file naming
- Handles broken links with request timeout protection

## Project Structure

```plaintext
Augmentation_project/
├── generated_links_4202.txt   # File containing image URLs
├── process_images.py                    # Main Python script
├── README.md                  # Documentation
└── augmented_dataset/         # Auto-generated output folder
```

## Output Naming Convention

For every processed image, the tool creates:

```plaintext
image_01_br100.jpg
image_01_br120.jpg
image_01_br150.jpg
```

## Requirements

Install the required Python libraries before running the project:

```bash
pip install opencv-python requests numpy
```

## How to Use

1. Place the file `generated_links_4202.txt` in the same directory as `main.py`

2. Run the script:

```bash
python process_images.py
```

3. Choose processing mode when prompted:

```plaintext
Do you want to process all images? (yes/no)
```

- Type `yes` to process the entire dataset
- Type `no` to select a custom image range

Example:

```plaintext
Start image: 1
End image: 100
```

## Technical Details

- Library Used: OpenCV (`cv2`)
- Brightness Method: `convertScaleAbs`
- Download Timeout: 20 seconds per image
- Designed for large-scale dataset augmentation workflows

## Use Cases

- YOLO Dataset Augmentation
- Object Detection Training
- Computer Vision Preprocessing
- Improving Model Robustness Under Different Lighting Conditions
