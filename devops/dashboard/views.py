# -*- coding: utf-8 -*-
from django.shortcuts import render,reverse

# Create your views here.
from django.contrib.auth.decorators import login_required
from  django.views.generic import TemplateView,View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from  named.models import  dns_record
from  django.http import  HttpResponse, JsonResponse, QueryDict



class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = "darshboard.html"



class SuccessView(LoginRequiredMixin, TemplateView):
    template_name = "success.html"
    def get_context_data(self, **kwargs):
        context = super(SuccessView,self).get_context_data(**kwargs)
        success_name = self.kwargs.get("next", "")
        next_url = "/"
        try:
            next_url = reverse(success_name)
        except:
            pass
        context["next_url"] = reverse(success_name)
        return  context


class ErrorView(LoginRequiredMixin,TemplateView):
    template_name = "error.html"
    def get_context_data(self, **kwargs):
        context = super(ErrorView,self).get_context_data(**kwargs)
        error_name = self.kwargs.get("next", "")
        errmsg = self.kwargs.get("errmsg", "")

        next_url = "/"
        try:
            next_url = reverse(error_name)
        except:
            pass
        context["next_url"] = next_url
        context["errmsg"] = errmsg
        return context


class  DarshboardData(LoginRequiredMixin, View):
    dns_model = dns_record

    def get(self, request, *args, **kwargs):
        ret ={}
        ret['zone_counts'] = dns_record.objects.count()
        ret['zone_count'] = dns_record.objects.values('zone').distinct().count()
        return  JsonResponse(ret)
