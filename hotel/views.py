from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout
from hotel.autoadmin.forms import UserCreationForm
# Create your views here.
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from hotel.autoadmin.sites import site
from hotel import models
from hotel.autoadmin.forms import creat_model_form
from hotel.utils import  table_search,table_filter,table_sort
from django.core.paginator import Paginator
import time
from hotel.autoadmin import set_up


def acc_login(request):
	if request.method=='GET':
		return render(request,'login.html')
	else:
		user=request.POST.get('user')
		pwd=request.POST.get('password')
 
		user = authenticate(username=user,password=pwd)
		if user:
 
			login(request,user)
			return redirect('/index/')
		else:
			return redirect('/login/')

def acc_logout(req):
    logout(req)
    return redirect('/login/')
 
def index(request):
	
	user_menu=models.UserProfile.objects.get(id=request.user.id).role.menus.all()
 
	return render(request, 'index.html', {'menu_list':user_menu})

 
def systempage(request):
	return render(request, 'system.html', {'site': site})
 
def table_list(request,app_name,model_name):
	model_admin=site.enabled_admins.get(app_name).get(model_name)
	fields=[]
	for field_name in model_admin.list_display:
		field=model_admin.model._meta.get_field(field_name)
		fields.append(field)
	try:
	    query_set=model_admin.model.objects.all()
	except Exception as e:
		print(e)
 
	object_list, filter_condtions = table_filter(request, model_admin)
	object_list = table_search(request,  model_admin, object_list)
	# object_list, orderby_key = table_sort(request, model_admin, object_list)  # 排序后的结果
	paginator = Paginator(object_list,  model_admin.list_per_page)  # Show 25 contacts per page
	page = request.GET.get('page')
	try:
		query_sets = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		query_sets = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		query_sets = paginator.page(paginator.num_pages)
	return render(request,'table_list.html',{'model_name':model_name,
	                                         'app_name':app_name,
	                                         'model_admin':model_admin,
	                                         'fields':fields,
	                                         'query_set':object_list,
	                                         'filter_conditions':filter_condtions
	                                         })

 
def table_add(request,app_name,model_name):
	model_admin=site.enabled_admins.get(app_name).get(model_name)
 
	
	if request.method=='GET':
		
		if model_name == 'userprofile':
			form =UserCreationForm()
		else:
 
			setattr(model_admin,'is_add_form', True)
			model_form = creat_model_form(request, model_admin=model_admin)
			form = model_form()
	 
		for item in form:
			if item.name=='book_resource':
			    setattr(form, 'book_r', item.field.queryset)


		
		
		return render(request, 'table_add.html', {'form': form,
		                                          'model_name':model_name,
		                                          'app_name':app_name
		                                          })
	else:
		model_form = creat_model_form(request, model_admin=model_admin)
		form=model_form()
		if model_name == 'userprofile':
			model_form =UserCreationForm
			form = model_form()
		obj = request.POST
		obj = model_form(obj)
	 
		error_dict={}
		if obj.is_valid():
			try:
				obj.save()
				if request.POST.get('submit')=='继续添加':
					return render(request, 'table_add.html',{'form':form,
		                                          'model_name':model_name,
		                                          'app_name':app_name})
				return redirect('table_list', app_name, model_name)
			except Exception as e:
				print(e)
				error_dict.update({'error':e})
			 
		
		return render(request, 'table_add.html',{'form':obj,
		                                          'model_name':model_name,
		                                          'app_name':app_name,
		                                         'error_dict':error_dict
		})
 
def table_detail(request,app_name,model_name,id):

	model_admin = site.enabled_admins.get(app_name).get(model_name)
	model_form = creat_model_form(request, model_admin=model_admin)
	error_dict={}
	if request.method == 'GET':
		obj = model_admin.model.objects.get(id=id)
		obj = model_form(instance=obj)
		return render(request,'table_detail.html',{'form':obj})
	else:
		obj =request.POST
		obj1=model_admin.model.objects.get(id=id)
		obj = model_form(obj,instance=obj1)
		if obj.is_valid():
			try:
				obj.save()
				return redirect('table_list', app_name, model_name)
			except Exception as e:
				error_dict['error']=e
	 
		return render(request, 'table_add.html', {'form': obj,
		                                          'model_name': model_name,
		                                          'app_name': app_name,
		                                          'error_dict': error_dict})
 
def room(request,*args,**kwargs):
	
	app_name=site.enabled_admins.get('hotel')
	model_admin=app_name.get('room')
	filter_conditions={}
	floor_id=kwargs.get('floor_id')
	building_id=kwargs.get('building_id')
	status_id=kwargs.get('status_id')
	type_id=kwargs.get('type_id')
	if type_id=='o':
		type_list=models.RoomType.objects.all().values_list('id')
		type_list=list(zip(*type_list))[0]
		
	if status_id=='o':
		status_list=models.RoomStatus.objects.all().values_list('id')
		status_list=list(zip(*status_list))[0]
		filter_conditions['status_id__in'] = status_list
		
	else:
		filter_conditions['status_id'] = status_id
	
	if  building_id=='o':
		pass
	else:
		if floor_id=='o':
			floors = models.Floor.objects.filter(building_id=building_id).values_list('id')
			floor_list = [x[0] for x in list(floors)]
		
			filter_conditions['floor_id__in']=floor_list
		else:
			filter_conditions['floor_id']=floor_id
	
		
	room_query_set =model_admin.model.objects.filter(**filter_conditions)
	building_query_set=models.Building.objects.all()
	status_query_set=models.RoomStatus.objects.all()
	type_query_set=models.RoomType.objects.all()
 
	
	
	
	return render(request,'room.html',locals())

def quick_checkin(request,room_id):
	
	model_admin=site.enabled_admins.get('hotel').get('customer')
	model_form = creat_model_form(request, model_admin=model_admin)
	if request.method == 'GET':
		setattr(model_admin, 'is_add_form', True)
		form = model_form()
		return HttpResponse(form.as_table())
	else:
 
		customer = model_form(request.POST)
		m=dict(request.POST)
		m.pop('csrfmiddlewaretoken')
	
	
		if customer.is_valid():
			customer.save()
			order_date = time.localtime()
			pre_checkout = request.POST.get('pre_checkout')
			pre_checkin = time.localtime()
			room_id = room_id
			book_customer = customer.instance.name
			book_staff = request.user
			book_resource_id = customer.instance.guest_source
			book_resource_type_id = customer.instance.guest_source.source_type_id
			customer_contact = customer.instance.contact
		 
 
			obj = models.Reserve.objects.create(
			    order_date=time.localtime(),
				pre_checkout=request.POST.get('pre_checkout'),
				pre_checkin=time.localtime(),
				room_type=models.Room.objects.get(id=room_id).type,
				book_customer=customer.instance.name,
				book_staff=request.user,
				book_resource_id=customer.instance.guest_source,
				book_resource_type_id=customer.instance.guest_source.source_type_id,
			    customer_contact=str(request.POST.get('contact'))
			)
			obj.save()
		
		
		return  redirect('room',*['o','o','o','o'])


def add_consumption(request,room_id):

	model_admin = site.enabled_admins.get('hotel').get('consumptionrecord')
	order=models.Room.objects.filter(id=room_id).first().order
	model_form = creat_model_form(request, model_admin=model_admin)
	if request.method=='POST':
		import time
	 
		name=request.POST.get('name')
		amount=request.POST.get('amount')
		obj=models.ConsumptionRecord.objects.create(
			order=order,
			operator=request.user,
			room_id=room_id,
			time=time.time(),
			amount=amount,
			name=name
		)
		try:
			order.Consumption=order.Consumption+int(obj.amount)
			order.save()
		 
		except Exception as e:
			pass
			
		return redirect('room',*['o','o','o','o'])
	else:
		 raise PermissionError
		
		
def report(request):
 
	guestsource_list=models.GuestSource.objects.all()
	responsible_list=models.UserProfile.objects.all()
	import datetime
	checkintime=time.mktime(datetime.datetime.today().timetuple())
 
	checkouttime=time.mktime((datetime.datetime.today()-datetime.timedelta(days=1)).timetuple())
	checkoutdate = datetime.datetime.now().strftime('%Y-%m-%d')
	checkindate =(datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
 
	return render(request,'report.html',locals())

def get_orders(request,guest_source_id,responsible_id,page_num,checkin,checkout):
	from django.db.models import Q
	q = Q()
	if guest_source_id != '0':
		q.children.append(('customer__guest_source_id',guest_source_id))
	if responsible_id != '0':
		q.children.append(('customer__guest_source__responsible_id',responsible_id))
	q.children.append(('checkin__gt',checkin))
	q.children.append(('checkout__lt',checkout))
 
	order_list = models.Order.objects.filter(q)
	try:
		paginator=Paginator(order_list,6)
		orders = paginator.page(int(page_num))
	except Exception as e:
		print(e)
	
	
	consumption_all=sum([x[0] for x in list(order_list.values_list('Consumption'))])
	
	
	return render(request,'get-orders.html',locals())

def analysis(request):
	guest_type=models.GuestSourceType.objects.all()
	data={}
	for type in guest_type:
 
		count=models.Order.objects.filter(customer__guest_source__source_type=type).count()
		data.update({type:count})
	print(data)
	return render(request,'data.html',locals())

def get_data(request):
	ret={'status':0,'data':''}
	data = []
 
	if request.GET.get('type')=='pre_c':
		guest_type = models.GuestSourceType.objects.all()
		for type in guest_type:
			count = models.Order.objects.filter(customer__guest_source__source_type=type).count()
			data.append({'value': count, 'name': type.name})
		ret['data']=data
  
		ret['para']={'title':'顾客来源分析表','subtitle':time.strftime('%Y-%m-%d'),'th':'顾客来源'}
	elif request.GET.get('type')=='pre_sale':
		responsible=models.UserProfile.objects.filter(role_id=2).all()
		for res in responsible:
			count=models.Order.objects.filter(customer__guest_source__responsible=res).count()
			data.append({'value': count, 'name': res.name})
		ret['data']=data
		ret['para']={'title':'销售业绩分析表','subtitle':'2018-3-1','th':'销售'}
	elif request.GET.get('type')=='ct':
		order_list=models.Order.objects.all()
		kv = [{'name': "22:00-01:00", 'value': 0},
		      {'name': "01:00-08:00", 'value': 0},
		      {'name': "08:00-12:00", 'value': 0},
		      {'name': "12:00-14:00", 'value': 0},
		      {'name': "14:00-18:00", 'value': 0},
		      {'name': "18:00-22:00", 'value': 0}]
		for order in order_list:
			
			if  order.checkin.strftime('%H:%M')<'01:00' or order.checkin.strftime('%H:%M')>='22:00':
				kv[0]['value']+=1
			elif order.checkin.strftime('%H:%M')>='01:00' and order.checkin.strftime('%H:%M')<'08:00':
				kv[1]['value']+= 1
			elif order.checkin.strftime('%H:%M')>='08:00' and order.checkin.strftime('%H:%M')<'12:00':
				kv[2]['value']+= 1
			elif order.checkin.strftime('%H:%M') >= '12:00' and order.checkin.strftime('%H:%M') < '14:00':
				kv[3]['value']+=1
			elif order.checkin.strftime('%H:%M') >= '14:00' and order.checkin.strftime('%H:%M') < '18:00':
				kv[4]['value']+=1
			elif order.checkin.strftime('%H:%M') >= '18:00' and order.checkin.strftime('%H:%M') < '22:00':
				kv[5]['value']+=1
	 
		for k in kv:
			data.append({'value': k['value'], 'name': k['name']})
		ret['data'] = data
		ret['para'] = {'title': '到店时间分析图', 'subtitle': '2018', 'th': '到店时间'}
	elif request.GET.get('type') == 'con-mode':
 
		for check_type in models.Order.check_choices:
			count=models.Order.objects.filter(check_type=check_type[0]).count()
			data.append({'value': count, 'name':check_type[1]})
		ret['data'] = data
		ret['para'] = {'title': '支付方式分析图', 'subtitle': '2018', 'th': '支付方式'}
	elif request.GET.get('type') == 'stay':
		order_list=models.Order.objects.all()
		kv = [{'name': "1天", 'value': 0},
		      {'name': "2天", 'value': 0},
		      {'name': "3-7天", 'value': 0},
		      {'name': "7-15天", 'value': 0},
		      {'name': "15-30天", 'value': 0},
		      {'name': "30天以上天", 'value': 0}]
		for order in order_list:
			if order.checkin.year==order.checkout.year:
				if order.checkin.month==order.checkout.month:
					days=order.checkout.day-order.checkin.day
					if days<=1:
						kv[0]['value']+=1
					elif days==2:
						kv[1]['value']+=1
					elif days>=3 and days <7:
						kv[2]['value']+=1
					elif days>=7 and days <15:
						kv[3]['value']+=1
					elif days>=15 and days <30:
						kv[4]['value']+=1
					elif days >= 30 :
						kv[5]['value'] += 1
				else:
					month=(order.checkout -order.checkin).days
					kv[5]['value']+=1
		for k in kv:
			data.append({'value': k['value'], 'name': k['name']})
		 
		ret['data'] = data
		ret['para'] = {'title': '顾客连住分析图', 'subtitle': '2018', 'th': '入住时间'}
	elif request.GET.get('type') == 'money':
		order_list=models.Order.objects.all()
		kv = [{'name': "300元以下", 'value': 0},
		      {'name': "200-1000元", 'value': 0},
		      {'name': "1000元以上", 'value': 0}]
		kv[0]['value']=models.Order.objects.filter(Consumption__lte=300).count()
		kv[1]['value']=models.Order.objects.filter(Consumption__gt=300).filter(Consumption__lte=1000).count()
		kv[2]['value']=models.Order.objects.filter(Consumption__gt=1000).count()
		for k in kv:
			data.append({'value': k['value'], 'name': k['name']})
		
		ret['data'] = data
		ret['para'] = {'title': '消费金额分析表', 'subtitle': '2018', 'th': '消费金额'}
	elif request.GET.get('type') == 'fr':
		customer_list = models.Customer.objects.all()
		kv = [{'name': "1次", 'value': 0},
		      {'name': "2次", 'value': 0},
		      {'name': "3次以上", 'value': 0}]
		for customer in customer_list:
			if customer.times == 1:
				kv[0]['value'] += 1
			elif customer.times == 2:
				kv[1]['value'] += 1
			else:
				kv[2]['value'] += 1
		for k in kv:
			data.append({'value': k['value'], 'name': k['name']})
		
		ret['data'] = data
		ret['para'] = {'title': '入住频率分析表', 'subtitle': '2018', 'th': '入住次数'}
	
	return JsonResponse(ret)
	
	
	
	