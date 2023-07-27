import json
from django.shortcuts import render
from django.http import JsonResponse
from mqtt.mqtt import client as mqtt_client
from django.views.decorators.csrf import csrf_exempt

from devices.models import ActiveDevices

@csrf_exempt
def publish_message(request):
    request_data = json.loads(request.body)
    rc, mid = mqtt_client.publish(request_data['topic'], request_data['msg'])
    return JsonResponse({'code': rc})
