from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from registration.forms import RegistrationFormUniqueEmail
from registration.backends.default.views import RegistrationView

from common.views import HomeView, AddUserView, AddCompetenceView, AddBusinessTypeView, AddUserTagView,\
    logout_view, LoginView, GetAccessView, UserDetailView, PersonalView

urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^get-access/$', GetAccessView.as_view(), name='get-access'),
    url(r'^user/add/$', AddUserView.as_view(), name='add-user'),
    url(r'^personal/$', PersonalView.as_view(), name='personal'),
    url(r'^user/(?P<username>.*)/$', UserDetailView.as_view(), name='user-detail'),
    url(r'^competence/add/$', AddCompetenceView.as_view(), name='add-competence'),
    url(r'^tag/add/$', AddUserTagView.as_view(), name='add-user-tag'),
    url(r'^btype/add/$', AddBusinessTypeView.as_view(), name='add-business-type'),
    # url(r'^Logos/', include('Logos.foo.urls')),

    url(r'^accounts/register/$', RegistrationView.as_view(), kwargs={'form_class':RegistrationFormUniqueEmail}),
    url(r'^accounts/', include('registration.backends.default.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
#    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
