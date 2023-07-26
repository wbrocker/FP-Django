from django.test import TestCase

from .models import Locations

class DevicesModelTest(TestCase):

    # Test to ensure Blog String Entry equalt the title
    def test_string_location(self):
        loc = Locations(name="Test", description="This is a test")
        self.assertEqual(str(loc), loc.name)
