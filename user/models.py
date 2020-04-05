from django.db import models

# Create your models here.


from home.models import TBook


class TAddress(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)  # 收获名
    address = models.CharField(max_length=100, blank=True, null=True)  # 详细地址
    zip_code = models.CharField(max_length=10, blank=True, null=True)  # 邮编
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # 手机号码
    home_number = models.CharField(max_length=15, blank=True, null=True)  # 固定电话
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)  # 用户id

    class Meta:
        managed = False
        db_table = 't_address'


class TCart(models.Model):
    book = models.ForeignKey(TBook, models.DO_NOTHING, blank=True, null=True)  # 书籍id
    count = models.IntegerField(blank=True, null=True)  # 数量
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)  # 用户id

    class Meta:
        managed = False
        db_table = 't_cart'


class TOrder(models.Model):
    book = models.ForeignKey(TBook, models.DO_NOTHING, blank=True, null=True)  # 书籍id
    amount = models.IntegerField(blank=True, null=True)  # 数量
    order = models.ForeignKey('TUserOrder', models.DO_NOTHING, blank=True, null=True)  # 订单id

    class Meta:
        managed = False
        db_table = 't_order'


class TUser(models.Model):
    username = models.CharField(max_length=20, blank=True, null=True)  # 用户名
    password = models.CharField(max_length=100, blank=True, null=True)  # 密码
    salt = models.CharField(max_length=20, blank=True, null=True)  # 盐

    class Meta:
        managed = False
        db_table = 't_user'


class TUserOrder(models.Model):
    order_id = models.CharField(max_length=50, blank=True, null=True)  # 订单号
    amount = models.IntegerField(blank=True, null=True)  # 总数
    user = models.ForeignKey(TUser, models.DO_NOTHING, blank=True, null=True)  # 用户id
    status = models.IntegerField(blank=True, null=True)  # 状态
    create_time = models.DateTimeField(blank=True, null=True)  # 生成时间
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)  # 总价
    address = models.ForeignKey(TAddress, models.DO_NOTHING, blank=True, null=True)  # 地址id

    class Meta:
        managed = False
        db_table = 't_user_order'


