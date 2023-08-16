from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import AuditLog
from .utils import Audit
from .views import ViewAuditLog

class AuditLogTestCase(TestCase):
    def test_create_audit_entry(self):
        AuditLog.objects.create(type='ALA', description='Test Alarm', source='Test')
        self.assertEqual(AuditLog.objects.count(), 1)

    def test_audit_function(self):
        Audit('CFG', 'Test Config', 'Test')
        self.assertEqual(AuditLog.objects.count(), 1)

    def test_audit_fields(self):
        entry = AuditLog.objects.create(type='OTH', description='Test Other', source='Test')
        self.assertEqual(entry.type, 'OTH')
        self.assertEqual(entry.description, 'Test Other')
        self.assertEqual(entry.source, 'Test')

class ViewAuditLogTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # Create sample AuditLog entries for testing
        AuditLog.objects.create(type="ALA", description="Test alarm", source="Source1")
        AuditLog.objects.create(type="CFG", description="Test config", source="Source2")

    def test_view_audit_log(self):
        url = reverse('audit:auditlog')
        request = self.factory.get(url)
        response = ViewAuditLog(request)

        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'audit/audit.html')
        self.assertContains(response, 'Test alarm')
        self.assertContains(response, 'Test config')
