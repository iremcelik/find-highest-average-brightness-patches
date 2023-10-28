# Image Processor

This Python script (`image_processor.py`) is designed to process images, find highest average brightness patches within the images, draw squares around the top patches, calculate the area of a quadrilateral formed by patch centers, and save the processed images. Additionally, there are associated test cases (`test_cases.py`) to ensure the correctness of the image processing functions.

## Getting Started

Follow these instructions to use the image processing script and run the provided test cases.

1. Place the path to the image you want in the relevant field in the image_processor.py file and run the code.
2. Make sure you get output from the image_processor.py file.
3. The outputs obtained from the image_processor.py file are given as input to the test_cases.py file.
4. Make sure that the path to the outputs obtained from the image_processor.py file in the test_cases.py file is correct.

### Prerequisites

Make sure you have the following software and libraries installed:

- Python (>= 3.6)
- OpenCV (cv2)
- NumPy

You can install the required libraries using pip:

```bash
pip install opencv-python numpy

