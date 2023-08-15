from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import AuditLog
from alarm.models import AlarmConfig

def ViewAuditLog(request):
    """
    Function to list the Audit logs
    """

    # Retrieve Alarm object to show in navbar
    alarm = AlarmConfig.objects.first()

    auditLog = AuditLog.objects.all().order_by('-created')
    paginator = Paginator(auditLog, 10)                     # 20 Items per page
    page = request.GET.get('page')

    try:
        audits = paginator.page(page)
    except PageNotAnInteger:
        # Show 1st page if parameter is not an integer
        audits = paginator.page(1)
    except EmptyPage:
        # Show last page if it's out of range
        audits = paginator.page(paginator.num_pages)

    return render(request,
                  'audit/audit.html',
                  {
                      'auditlog': audits,
                      'alarm': alarm
                  })
