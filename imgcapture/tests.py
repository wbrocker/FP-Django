from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
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


class DeleteAllViewTestCase(TestCase):
    def setUp(self):
        # Create a test client
        self.client = Client() 

    def test_delete_all_with_dnd_true(self):
        # Create ImageDetection object with DND=True
        ImageDetection.objects.create(image=SimpleUploadedFile("test_image1.jpg", b"file_content"), dnd=True)

        # Perform GET request to the Delete_all view
        url = reverse('imgcapture:del_all')
        response = self.client.get(url)
        print(response)

        # Confirm that the response is successful
        self.assertEqual(response.status_code, 302)

        # Confirm that no objects are deleted since dnd=True
        self.assertEqual(ImageDetection.objects.count(), 1)

    def test_delete_all_with_dnd_false(self):
        # Create ImageDetection objects with dnd=False
        ImageDetection.objects.create(image=SimpleUploadedFile("test_image2.jpg", b"file_content"), dnd=False)
        ImageDetection.objects.create(image=SimpleUploadedFile("test_image3.jpg", b"file_content"), dnd=False)

        # Perform GET request to delete_all view
        url = reverse('imgcapture:del_all')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)