from .models import AuditLog

def Audit(event_type_param, description, source=''):
    """
    Add event to the AuditLog

    Parameters:
        event_type (str): The type of the event (e.g., 'ALA' for Alarm, 'CFG' for Configuration).
        description (str): A brief description of the event.
        source (str, optional): The source of the event. Default is an empty string.
    """
    AuditLog.objects.create(
        type=event_type_param,
        description=description,
        source=source
    )