from django.contrib import messages
from django.views.generic import TemplateView, FormView, View
from common.forms import NewUserForm
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.http import HttpResponse
from common.models import UserProfile, Competence, BusinessType, UserTag
# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

class AddCompetenceView(View):
    def post(self, request, *args, **kwargs):
        comp = request.POST.get('competence', False)
        resp = u''
        if comp:
            c = Competence.objects.create(name=comp, slug=slugify(comp))
            resp = u'[{}, {}]'.format(c.name, c.name)
        return HttpResponse(resp)

class AddBusinessTypeView(View):
    def post(self, request, *args, **kwargs):
        btype = request.POST.get('btype', False)
        resp = u''
        if btype:
            c = BusinessType.objects.create(name=btype, slug=slugify(btype))
            resp = u'[{}, {}]'.format(c.name, c.name)
        return HttpResponse(resp)

class AddUserTagView(View):
    def post(self, request, *args, **kwargs):
        tag = request.POST.get('tag', False)
        resp = u''
        if tag:
            c = UserTag.objects.create(name=tag, slug=slugify(tag), author=request.user)
            resp = u'[{}, {}]'.format(c.name, c.name)
        return HttpResponse(resp)

class AddUserView(FormView):
    template_name = 'add-contact.html'
    form_class = NewUserForm

    def form_invalid(self, form):
        print 'FORM INVALID'
        return super(AddUserView, self).form_invalid(form)

    def form_valid(self, form):
        print 'FORM VALID'
        username = u'username{}'.format(User.objects.count()+1)
        password = User.objects.make_random_password()
        new_user = User.objects.create_user(username=username, password=password, email=form.email)
        UserProfile.objects.create(user=new_user, phone=form.phone)
        return super(AddUserView, self).form_valid(form)