# -*- encoding: utf-8 -*-

import os
from datetime import datetime
import hashlib
import time 

from django.db import models

try:
    import json
except:
    import simplejson as json


class ErrorStats(models.Model):
    key = models.CharField(max_length=128)
    times = models.IntegerField(default=0)

class ErrorSummary(models.Model):

    key = models.CharField(max_length=128)
    error = models.TextField(default='')
    times = models.IntegerField(default=0)
    last_time = models.DateTimeField(default=datetime.now)

    def timestamp(self):
        return time.mktime(self.last_time.timetuple())

    def to_dict(self):
        return {
            'date': self.timestamp() , 
            'error': json.loads(self.error),
            'times': self.times
        }

class Error(models.Model):
    error = models.TextField(default='')
    when = models.DateTimeField(default=datetime.now)

    @staticmethod
    def track(log):
        e = json.dumps(log)
        Error(error=e).save();
        _hash = hashlib.md5(log['error']).hexdigest()
        # ok, this is not safe, but lost one exception is not so important
        u, c = ErrorSummary.objects.get_or_create(key=_hash)
        if c:
            u.error = e
        u.times+=1
        u.last_time = datetime.now()
        u.save();

        Error._stats_incr(Error._month_key())
        Error._stats_incr(Error._today_key())

    @staticmethod
    def _month_key(d=None):
        d = d or datetime.now()
        return "%d-%d" % (d.month, d.year)
    
    @staticmethod
    def _today_key(d=None):
        d = d or datetime.now()
        return "%d-%d-%d" % (d.day, d.month, d.year)

    @staticmethod
    def _stats_incr(k):
        d = datetime.now()
        u, c = ErrorStats.objects.get_or_create(key=k)
        u.times+=1
        u.save();

    @staticmethod
    def stats_for(k):
        try:
            return ErrorStats.objects.get(key=k).times
        except ErrorStats.DoesNotExist:
            return 0

    @staticmethod
    def today():
        return Error.stats_for(Error._today_key())

    @staticmethod
    def month():
        return Error.stats_for(Error._month_key())

    @staticmethod
    def count(since=None):
        o = Error.objects
        if since:
            o = o.filter(when__gt=since)
        return o.count()

    @staticmethod
    def latest(items=10, since=None):
        q = ErrorSummary.objects
        if since:
            q = q.filter(last_time__gt=since)
        return q.order_by('-last_time')[:items]


