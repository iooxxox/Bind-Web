# _*_ coding: utf-8 _*_

from django.forms import ModelForm
from  named.models import  dns_record


class dns_recordForm(ModelForm):
    class Meta:
        model = dns_record
        fields = ['data','host','type','zone','ttl']


