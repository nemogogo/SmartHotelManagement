from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from hotel import models
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ['name']


class OrderAdmin(admin.ModelAdmin):
	list_display = ['customer','checkin','checkout']
class SubmenuAdmin(admin.ModelAdmin):
	list_display = ['name','url_name']


admin.site.register(models.UserProfile)
admin.site.register(models.Room)
admin.site.register(models.RoomFacility)
admin.site.register(models.Customer)
admin.site.register(models.Reserve)
admin.site.register(models.CertificateType)
admin.site.register(models.GuestSource)
admin.site.register(models.Order,OrderAdmin)
admin.site.register(models.Role)
admin.site.register(models.FirstLayerMenu)
admin.site.register(models.RoomStatus)
admin.site.register(models.RoomType)
admin.site.register(models.City)
admin.site.register(models.Country)
admin.site.register(models.Hotel)
admin.site.register(models.SubMenu,SubmenuAdmin)


