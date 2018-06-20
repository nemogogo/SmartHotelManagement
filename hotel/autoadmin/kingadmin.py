#__author:zhang_lei

from hotel import models
from hotel.autoadmin.sites import site
from hotel.autoadmin.base_admin import BaseKingAdmin
from django.contrib.auth.models import Group

class UserProfileAdmin(BaseKingAdmin):
    list_display = ['id','last_login','email','is_staff']
    list_filters = [ 'role']
    search_fields = ['name']
    readonly_fields = ['id','last_login','email','password']

class RoomAdmin(BaseKingAdmin):
    list_display = ['id','No','status','type','floor']
    list_filters = [ 'status','type','building','floor']
    search_fields = ['type']
    readonly_fields = ['id']
class RoomStatusAdmin(BaseKingAdmin):
	list_display = ['id','name']
class GuestSourceAdmin(BaseKingAdmin):
	list_display = ['id',  'source_name', 'contacts', 'responsible']
	list_filters = ['responsible', 'source_type',  ]
	search_fields = ['source_name']
	
class OrderAdmin(BaseKingAdmin):
	list_display = ['id','customer','checkin','checkout']
	list_filters = ['checkin','checkout']
 
class ReserveAdmin(BaseKingAdmin):
	list_display = ['id','book_customer','order_date','book_contact','pre_checkin','pre_checkout']
	list_filters = ['pre_checkin','pre_checkout','book_resource_type', ]
	search_fields = ['book_customer']
 
class RoomAdmin(BaseKingAdmin):
	list_display = ['id','floor','status']
	readonly_fields = ['id','floor','No','type']
class CustomerAdmin(BaseKingAdmin):
	list_display = ['id','name','guest_source','VIP']
	search_fields = ['name',]
	list_filters =['VIP','guest_source']
site.register(models.UserProfile,UserProfileAdmin)
site.register(models.Room,RoomAdmin)
site.register(models.RoomFacility)
site.register(models.Customer,CustomerAdmin)
site.register(models.Reserve,ReserveAdmin)
site.register(models.CertificateType)
site.register(models.GuestSource,GuestSourceAdmin)
site.register(models.Order,OrderAdmin)
site.register(models.Role)
site.register(models.RoomStatus,RoomStatusAdmin)
site.register(models.RoomType)
site.register(models.City)

site.register(models.Country)
site.register(models.Hotel)
site.register(Group)
site.register(models.FirstLayerMenu)
site.register(models.SubMenu)
site.register(models.Building)
site.register(models.Floor)
site.register(models.GuestSourceType)
site.register(models.MaintenanceRecord)
site.register(models.PriceStrategy)
site.register(models.PriceDetail)
site.register(models.ConsumptionRecord)



















