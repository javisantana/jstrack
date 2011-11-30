# -*- encoding: utf-8 -*-

import logging
import time
try:
    import json
except:
    import simplejson as json

from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response

from django.conf import settings
from models import Error

def error_js(request):
    s = request.GET.get('s', '')
    if not s:
        raise Http404

    if s[-1] != '/':
        s += '/'

    return render_to_response('error_track.js', {
        'tracking_server': s
    }, mimetype='application/javascript')

def error_track(request):
    err = request.GET.get('e', '')
    ua = request.META['HTTP_USER_AGENT']
    host = request.get_host()
    if err:
        Error.track({
            'error': err,
            'ua': ua,
            'host': host
        })
    return HttpResponse('', mimetype='application/json')

@csrf_exempt
def error(request):
    if request.method == "POST":
        Error.track(request.raw_post_data)
        return HttpResponse("logged, thanks!")
    else:
        data = {
            'count_today': Error.today(),
            'count_month': Error.month(),
            'count': Error.count(),
            'latest': [x.to_dict() for x in Error.latest()]
        }
        return HttpResponse(json.dumps(data), mimetype='application/json')

def errors(request):
    text = '\n'.join([x.when.isoformat() + " =>" + x.error for x in Error.latest()])
    return HttpResponse(text, mimetype='text/plain')



