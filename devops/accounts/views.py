# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import  JsonResponse,HttpResponseRedirect,HttpResponse
from django.urls import reverse
from models import  *
from  django.views.generic import  View,ListView,TemplateView

# Create your views here.

class  LoginView(TemplateView):
    template_name = "user/login.html"
    def post(self, request):
        username = request.POST.get("username","")
        passwd  =  request.POST.get("password","")
        user = authenticate(username=username, password=passwd)
        results = {'code': 0, 'msg': u"Successful"}
        if user:
            login(request, user)
            results['next_url'] = request.GET.get("next") if request.GET.get("next", None) else "/"
        else:
            results = {'code': 1, 'msg': u"用户名或者密码错误!"}
        return JsonResponse(results)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("user_login"))