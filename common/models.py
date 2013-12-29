# coding: utf-8
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class BusinessType(models.Model):
    """
    Модель для вида бизнеса
    """
    name = models.CharField(max_length=64, verbose_name=u'Вид бизнеса', unique=True)
    slug = models.CharField(max_length=64, verbose_name=u'Slug для вида бизнеса', unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Вид бизнеса'
        verbose_name_plural = u'Виды бизнеса'

class Сompetence(models.Model):
    """
    Модель для сферы компетентности пользователя
    """
    name = models.CharField(max_length=64, verbose_name=u'Сфера компетенции', unique=True)
    slug = models.CharField(max_length=64, verbose_name=u'Slug для сферы компетенции', unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Сфера компетенции'
        verbose_name_plural = u'Сферы компетенции'

class Tag(models.Model):
    """
    Модель для тегов пользователя.
    Те что он ставит себе сам.
    """
    name = models.CharField(max_length=10, verbose_name=u'Тег', unique=True)
    slug = models.CharField(max_length=20, verbose_name=u'Slug для тега', unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Тег'
        verbose_name_plural = u'Теги'

class UserTag(models.Model):
    """
    Модель для пользовательских тегов. Один пользователь другому может их проставить
    """
    name = models.CharField(max_length=10, verbose_name=u'Тег', unique=True)
    slug = models.CharField(max_length=20, verbose_name=u'Slug для тега', unique=True)
    author = models.ForeignKey(User, verbose_name=u'Автор тега', related_name='author_tags')
    target = models.ForeignKey(User, verbose_name=u'Кому тег был проставлен', related_name='tags')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Пользовательский тег'
        verbose_name_plural = u'Пользовательские теги'

class UserProfile(models.Model):
    """
    Модель для профайлов пользователя
    """
    user = models.ForeignKey(User, verbose_name=u'Пользователь')
    phone = models.CharField(max_length=20, verbose_name=u'Номер телефона')
    rating = models.DecimalField(decimal_places=2, max_digits=5, verbose_name=u'Рейтинг пользователя')
    bType = models.ForeignKey(BusinessType, verbose_name=u'Вид бизнеса', related_name='profiles')
    competence = models.ForeignKey(Сompetence, verbose_name=u'Сфера компетенции', related_name='profiles')