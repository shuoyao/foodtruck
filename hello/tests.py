from django.test import TestCase
import unittest
from django.core.urlresolvers import reverse
from .models import Greeting

class DatabaseTest(TestCase):
    def test_create_unpublished(self):
        greeting = Greeting()
        old_objects_count = Greeting.objects.all().count()
        greeting.save()
        self.assertEqual(Greeting.objects.all().count(), 1 + old_objects_count)
      
class ViewTests(TestCase):
    def test_index_url(self):
        response = self.client.get(reverse('db'))
        self.assertEqual(200, response.status_code)
        self.assertIn("GettingStarted", response.content)
    def test_events_url(self):
        response = self.client.get(reverse('events'))   
        self.assertEqual(200, response.status_code)
    def test_vendors_url(self):
        response = self.client.get(reverse('vendors'))   
        self.assertEqual(200, response.status_code)
