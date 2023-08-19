import sys
import time
import os
import json 

import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision

from audit.utils import AuditLog

from .models import ImageDetection

# Custom serialization function for the Detection object
def serialize_detection(detection, height):
    return {
        'bounding_box': {
            'origin_x': detection.bounding_box.origin_x,
            'origin_y': height - detection.bounding_box.origin_y - detection.bounding_box.height,
            'width': detection.bounding_box.width,
            'height': detection.bounding_box.height
        },
        'categories': [
            {
                'index': category.index,
                'score': category.score,
                'display_name': category.display_name,
                'category_name': category.category_name
            }
            for category in detection.categories
        ]
    }


def detect(pk, model: str):
    """
    Detect the objects in the image and return results.
    
    Note:
    Example code used from TFLite Object Recognition examples.
    The model that is used here is also the default model for 
    object detection in TensorFlow Lite. This was to reduce the 
    time to train a new model.

    Arguments
        model: The name of the TFLite object detection model used.
        width: The width of the frame
        height: The height of the frame
    """

    image_detection = ImageDetection.objects.get(pk=pk)

    filename = image_detection.image.url 
    type(filename)
    filename = "." + filename
    # print("Filename: " + filename)

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

    image = cv2.flip(inputImage, 0)

    # Convert the image from BGR to RGB as required from TFLite model.
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create a TensorImage object from the RGB image.
    input_tensor = vision.TensorImage.create_from_array(rgb_image)

    # Run object detection estimation using the model.
    detection_result = detector.detect(input_tensor)

    detections = detection_result.detections
    print("======Detections: ")
    print(detections)

    # Serialize the TensorFlow object into JSON
    serialized_data = json.dumps(
        {
            'detections': [serialize_detection(detection, height) for detection in detections]
        }
    )

    image_detection.analyzed = True
    image_detection.detection_data = serialized_data
    image_detection.save()

    AuditLog("TEN", "Image Analyzed - " + str(image_detection.pk), "TensorFlow")

    # Call the Alarm function to determine if alarm must be raised
    from alarm.utils import checkAlarm
    checkAlarm(image_detection.id)
    
    return detection_result