from django.test import TestCase
from .models import AuditLog
from .utils import Audit

class AuditLogTestCase(TestCase):
    def test_create_audit_entry(self):
        AuditLog.objects.create(type='ALA', description='Test Alarm', source='Test')
        self.assertEqual(AuditLog.objects.count(), 1)

    def test_audit_function(self):
        Audit(event_type='CFG', description='Test Config', source='Test')
        self.assertEqual(AuditLog.objects.count(), 1)

    def test_audit_fields(self):
        entry = AuditLog.objects.create(type='OTH', description='Test Other', source='Test')
        self.assertEqual(entry.type, 'OTH')
        self.assertEqual(entry.description, 'Test Other')
        self.assertEqual(entry.source, 'Test')