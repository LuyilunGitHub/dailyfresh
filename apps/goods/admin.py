from django.contrib import admin
from  db.base_model import BaseModel
from apps.goods.models import  Goods
# Register your models here.
admin.site.register(Goods)