from django.test import TestCase, Client
import json
from django.urls import reverse

from imgcapture.models import ImageDetection

class DashboardViewTestCase(TestCase):
    def setUp(self):
        # Setup test instances of imageDetection
        ImageDetection.objects.create(
            image='test.jpg',
            detection_data='{"key1": "value1"}'
        )
        ImageDetection.objects.create(
            image='test1.jpg',
            detection_data='{"key2": "value2"}'
        )

    def test_index_view(self):
        # test the 'index' view
        url = reverse('dashboard:dash')
        response = self.client.get(url)

        # Confirm the view returns 200
        self.assertEqual(response.status_code, 200)

        # Confirm the correct template is used.
        self.assertTemplateUsed(response, 'dash/home.html')


    def test_imageList_view(self):
        # Testing the imageList view
        url = reverse('dashboard:image-list')
        response = self.client.get(url)

        # Confirm the view returns 200
        self.assertEqual(response.status_code, 200)

        # Confirm the correct view is used.
        self.assertTemplateUsed(response, 'dash/images.html')

        # Confirm that the 'images' variable contains data
        images = response.context['images']
        self.assertEqual(len(images), 2)     # Assuming 2 images
        for image in images:
            self.assertIsInstance(image.detection_data, dict)

    def test_individualImage_view(self):
        # Test the Individual image view
        image = ImageDetection.objects.first()          # Assuming at least one image
        url = reverse('dashboard:image', args=[image.pk])
        response = self.client.get(url)

        # Confirm the view returns 200
        self.assertEqual(response.status_code, 200)

        # Confirm that the correct template is used.
        self.assertTemplateUsed(response, 'dash/image.html')

        # Confirm the variable 'image' contains data
        image_data = response.context['image']
        self.assertIsInstance(image_data.detection_data, dict)