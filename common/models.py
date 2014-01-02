# coding: utf-8
from django.db import models
from django.contrib.auth.models import User


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


class Competence(models.Model):
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
    target = models.ForeignKey(User, verbose_name=u'Кому тег был проставлен', related_name='tags', null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Пользовательский тег'
        verbose_name_plural = u'Пользовательские теги'


class UserRating(models.Model):
    """
    Модель для пользовательского рейтинга
    """
    author = models.ForeignKey(User, verbose_name=u'Автор оценки', related_name='author_rating')
    target = models.ForeignKey(User, verbose_name=u'Кому была поставлена оценка', related_name='target_rating')
    rating = models.DecimalField(decimal_places=2, max_digits=5, verbose_name=u'Рейтинг пользователя')

    def __unicode__(self):
        return u'{}: {} -> {}'.format(self.rating, self.author, self.target)

    class Meta:
        verbose_name = u'Пользовательский рейтинг'
        verbose_name_plural = u'Пользовательские рейтинги'


class UserProfile(models.Model):
    """
    Модель для профайлов пользователя
    """
    user = models.OneToOneField(User, verbose_name=u'Пользователь', related_name='profile')
    phone = models.CharField(max_length=20, verbose_name=u'Номер телефона')
    rating = models.DecimalField(decimal_places=2, max_digits=5, default=1.0, verbose_name=u'Рейтинг пользователя')
    bTypes = models.ManyToManyField(BusinessType, verbose_name=u'Вид бизнеса', related_name='profiles')
    competences = models.ManyToManyField(Competence, verbose_name=u'Сфера компетенции', related_name='profiles')
    photo = models.ImageField(upload_to='uploads/', verbose_name=u'Фото', null=True)

    def __unicode__(self):
        return self.user.username

    def get_name(self):
        if self.user.first_name and self.user.last_name:
            return u'{} {}'.format(self.user.first_name, self.user.last_name)
        else:
            return self.user.username

    def get_tags(self):
        tags = [u'<a href="?tags={0}">{1}</a>'.format(tag.slug, tag.name) for tag in self.user.tags.all()]
        return u','.join(tags)

    def get_btypes(self):
        btypes = [u'<a href="?btypes={0}">{1}</a>'.format(b.slug, b.name) for b in self.bTypes.all()]
        return u','.join(btypes)

    def get_competences(self):
        competences = [u'<a href="?competences={0}">{1}</a>'.format(c.slug, c.name) for c in self.competences.all()]
        return u','.join(competences)

    class Meta:
        verbose_name = u'Профиль пользователя'
        verbose_name_plural = u'Профили пользователей'