#__author:zhang_lei
#date:2018/2/8


from django import template
from django.core.exceptions import FieldDoesNotExist
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime,timedelta

register = template.Library()


@register.simple_tag
def render_model_content(request,item):
	role_id=request.user.role.id
	status_id=item.status.id
	ele=''
	customer = None
	checkin = None
	pre_checout = None
	reserve_customer=None
	customer_contacts=None
	pre_checkin = None
	try:
		customer=item.order.customer
		reserve_customer = item.reserve.book_customer
		customer_contacts=item.reserve.customer_contact
		checkin=item.order.checkin
		pre_checkin=item.reserve.pre_checkin
		pre_checout=item.reserve.pre_checkout
	except Exception:
		pass
	
	if   status_id in [1,4,7]:
		cus_name="<p>客人姓名：{customer}</p>".format(customer=customer)
		checkin_time="<p>入住时间：{checkin}</p>".format(checkin=checkin)
		pre_checkout_time="<p>预离日期:{pre_checkout}</p>".format(pre_checkout=pre_checout)
		
		if role_id in [1,2,3,4]:
			ele+=cus_name+checkin_time+pre_checkout_time
			if request.user.role.id ==1:
				ele+="<p><a href='#' class='add_consumption' >添加消费</a></p><p><a href='#'>快速结账</a></p><p><a href='#'>查看详情</a></p>"
		else:
			ele+=checkin_time+pre_checkout_time
		return mark_safe(ele)
	if status_id == 2:
		if role_id ==1:
		    ele += "<p><a class='quick_checkin' >快速入住</a></p><p><a href='/hotel/reserve/add'>预定房间</a></p><p><a href='/hotel/maintenancerecord/add'>报修</a></p>"
		else:
			ele="<p>空房</p>"
		return mark_safe(ele)
	if status_id == 3:
		if role_id in [1,2,3,4,5]:
			ele+="<p><a>房间打扫中</a></p>"
		if role_id == 6:
			ele+="<p><a>打扫房间</a></p>"
		return mark_safe(ele)
	if status_id == 5:
		cus_name = "<p>预定人：{reserve_customer}</p>".format(reserve_customer=reserve_customer)
		pre_checkin_time = "<p>预抵日期：{pre_checkin}</p>".format(pre_checkin=pre_checkin)
		pre_checkout_time = "<p>预离日期:{pre_checkout}</p>".format(pre_checkout=pre_checout)
		customer_contacts="<p>联系方式：{contact}</a>".format(contact=customer_contacts)
		if role_id in [1,2,3]:
			ele+=cus_name+customer_contacts+pre_checkin_time+pre_checkout_time
			
			ele+="<p><a>快速入住</a></p><p><a>修改订单</a></p>"
			return  mark_safe(ele)
		else:
			ele=pre_checkout_time+pre_checkout_time
			return  mark_safe(ele)

@register.simple_tag
def render_sorted_arrow(column,sorted_column):
    if column in sorted_column:  # 这一列被排序了,
        last_sort_index = sorted_column[column]
        if last_sort_index.startswith('-'):
            arrow_direction = 'bottom'
        else:
            arrow_direction = 'top'
        ele = '''<span class="glyphicon glyphicon-triangle-%s" aria-hidden="true"></span>''' % arrow_direction
        return mark_safe(ele)
    return ''
@register.simple_tag
def get_sorted_column(column,sorted_column,forloop):
    #sorted_column = {'name': '-0'}
    if column in sorted_column:#这一列被排序了,
        #你要判断上一次排序是什么顺序,本次取反
        last_sort_index = sorted_column[column]
        if last_sort_index.startswith('-'):
            this_time_sort_index = last_sort_index.strip('-')
        else:
            this_time_sort_index = '-%s' % last_sort_index
        return this_time_sort_index
    else:
        return forloop

@register.simple_tag
def render_filter_ele(filter_field,admin_class,filter_condtions):
    #select_ele = '''<select class="form-control" name='%s' ><option value=''>----</option>''' %filter_field
    select_ele = '''<select class="form-control" name='{filter_field}' ><option value=''>----</option>'''
    field_obj = admin_class.model._meta.get_field(filter_field)
  
    if field_obj.choices:
        selected = ''
        for choice_item in field_obj.choices:
            # print("choice",choice_item,filter_condtions.get(filter_field),type(filter_condtions.get(filter_field)))
            if filter_condtions and filter_condtions.get(filter_field) == str(choice_item[0]):
                selected ="selected"

            select_ele += '''<option value='%s' %s>%s</option>''' %(choice_item[0],selected,choice_item[1])
            selected =''

    if type(field_obj).__name__ == "ForeignKey":
        selected = ''
        for choice_item in field_obj.get_choices()[1:]:
	        if filter_condtions:
	            if filter_condtions.get(filter_field)== str(choice_item[0]):
	                selected = "selected"
			        
	        select_ele += '''<option value='%s' %s>%s</option>''' %(choice_item[0],selected,choice_item[1])
	        selected=''
    if type(field_obj).__name__ in ['DateTimeField','DateField']:
        date_els = []
        today_ele = datetime.now().date()
        date_els.append(['今天', datetime.now().date()])
        date_els.append(["昨天",today_ele - timedelta(days=1)])
        date_els.append(["近7天",today_ele - timedelta(days=7)])
        date_els.append(["本月",today_ele.replace(day=1)])
        date_els.append(["近30天",today_ele - timedelta(days=30)])
        date_els.append(["近90天",today_ele - timedelta(days=90)])
        date_els.append(["近180天",today_ele - timedelta(days=180)])
        date_els.append(["本年",today_ele.replace(month=1,day=1)])
        date_els.append(["近一年",today_ele  - timedelta(days=365)])

        selected = ''
        for item in date_els:
            select_ele += '''<option value='%s' %s>%s</option>''' %(item[1],selected,item[0])
	        
	        

        filter_field_name = "%s__gte" % filter_field


    else:
        filter_field_name = filter_field
        
    
    select_ele += "</select>"
    select_ele = select_ele.format(filter_field=filter_field_name)
 
    

    return mark_safe(select_ele)


@register.simple_tag
def render_sorted_arrow(column,sorted_column):
    if column in sorted_column:  # 这一列被排序了,
        last_sort_index = sorted_column[column]
        if last_sort_index.startswith('-'):
            arrow_direction = 'bottom'
        else:
            arrow_direction = 'top'
        ele = '''<span class="glyphicon glyphicon-triangle-%s" aria-hidden="true"></span>''' % arrow_direction
        return mark_safe(ele)
    return ''
@register.simple_tag
def get_model_name(admin_class):
    return admin_class.model._meta.model_name
@register.simple_tag
def build_table_row(obj,admin_class):
    ele = ''
    if admin_class.list_display:
        for index, column_name in enumerate(admin_class.list_display):

            column_obj = admin_class.model._meta.get_field(column_name)
            if column_obj.choices:  # get_xxx_display
                column_data = getattr(obj, 'get_%s_display' % column_name)()
            else:
                column_data = getattr(obj, column_name)

            if index == 0:
                td_ele = "<td><a href='/%s/%s/%d/change'>%s</a></td>" % (admin_class.model._meta.app_label,admin_class.model._meta.model_name,obj.id, column_data)
            else:
                td_ele = "<td>%s</td>" % column_data
            ele += td_ele
    else:
        td_ele = "<td><a href='%d/change'>%s</a></td>" % (obj.id, obj)
        ele += td_ele
    return mark_safe(ele)

@register.simple_tag
def display_related_objs(obj):
    """
    显示将要被删除的对象的所有关联对象
    :param obj:
    :return:
    """
    ele='<ul>'
    for reversed_fk_obj in obj._meta.related_objects:
        related_table_name=reversed_fk_obj.name
        related_lookup_key='%s_set'%related_table_name
        related_objs=getattr(obj,related_lookup_key).all()
        ele='<li>%s3333<ul>'%related_table_name
        if reversed_fk_obj.get_internal_type()=='ManyToManyField':
            for o in related_objs:
                ele+="<li><a href='/hotel/%s/%s/%s/change/'>%s</a>记录里与[%s]相关的数据都将" \
                     "被删除</li>"%(o._meta.app_label,o._meta.model_name,o.id,o,obj)
        else:
             for o in related_objs:
                 ele+="<li><a href='/hotel/%s/%s/%s/change/'>%s</a></li>"%(o._meta.app_label,
                                                                         o._meta.model_name,o.id,o)
                 ele+=display_related_objs(o)
        ele+="</ul></li>"
    ele+="</ul>"
    return mark_safe(ele)

@register.simple_tag
def render_filtered_args(model_admin,render_html=True):
    '''拼接筛选的字段'''
    if model_admin.filter_condtions:
        ele = ''
        for k,v in model_admin.filter_condtions.items():
            ele += '&%s=%s' %(k,v)
        if render_html:
            return mark_safe(ele)
        else:
            return ele
    else:
        return ''


	
			
	
			
	
			
		
	
 
		
 
		
  
	
