#coding: utf-8
from django.core.paginator import  Paginator, PageNotAnInteger ,EmptyPage


class get_pagerange:
    def get_pageranges(self, page_obj):
        current_index = page_obj.number
        start = current_index - self.befor_range_num
        end = current_index + self.after_range_num
        if start <= 0:
            start = 1
        if end >= page_obj.paginator.num_pages:
            end = page_obj.paginator.num_pages

        return range(start, end + 1)