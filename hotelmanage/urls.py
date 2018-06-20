"""hotelmanage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from hotel import views
urlpatterns = [
    path('admin/', admin.site.urls),
	url(r'^login/$',views.acc_login,name='acc_login'),
	url(r'^logout/$', views.acc_logout, name='acc_logout'),
    url(r'^index/$',views.index,name='index'),
     url(r'^system/$',views.systempage,name='system'),
	url(r'analysis/$',views.analysis,name='analysis'),
	url(r'get_data/$',views.get_data,name='get_data'),
url(r'^quick_checkin/(?P<room_id>\d+)$',views.quick_checkin,name='quick_checkin'),
url(r'^report$',views.report,name='report'),
url(r'^get-orders/(?P<guest_source_id>\d+)/(?P<responsible_id>\d+)/(?P<page_num>\d+)/(?P<checkin>([\d-]+))/(?P<checkout>[\d-]+)$',views.get_orders,name='get_orders'),
url(r'^add_consumption/(?P<room_id>\d+)$',views.add_consumption,name='add_consumption'),
url(r'^room-(?P<building_id>([\d+o]))-(?P<floor_id>([\d+o]))-(?P<status_id>([\d+o]))-(?P<type_id>([\d+o]))$',views.room,name='room'),
url(r'^(?P<app_name>\w+)/(?P<model_name>\w+)/$',views.table_list,name='table_list'),
url(r'^(?P<app_name>\w+)/(?P<model_name>\w+)/add/$',views.table_add,name='table_add'),
url(r'^(?P<app_name>\w+)/(?P<model_name>\w+)/(?P<id>\d+)/change/$',views.table_detail,name='table_detail'),
]
