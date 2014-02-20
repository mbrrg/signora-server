from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.conf import settings
from django.core.urlresolvers import reverse
from ipware.ip import get_ip
from datetime import datetime
import json
import redis
import logging
from ws4redis import settings as redis_settings
from signora import queries
from signora.models import Device, Content


def index(request, device_identifier):
    logger = logging.getLogger('devices.index')

    if request.method != 'PUT':
        return HttpResponseBadRequest()

    try:
        device = Device.objects.get(identifier=device_identifier)
    except Device.DoesNotExist:
        device = Device(identifier=device_identifier)

    device.last_seen = datetime.now()

    try:
        raw = request.read().decode('utf-8')
        data = json.loads(raw)

        if 'os' in data:
            device.os = data['os']

        if "version" in data:
            device.app_version = data['version']

        ip = get_ip(request)

        device.ip_address = ip if ip is not None else ''

    except ValueError:
        pass

    device.save()

    content = queries.get_current_device_content(device)

    if content:
        if content.type == Content.STATIC_URL:
            result = {'url': content.static_url}
        elif content.type == Content.SLEEP:
            result = {'action': 'sleep'}
    else:
        url = request.build_absolute_uri("{0}signora/connected.html".format(settings.STATIC_URL))
        result = {'url': url}

    return HttpResponse(json.dumps(result), content_type='application/json')
