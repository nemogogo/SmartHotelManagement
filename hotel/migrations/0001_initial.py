# Generated by Django 2.0.5 on 2018-05-20 13:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, null=True, unique=True, verbose_name='email address')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CertificateType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='城市')),
            ],
        ),
        migrations.CreateModel(
            name='ConsumptionRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_created=True)),
                ('name', models.CharField(max_length=64, verbose_name='消费项目')),
                ('operator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='国家')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='name')),
                ('VIP', models.BooleanField(default=False, verbose_name='会员')),
                ('VIPID', models.CharField(blank=True, max_length=32, null=True, verbose_name='会员号')),
                ('Certificate_ID', models.CharField(max_length=32, verbose_name='证件号')),
                ('times', models.PositiveIntegerField(default=1, verbose_name='入住次数')),
                ('Certificate_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.CertificateType')),
            ],
        ),
        migrations.CreateModel(
            name='FirstLayerMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='菜单名')),
                ('url_type', models.SmallIntegerField(choices=[(0, 'related_name'), (1, 'absolute_url')], default=0)),
                ('url_name', models.CharField(max_length=64)),
                ('order', models.SmallIntegerField(default=0, verbose_name='菜单排序')),
            ],
            options={
                'verbose_name': '第一层菜单',
                'verbose_name_plural': '第一层菜单',
            },
        ),
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=8)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.Building')),
            ],
        ),
        migrations.CreateModel(
            name='GuestSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_name', models.CharField(max_length=32, null=True, unique=True, verbose_name='名称')),
                ('address', models.CharField(blank=True, max_length=32, null=True, verbose_name='地址')),
                ('contacts', models.CharField(blank=True, max_length=32, null=True, verbose_name='联系人')),
                ('contact_no', models.CharField(blank=True, max_length=32, null=True, verbose_name='联系方式')),
                ('note', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
        ),
        migrations.CreateModel(
            name='GuestSourceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='类型')),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='名称')),
                ('address', models.CharField(max_length=128, verbose_name='地址')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.City', verbose_name='城市')),
            ],
        ),
        migrations.CreateModel(
            name='HotelGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='名称')),
                ('hotels', models.ManyToManyField(to='hotel.Hotel', verbose_name='酒店')),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_time', models.DateTimeField(auto_now_add=True)),
                ('repair_day', models.DateTimeField(null=True, verbose_name='维修日期')),
                ('repair_operator', models.CharField(max_length=32, verbose_name='维修人员')),
                ('contact_no', models.CharField(max_length=32, verbose_name='联系方式')),
                ('problem', models.TextField(verbose_name='故障简介')),
                ('note', models.TextField(verbose_name='备注')),
                ('request_operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='保修人员')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkin', models.DateTimeField(auto_created=True, verbose_name='入住时间')),
                ('checkout', models.DateTimeField(blank=True, null=True, verbose_name='离店时间')),
                ('check_type', models.SmallIntegerField(choices=[(1, '现金'), (2, '支付宝'), (3, '微信'), (4, '信用卡'), (5, '借记卡'), (6, '会员卡'), (7, '记账')], verbose_name='结账方式')),
                ('Consumption', models.PositiveIntegerField(verbose_name='消费金额')),
                ('park', models.CharField(blank=True, max_length=16, null=True, verbose_name='停车位')),
                ('note', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.Customer', verbose_name='客人信息')),
                ('opertator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PriceDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(verbose_name='价格')),
                ('discount', models.SmallIntegerField(verbose_name='折扣')),
            ],
        ),
        migrations.CreateModel(
            name='PriceStrategy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='名称')),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='省份')),
            ],
        ),
        migrations.CreateModel(
            name='Reserve',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now_add=True, verbose_name='预定日期')),
                ('pre_checkin', models.DateField(verbose_name='入住日期')),
                ('pre_checkout', models.DateField(verbose_name='离店日期')),
                ('book_customer', models.CharField(max_length=64, verbose_name='预定人')),
                ('book_contact', models.CharField(max_length=32, verbose_name='联系方式')),
                ('reserve_status', models.SmallIntegerField(choices=[(1, '已预订'), (2, '已入住'), (3, '已取消'), (4, '预定未到')], default=1, verbose_name='预定状态')),
                ('customer_contact', models.CharField(blank=True, max_length=32, null=True, verbose_name='入住客人联系方式')),
                ('note', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
                ('book_resource', models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.GuestSource', verbose_name='预定来源')),
                ('book_resource_type', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='hotel.GuestSourceType', verbose_name='预定方式')),
                ('book_staff', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='操作员工')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='角色')),
                ('menus', models.ManyToManyField(blank=True, to='hotel.FirstLayerMenu')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('No', models.CharField(max_length=16, unique=True, verbose_name='房号')),
                ('floor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.Floor', verbose_name='楼层')),
                ('order', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='related_order', to='hotel.Order', verbose_name='关联订单')),
                ('reserve', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_reserve', to='hotel.Reserve', verbose_name='关联预定')),
            ],
        ),
        migrations.CreateModel(
            name='RoomFacility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='设施名')),
            ],
        ),
        migrations.CreateModel(
            name='RoomStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, unique=True, verbose_name='房态')),
            ],
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='房间类型')),
                ('bed_size', models.CharField(max_length=16, verbose_name='床宽')),
                ('bed_num', models.SmallIntegerField(verbose_name='床量')),
                ('window', models.SmallIntegerField(choices=[(1, '有'), (2, '无'), (3, '暗窗')], default=1, verbose_name='窗户')),
                ('room_facilities', models.ManyToManyField(to='hotel.RoomFacility', verbose_name='房间设施')),
            ],
        ),
        migrations.CreateModel(
            name='SubMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='二层菜单')),
                ('url_type', models.SmallIntegerField(choices=[(0, 'related_name'), (1, 'absolute_url')], default=0)),
                ('url_name', models.CharField(max_length=64, unique=True)),
                ('order', models.SmallIntegerField(default=0, verbose_name='菜单排序')),
            ],
        ),
        migrations.CreateModel(
            name='www',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='room',
            name='status',
            field=models.ForeignKey(default=2, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.RoomStatus', verbose_name='状态'),
        ),
        migrations.AddField(
            model_name='room',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.RoomType', verbose_name='房型'),
        ),
        migrations.AddField(
            model_name='reserve',
            name='room_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='hotel.RoomType', verbose_name='房型'),
        ),
        migrations.AddField(
            model_name='pricedetail',
            name='roomtype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.RoomType', verbose_name='房型'),
        ),
        migrations.AddField(
            model_name='pricedetail',
            name='strategy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.PriceStrategy', verbose_name='价格策略'),
        ),
        migrations.AddField(
            model_name='order',
            name='reserve',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.Reserve', verbose_name='订单信息'),
        ),
        migrations.AddField(
            model_name='maintenancerecord',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.Room', verbose_name='房间'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='provice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.Province', verbose_name='省份'),
        ),
        migrations.AddField(
            model_name='guestsource',
            name='price_strategy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.PriceStrategy'),
        ),
        migrations.AddField(
            model_name='guestsource',
            name='source_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.GuestSourceType', verbose_name='类型'),
        ),
        migrations.AddField(
            model_name='firstlayermenu',
            name='sub_menus',
            field=models.ManyToManyField(blank=True, to='hotel.SubMenu'),
        ),
        migrations.AddField(
            model_name='customer',
            name='guest_source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.GuestSource', verbose_name='客人来源'),
        ),
        migrations.AddField(
            model_name='consumptionrecord',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.Order', verbose_name='订单'),
        ),
        migrations.AddField(
            model_name='consumptionrecord',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.Room', verbose_name='房间'),
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.Province', verbose_name='省份'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.Role'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='room',
            unique_together={('type', 'No')},
        ),
        migrations.AlterUniqueTogether(
            name='pricedetail',
            unique_together={('strategy', 'roomtype')},
        ),
        migrations.AlterUniqueTogether(
            name='floor',
            unique_together={('name', 'building')},
        ),
    ]
