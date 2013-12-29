__author__ = 'vampire'
from models import UserProfile, UserRating, UserTag, Competence, BusinessType, Tag
from django.contrib import admin


admin.site.register(UserProfile)
admin.site.register(UserRating)
admin.site.register(UserTag)
admin.site.register(Competence)
admin.site.register(BusinessType)
admin.site.register(Tag)