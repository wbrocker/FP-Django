import sys
import time

import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision

def detect(filename, model: str):
    """
    Detect the objects in the image and return results.

    Example used from TFLite:

    Arguments
        model: The name of the TFLite object detection model used.
        width: The width of the frame
        height: The height of the frame
    """

    # Open the image from filename
    inputImage = cv2.imread(filename)

    # Determine Height and Width of image
    height, width, channels = inputImage.shape

    # Init the object detection model.
    base_options = core.BaseOptions(
        file_name = model, use_coral = False, num_threads = 2)
    detection_options = processor.DetectionOptions(
        max_results = 3, score_threshold = 0.3)
    options = vision.ObjectDetectorOptions(
        base_options = base_options, detection_options = detection_options)
    detector = vision.ObjectDetector.create_from_options(options)

    image = cv2.flip(inputImage, 1)

    # Convert the image from BGR to RGB as required from TFLite model.
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create a TensorImage object from the RGB image.
    input_tensor = vision.TensorImage.create_from_array(rgb_image)

    # Run object detection estimation using the model.
    detection_result = detector.detect(input_tensor)

    print(detection_result)
    
    return detection_result