from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from common.views import HomeView, AddUserView, AddCompetenceView, AddBusinessTypeView, AddUserTagView

urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^user/add/$', AddUserView.as_view(), name='add-user'),
    url(r'^competence/add/$', AddCompetenceView.as_view(), name='add-competence'),
    url(r'^tag/add/$', AddUserTagView.as_view(), name='add-user-tag'),
    url(r'^btype/add/$', AddBusinessTypeView.as_view(), name='add-business-type'),
    # url(r'^Logos/', include('Logos.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT})
)
