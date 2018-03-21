# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.


class dns_record(models.Model):
    zone = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    type = models.CharField(max_length=5)
    data = models.CharField(max_length=255, blank=True, null=True)
    ttl = models.IntegerField()
    mx_priority = models.IntegerField(blank=True, null=True)
    view = models.CharField(max_length=7,default='any')
    priority = models.IntegerField(default=255)
    refresh = models.IntegerField(default=28800)
    retry = models.IntegerField(default=14400)
    expire = models.IntegerField(default=86400)
    minimum = models.IntegerField(default=86400)
    serial = models.BigIntegerField(default=2015050917)
    resp_person = models.CharField(max_length=64, default='ddns.net')
    primary_ns = models.CharField(max_length=64, default='ns.ddns.net.')

    class Meta:
        db_table = 'dns_records'
        index_together = ('zone', 'host')
