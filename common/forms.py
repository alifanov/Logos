# coding: utf-8
__author__ = 'vampire'
from django import forms
from common.models import Competence, BusinessType, UserTag

class NewUserForm(forms.Form):
    lastname = forms.CharField(help_text=u'Фамилия', label=u'Фамилия')
    firstname = forms.CharField(help_text=u'Имя', label=u'Имя')
    phone = forms.CharField(help_text=u'Телефон', label=u'Телефон')
    email = forms.EmailField(help_text=u'Email', label=u'Email')
    competences = forms.MultipleChoiceField(help_text=u'Сфера компетенции', label=u'Сфера компетенции', choices=[(a.name, a.name) for a in Competence.objects.all()])
    businesstypes = forms.MultipleChoiceField(help_text=u'Вид бизнеса', label=u'Вид бизнеса', choices=[(a.name, a.name) for a in BusinessType.objects.all()])
    tags = forms.MultipleChoiceField(help_text=u'Пользовательские теги', label=u'Пользовательские теги', choices=[(a.name, a.name) for a in UserTag.objects.all()])