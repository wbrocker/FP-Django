from django.test import TestCase
from django.urls import reverse

from .models import ImageDetection

# Models Testcase
class ImageModelTest(TestCase):

    def test_image_det_creation(self):
        # Testing the creation of iamges

        image_det = ImageDetection.objects.create(
            image='test.jpg',
            cameraId='10',
            analyzed=False,
            detection_data='{"key":"value"}'
        )

        self.assertIsInstance(image_det, ImageDetection)
        self.assertEqual(image_det.cameraId, '10')
        self.assertFalse(image_det.analyzed)
        self.assertEqual(image_det.detection_data, '{"key":"value"}')



    def test_default_values(self):
        # Testing the default values
        image_det = ImageDetection.objects.create(image='test.jpg')

        self.assertFalse(image_det.analyzed)
        self.assertEqual(image_det.detection_data, '{}')