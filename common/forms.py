# coding: utf-8
__author__ = 'vampire'
from django import forms
from common.models import Competence, BusinessType, UserTag, UserProfile
from django.contrib.auth.models import User

class UpdateUserForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=UserTag.objects.all(), required=False
    )

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['tags'].initial = [str(tag.pk) for tag in self.instance.tags.filter(author=self.instance).all()]

    def save(self, *args, **kwargs):
        kwargs.pop('commit', None)
        u = super(UpdateUserForm, self).save(*args, **kwargs)
        u.tags.add(*self.cleaned_data['tags'])
        return u

    class Meta:
        model = User
        fields = ('first_name', 'last_name',)

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('vk', 'phone', 'photo', 'competences', 'bTypes')

class ImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('photo',)

class NewUserForm(forms.Form):
    lastname = forms.CharField(help_text=u'Фамилия', label=u'Фамилия')
    firstname = forms.CharField(help_text=u'Имя', label=u'Имя')
    phone = forms.CharField(help_text=u'Телефон', label=u'Телефон')
    email = forms.EmailField(help_text=u'Email', label=u'Email')
    competences = forms.MultipleChoiceField(help_text=u'Сфера компетенции', label=u'Сфера компетенции',
        choices=[(a.name, a.name) for a in Competence.objects.all()], required=False)
    businesstypes = forms.MultipleChoiceField(help_text=u'Вид бизнеса', label=u'Вид бизнеса',
        choices=[(a.name, a.name) for a in BusinessType.objects.all()], required=False)
    tags = forms.MultipleChoiceField(help_text=u'Пользовательские теги', label=u'Пользовательские теги',
        choices=[(a.name, a.name) for a in UserTag.objects.all()], required=False)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError(u'Пользователь с таким email уже есть в базе')
        return email