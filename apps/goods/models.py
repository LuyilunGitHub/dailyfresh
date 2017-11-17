from django.db import models
from tinymce.models import HTMLField
# Create your models here.


class Goods(models.Model):
    '''商品模型类'''
    STATUS_CHOICES = (
        (0, '下架'),
        (1, '上架')
    )
    # 0-下架 1-上架
    status = models.SmallIntegerField(default=1, choices=STATUS_CHOICES, verbose_name='商品状态')
    detail = HTMLField(verbose_name='商品详情')

    class Meta:
        db_table = 'df_goods'
        verbose_name = '商品'
        verbose_name_plural = verbose_name