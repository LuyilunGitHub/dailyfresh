from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel
# Create your models here.


class User(AbstractUser, BaseModel):
    '''用户模型类'''

    class Meta:
        db_table = 'df_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name




class AddressManager(models.Manager):
    #查询是否有默认地址
    def get_default_addr(self,user):
        try:
          address = self.get(user=user,is_default=True)
        except self.model.DoesNotExist as e:
            address = None
        return address

    #查询所有的地址
    def get_alladdrByuser(self,user):
        try:
            addrlist = self.filter(user=user).order_by('-is_default','-update_time')[0:5]
        except self.model.DoesNotExist as e:
            addrlist = None
        return addrlist



class Address(BaseModel):
    '''地址模型类'''
    user = models.ForeignKey('User', verbose_name='所属账户')
    receiver = models.CharField(max_length=20, verbose_name='收件人')
    addr = models.CharField(max_length=256, verbose_name='收件地址')
    zip_code = models.CharField(max_length=6, null=True, verbose_name='邮政编码')
    phone = models.CharField(max_length=11, verbose_name='联系电话')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')

    newObject=AddressManager()

    class Meta:
        db_table = 'df_address'
        verbose_name = '地址'
        verbose_name_plural = verbose_name