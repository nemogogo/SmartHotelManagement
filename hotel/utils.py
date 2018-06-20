from django.db.models import Q
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import  HttpResponseRedirect,render
from hotelmanage.settings import EXCLUDE_URL,JSON_EXCLUDE_URL
import re
from django.contrib.auth import authenticate,login

exclued_path = [re.compile(item) for item in EXCLUDE_URL]
json_exclued_path= JSON_EXCLUDE_URL
class MyPermissionCheckMiddleware(MiddlewareMixin):
	
	def process_request(self, request):
		url_path = request.path
		
		for each in json_exclued_path:
			if url_path.startswith(each):
				return
		
		for menu in request.user.role.menus.all():
			if menu.url_name==request.path:
				return
			for  sub_menu in menu.sub_menus.all():
				if sub_menu.url_name == request.path:
					return
		else:
			
			
			return render(request,'403.html')
		
		  
		
	 
class AuthenticationCheckMiddleware(MiddlewareMixin):
	
	def process_request(self, request):
		url_path = request.path
		for each in exclued_path:
			if re.match(each, url_path):
				if request.method=='POST':
					user = request.POST.get('user')
					pwd = request.POST.get('password')
					user = authenticate(username=user, password=pwd)
					if user:
						login(request, user)
						return HttpResponseRedirect('/index/')
				return
	 
			if request.user.is_authenticated:
				return
			else:
				return HttpResponseRedirect('/login')
		else:
			return

def table_filter(request,admin_class):
     '''进行条件过滤并返回过滤后的数据'''
     filter_conditions={}
     keywords=['page','_o','_q']
     for k,v in request.GET.items():
         if k in keywords:
             '''保留的分页关键字，and 排序关键字'''
             continue
         if v:
             filter_conditions[k]=v
     return admin_class.model.objects.filter(**filter_conditions).order_by("%s" % admin_class.ordering if admin_class.ordering else  "id"),filter_conditions

def table_search(request,admin_class,obj_list):
    search_key=request.GET.get('_q','')
    q_obj=Q()
    q_obj.connector='OR'
    for column in admin_class.search_fields:
        q_obj.children.append(('%s__contains'%column,search_key))

    res=obj_list.filter(q_obj)
    return res

def table_sort(request,admin_class,objs):
    orderby_key=request.GET.get('_o')
    if orderby_key:
        if orderby_key.startswith('-'):
            orderby_key=orderby_key.strip('-')
        else:
            orderby_key='-%s'%orderby_key
        res=objs.order_by(orderby_key)
    else:
        orderby_key='id'
        res=objs
    # print('----------',orderby_key)
    return res,orderby_key


