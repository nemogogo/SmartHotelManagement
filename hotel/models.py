from django.db import models
from hotel.auth import UserProfileManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin

import django.utils.timezone as timezone
# Create your models here.
class FirstLayerMenu(models.Model):
    '''第一层侧边栏菜单'''
    name = models.CharField('菜单名',max_length=64)
    url_type_choices = ((0,'related_name'),(1,'absolute_url'))
    url_type = models.SmallIntegerField(choices=url_type_choices,default=0)
    url_name = models.CharField(max_length=64)
    order = models.SmallIntegerField(default=0,verbose_name='菜单排序')
    sub_menus = models.ManyToManyField('SubMenu',blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "第一层菜单"
        verbose_name_plural = "第一层菜单"


class SubMenu(models.Model):
    '''第二层侧边栏菜单'''

    name = models.CharField('二层菜单', max_length=64)
    url_type_choices = ((0,'related_name'),(1,'absolute_url'))
    url_type = models.SmallIntegerField(choices=url_type_choices,default=0)
    url_name = models.CharField(max_length=64)
    order = models.SmallIntegerField(default=0, verbose_name='菜单排序')

    def __str__(self):
        return self.name
class UserProfile(AbstractBaseUser,PermissionsMixin):

    email=models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=True
    )
    name=models.CharField(max_length=32,unique=True)
    is_active=models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    role = models.ForeignKey("Role", blank=True, null=True,on_delete=models.CASCADE)
   

    objects=UserProfileManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        #The user is identified by their email address
        return self.email
    def get_short_name(self):
        #The user is identified by their email address
        return self.email
    def __str__(self):
        return self.email
    def has_perm(self,perm,obj=None):
        "Does the user have a specific permission?"
        #Simplest possible answer:Yes,always
        return True
    def has_module_perms(self,app_label):
        "Does the user have permissions to view the app'app_label"
        #Simplest possible answer:Yes,always
        return True
    class Meta:
        permissions = (

        )
	
class Hotel(models.Model):
	name=models.CharField(max_length=32,verbose_name='名称',unique=True)
	address=models.CharField(max_length=128,verbose_name='地址')
	provice=models.ForeignKey('Province',verbose_name='省份',on_delete=models.CASCADE)
	city=models.ForeignKey('City',verbose_name='城市',on_delete=models.CASCADE)
	def __str__(self):
		return self.name
	
class City(models.Model):
	name=models.CharField(max_length=32,verbose_name='城市',unique=True)
	province=models.ForeignKey('Province',verbose_name='省份',on_delete=models.CASCADE)
	def __str__(self):
		return self.name
class Province(models.Model):
	name=models.CharField(max_length=32,verbose_name='省份',unique=True)
	def __str__(self):
		return self.name
	
class HotelGroup(models.Model):
	name=models.CharField(max_length=32,verbose_name='名称',unique=True)
	hotels=models.ManyToManyField('Hotel',verbose_name='酒店')
	def __str__(self):
		return self.name
 
class Role(models.Model):
	name=models.CharField(max_length=32,verbose_name='角色',unique=True)
	menus = models.ManyToManyField('FirstLayerMenu', blank=True)
	def __str__(self):
		return self.name
	

class RoomStatus(models.Model):
	name=models.CharField(max_length=16,verbose_name='房态',unique=True)
	def __str__(self):
		return self.name
class RoomType(models.Model):
	name=models.CharField(max_length=32,verbose_name='房间类型',unique=True)
	bed_size=models.CharField(max_length=16,verbose_name='床宽')
	bed_num=models.SmallIntegerField(verbose_name='床量')
	room_facilities=models.ManyToManyField('RoomFacility',verbose_name='房间设施')
	window_status=(
		(1,'有'),
		(2,'无'),
		(3,'暗窗')
	)
	window=models.SmallIntegerField(choices=window_status,verbose_name='窗户',default=1)
	def __str__(self):
		return self.name
class RoomFacility(models.Model):
	name=models.CharField(max_length=32,verbose_name='设施名',unique=True)
	def __str__(self):
		return self.name
	
class Room(models.Model):
	floor=models.ForeignKey('Floor',verbose_name='楼层',on_delete=models.CASCADE)
	No=models.CharField(max_length=16,verbose_name='房号',unique=True)
	status=models.ForeignKey('RoomStatus',verbose_name='状态',on_delete=models.CASCADE,null=True,default=2)
	type=models.ForeignKey('RoomType', verbose_name='房型', on_delete=models.CASCADE,null=True)
	reserve=models.ForeignKey('Reserve',verbose_name='关联预定' ,related_name='related_reserve',null=True,blank=True,on_delete=models.CASCADE)
	order=models.ForeignKey('Order',verbose_name='关联订单',on_delete=models.CASCADE,default=1,related_name='related_order')
	def __str__(self):
		return '%s-%s'%(self.type,self.No)
	class Meta:
		unique_together = ('type', 'No')
	
	
class Reserve(models.Model):
	order_date=models.DateTimeField(verbose_name='预定日期',auto_now_add=True)
	pre_checkin=models.DateField(verbose_name='入住日期')
	pre_checkout=models.DateField(verbose_name='离店日期')
	book_customer=models.CharField(max_length=64,verbose_name='预定人')
	book_contact=models.CharField(max_length=32,verbose_name='联系方式')
	book_resource_type = models.ForeignKey('GuestSourceType', verbose_name='预定方式', on_delete=models.CASCADE,
    	                                       default=0)
	book_resource = models.ForeignKey('GuestSource', verbose_name='预定来源', on_delete=models.CASCADE, default=0,null=True,blank=True)
	room_type=models.ForeignKey('RoomType',verbose_name='房型',on_delete=models.CASCADE,default=1)
	status_choices=(
		(1,'已预订'),
		(2,'已入住'),
		(3,'已取消'),
		(4,'预定未到')
	)
	reserve_status=models.SmallIntegerField(choices=status_choices,verbose_name='预定状态',default=1)
	book_staff=models.ForeignKey('UserProfile',verbose_name='操作员工',on_delete=models.CASCADE,default=0)
	customer_contact=models.CharField(max_length=32,verbose_name='入住客人联系方式',blank=True,null=True)
	note=models.CharField(max_length=128,verbose_name='备注',null=True,blank=True)
	def __str__(self):
		return '%s-%s-%s'%(self.order_date,self.room_type,self.book_customer)

class Customer(models.Model):
	name=models.CharField(max_length=64,verbose_name='name')
	VIP=models.SmallIntegerField(choices=((1,'REG'),(2,'VIP'),(3,'SVIP')),verbose_name='会员',default=1)
	contact=models.CharField(max_length=32,verbose_name='联系方式',default=1)
	VIPID=models.CharField(max_length=32,verbose_name='会员号',null=True,blank=True)
	guest_source=models.ForeignKey('GuestSource',verbose_name='客人来源',on_delete=models.CASCADE)
	Certificate_type=models.ForeignKey('CertificateType',on_delete=models.CASCADE)
	Certificate_ID = models.CharField(max_length=32, verbose_name='证件号')
	times=models.PositiveIntegerField(verbose_name='入住次数',default=0)
	def __str__(self):
		return self.name
	
 
class Country(models.Model):
	name=models.CharField(max_length=64,verbose_name='国家',unique=True)
	def __str__(self):
		return self.name
class GuestSourceType(models.Model):
    name=models.CharField(max_length=32,verbose_name='类型')
    def __str__(self):
	    return self.name
class PriceDetail(models.Model):
	roomtype=models.ForeignKey('RoomType',verbose_name='房型',on_delete=models.CASCADE)
	price=models.FloatField(verbose_name='价格')
	discount=models.SmallIntegerField(verbose_name='折扣')
	strategy=models.ForeignKey('PriceStrategy',on_delete=models.CASCADE,verbose_name='价格策略')
	def __str__(self):
		return '%s-%s'%(self.strategy,self.roomtype)
	class Meta:
		unique_together=('strategy','roomtype')
class PriceStrategy(models.Model):
	name=models.CharField(max_length=32,verbose_name='名称')
	def __str__(self):
		return self.name

class GuestSource(models.Model):
	 source_type=models.ForeignKey('GuestSourceType',verbose_name='类型',on_delete=models.CASCADE)
	 source_name=models.CharField(max_length=32,verbose_name='名称',null=True,unique=True)
	 price_strategy=models.ForeignKey('PriceStrategy',on_delete=models.CASCADE,null=True,blank=True)
	 address=models.CharField(max_length=32,verbose_name='地址',null=True,blank=True)
	 contacts=models.CharField(max_length=32,verbose_name='联系人',null=True,blank=True)
	 contact_no=models.CharField(max_length=32,verbose_name='联系方式',null=True,blank=True)
	 note=models.TextField(verbose_name='备注',null=True,blank=True)
	 responsible=models.ForeignKey('UserProfile',verbose_name='负责人',on_delete=models.CASCADE,null=True,blank=True)
	 def __str__(self):
		 return '%s-%s'%(self.source_type,self.source_name)

class CertificateType(models.Model):
	name=models.CharField(max_length=64,unique=True)
	def __str__(self):
		return self.name
	
class Order(models.Model):
	reserve=models.ForeignKey('Reserve',verbose_name='订单信息',on_delete=models.CASCADE,null=True,blank=True)
	customer=models.ForeignKey('Customer',verbose_name='客人信息',on_delete=models.CASCADE,default=8)
	checkin=models.DateTimeField(auto_created=True,verbose_name='入住时间')
	checkout=models.DateTimeField(verbose_name='离店时间',blank=True,null=True)
	check_choices=(
		(1,'现金'),
		(2,'支付宝'),
		(3,'微信'),
		(4,'信用卡'),
		(5,'借记卡'),
		(6,'会员卡'),
		(7,'记账')
	)
	check_type=models.SmallIntegerField(choices=check_choices,verbose_name='结账方式')
	Consumption=models.PositiveIntegerField(verbose_name='消费金额')
	park=models.CharField(max_length=16,verbose_name='停车位',blank=True,null=True)
	note=models.CharField(max_length=128,verbose_name='备注',null=True,blank=True)
	opertator=models.ForeignKey('UserProfile',on_delete=models.CASCADE,null=True)
	def __str__(self):
		return '%s-%s-%s'%(self.customer,self.checkin,self.checkout)

class ConsumptionRecord(models.Model):
	order=models.ForeignKey('Order',on_delete=models.CASCADE,verbose_name='订单',null=True)
	name=models.CharField(verbose_name='消费项目',max_length=64)
	amount=models.FloatField(verbose_name='消费金额',blank=True,null=True)
	time=models.DateTimeField(auto_now_add=True)
	room=models.ForeignKey('Room',on_delete=models.CASCADE,verbose_name='房间',null=True)
	operator=models.ForeignKey('UserProfile',on_delete=models.CASCADE,verbose_name='操作人')
	def __str__(self):
		return '%s-%s'%(self.order,self.name)
	operator=models.ForeignKey('UserProfile',on_delete=models.CASCADE,null=True)
class www(models.Model):
	name=models.CharField(max_length=32)
class Building(models.Model):
	name=models.CharField(max_length=32,unique=True)
	def __str__(self):
		return self.name
class MaintenanceRecord(models.Model):
	room=models.ForeignKey('Room',on_delete=models.CASCADE,verbose_name='房间')
	request_time=models.DateTimeField(auto_now_add=True)
	request_operator=models.ForeignKey('UserProfile',on_delete=models.CASCADE,verbose_name='报修人员')
	repair_day=models.DateTimeField(verbose_name='维修日期',null=True,blank=True)
	repair_operator=models.CharField(max_length=32,verbose_name='维修人员',null=True,blank=True)
	contact_no=models.CharField(max_length=32,verbose_name='联系方式',null=True,blank=True)
	problem=models.TextField(verbose_name='故障简介')
	note=models.TextField(verbose_name='备注')
	def __str__(self):
		return '%s-%s'%(self.room,self.request_time)
class Floor(models.Model):
	name=models.CharField(max_length=8)
	building=models.ForeignKey('Building',on_delete=models.CASCADE)
	def __str__(self):
		return '%s-%s'%(self.building,self.name)
	class Meta:
		unique_together=('name','building')
	 
	
	
	