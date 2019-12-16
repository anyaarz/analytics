from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

class Domain(models.Model):
    name = models.CharField(max_length=200, blank=True, verbose_name='Название')
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'domain_user', verbose_name='Пользователи')
    def __str__(self):
        return self.name

class Items(models.Model):
    name = models.CharField(max_length=200, blank=True, verbose_name='Название')
    domain = models.ForeignKey(Domain, null = True, blank = True, help_text='Укажите область', verbose_name='Область знаний',on_delete=models.CASCADE,)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'author', verbose_name='Пользователи')
    value = models.IntegerField(blank=True, null = True, verbose_name='Значение')
    source = models.CharField(max_length=200, blank=True, verbose_name='Источник')    
    date_created = models.DateField(auto_now_add=False, verbose_name='Дата создания')
    date_updated = models.DateField(auto_now_add=False, verbose_name='Дата обновления')
    def __str__(self):
        return self.name
    

class Relation(models.Model):
    STATUS_CHOICES = (
        ('0', 'неопределенное'),
        ('1', 'включает в себя'),
        ('2', 'является пререквизитом'),
        ('3', 'тождество'),
        ('4', 'являются частями одного раздела'),
        ('5', 'отсутствует'),
    )
    item1 = models.ForeignKey(Items,on_delete=models.CASCADE, related_name = 'item1', blank=True, null=True)
    item2 = models.ForeignKey(Items,on_delete=models.CASCADE, related_name = 'item2',  blank=True, null=True)
    relation = models.CharField(max_length=10, choices=STATUS_CHOICES, default='0')

class Data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'data_user', verbose_name='Пользователи')
    date = models.DateField(auto_now_add=True, verbose_name='Дата')
    change_msg = models.TextField(max_length=500, blank=True, verbose_name='Действие')
    item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name = 'item_list', verbose_name='Сущности')
    action = models.TextField(max_length=500, blank=True, verbose_name='Тип действия')
    result = models.TextField(max_length=500, blank=True, verbose_name='Результат')

# Create your models here.
