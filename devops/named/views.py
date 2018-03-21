# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from  django.views.generic import  View,ListView, TemplateView, DetailView
from django.shortcuts import render
from django.contrib.auth.models import  User,Group
from django.contrib.auth.mixins import LoginRequiredMixin
from  django.http import  HttpResponse, JsonResponse, QueryDict
from  django.db import IntegrityError
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import  permission_required, login_required
from django.core.paginator import  Paginator, PageNotAnInteger ,EmptyPage
from django.db.models import Q
from  .pagerange import get_pagerange
from django.contrib.auth.mixins import  LoginRequiredMixin
from   accounts.mixins import PermissionRequiredMixin
from django.conf import settings

from  named.models import  dns_record
from  named.forms import dns_recordForm


class  NamedListView(LoginRequiredMixin,TemplateView,get_pagerange):
    model = dns_record
    template_name = "named/named_list.html"
    per = 10
    paginate_by = 10
    befor_range_num = 5
    after_range_num = 5


    def get_context_data(self, **kwargs):
        context = super(NamedListView, self).get_context_data(**kwargs)
        search = self.request.GET.get("search_data", None)                #获取搜索字段数据
        page_num = int(self.request.GET.get("page",1))                    #获取page id

        if search:
            obj_list = dns_record.objects.filter(Q(zone__contains=search)|Q(host__contains=search)|Q(type__contains=search)|Q(data__contains=search)|Q(ttl__contains=search)).order_by('id') #取搜索域名
        else:
            obj_list = dns_record.objects.get_queryset().order_by('id')

        paginator = Paginator(obj_list,self.per)
        pages_nums = paginator.num_pages #总分页数
        # 处理搜索条件

        search_data = self.request.GET.copy()
        try:
            search_data.pop("page")
        except BaseException as  e:
            pass
        context.update(search_data.dict())
        context['search_data'] = search_data.urlencode()

        try:
            context['page_obj'] = paginator.page(page_num)
        except PageNotAnInteger: #返回第一页数据
            context['page_obj'] = paginator.page(1)
        except EmptyPage:        #返回最后一页数据
            context['page_obj'] = paginator.page(pages_nums)

        context['page_range'] = self.get_pageranges(context["page_obj"]) #page_range分页列表数据
        context['object_list'] = context['page_obj'].object_list        #用户数据
        return  context

    def post(self, request):
        form = dns_recordForm(request.POST)
        if form.is_valid():
            form.save()
            res = {'code': 0, 'result': '添加解析成功'}
        else:
            # form.errors会把验证不通过的信息以对象的形式传到前端，前端直接渲染即可
            res = {'code': 1, 'errmsg': form.errors}
        return JsonResponse(res, safe=True)





class NamedDetailView(LoginRequiredMixin, DetailView):
    '''
    动作：getone, update, delete
    '''
    model = dns_record
    template_name = "named/named_detail.html"
    context_object_name = 'named'
    next_url = '/named/list/'

    def get_context_data(self, **kwargs):
        self.keyword = self.request.GET.get('keyword', '').strip()
        context = super(NamedDetailView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        p = self.model.objects.get(pk=pk)
        form = dns_recordForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            res = {"code": 0, "result": "更新成功", 'next_url': self.next_url}
        else:
            res = {"code": 1, "errmsg": form.errors, 'next_url': self.next_url}
        return render(request, settings.JUMP_PAGE, res)


    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        print(pk)
        #删除数据
        try:
            obj =self.model.objects.filter(pk=pk).delete()
            if obj:
                res = {"code": 0, "result": "删除成功"}
            else:
                res = {"code": 1, "errmsg": "该解析,请联系管理员"}
        except:
            res = {"code": 1, "errmsg": "删除错误请联系管理员"}
        return JsonResponse(res, safe=True)
