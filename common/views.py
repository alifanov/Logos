# coding: utf-8
from django.contrib import messages
from django.views.generic import TemplateView, FormView, View, ListView, DetailView
from common.forms import NewUserForm, ImageForm, UpdateProfileForm, UpdateUserForm
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from pytils.translit import slugify
from django.http import HttpResponse, HttpResponseRedirect
from common.models import UserProfile, Competence, BusinessType, UserTag
from django.db.models import Q
from django.template.loader import get_template
from django.template import Context
from django.core.mail import send_mail
from django.conf import settings

class LoginView(TemplateView):
    template_name='login.html'
    errors = u''

    def get_context_data(self, **kwargs):
        ctx = super(LoginView, self).get_context_data(**kwargs)
        ctx['errors'] = self.errors
        return ctx

    def post(self, request, *args, **kwargs):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                self.errors = u'Пользователь не активирован'
        else:
            self.errors = u'Нет пользователя в системе с такими логином и паролем'
        return self.get(request, *args, **kwargs)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

# Create your views here.
class GetAccessView(TemplateView):
    template_name = 'get-access.html'
    errors = u''
    activated = False

    def get_context_data(self, **kwargs):
        ctx = super(GetAccessView, self).get_context_data(**kwargs)
        ctx['activated'] = self.activated
        ctx['errors'] = self.errors
        return ctx

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        if email:
            print email
            if User.objects.filter(email=email, is_active=False).count() == 0:
                self.errors = u'В базе нет неактивных пользователей с таким email'
            else:
                user = User.objects.get(email=email, is_active=False)
                user.is_active=True
                newpassword = User.objects.make_random_password()
                user.set_password(newpassword)
                user.save()
                self.activated = True
                # send_email
                plaintxt = get_template('email/get_access_email.txt')
                c = Context({'username': user.username, 'password': newpassword})
                txt = plaintxt.render(c)
                send_mail(u'Данные для входа в систему', txt, settings.DEFAULT_FROM_EMAIL, [user.email])
        else:
            self.errors = u'Введите email'
        return self.get(request, *args, **kwargs)

class HomeView(ListView):
    template_name = 'contacts.html'
    search_query = u''
    btypes = u''
    competences = u''
    tags = u''
    qd = u''
    paginate_by = 2
    model = User
    context_object_name = 'users'

    def get_queryset(self):
        self.users = User.objects.exclude(first_name__exact='', last_name__exact='')
        if self.request.GET.get('competences'):
            self.competences = self.request.GET.get('competences')
            self.users = self.users.filter(profile__competences__slug=self.competences)
        if self.request.GET.get('btypes'):
            self.btypes = self.request.GET.get('btypes')
            self.users = self.users.filter(profile__bTypes__slug=self.btypes)
        if self.request.GET.get('tags'):
            self.tags = self.request.GET.get('tags')
            self.users = self.users.filter(tags__slug=self.tags)
        if self.request.GET.get('search_query'):
            self.search_query = self.request.GET.get('search_query')
            s = self.search_query
            f = Q(tags__slug__istartswith=s)|Q(tags__name__istartswith=s)
            f |= Q(profile__bTypes__slug__istartswith=s)|Q(profile__bTypes__name__istartswith=s)
            f |= Q(profile__competences__slug__istartswith=s)|Q(profile__competences__name__istartswith=s)
            f |= Q(first_name__istartswith=s)|Q(last_name__istartswith=s)
            self.users = self.users.filter(f)
        return self.users

    def get(self, request, *args, **kwargs):
        if request.GET.get('type') == 'reset':
            return HttpResponseRedirect('/')
        else:
            self.qd = request.GET.copy()
            if 'page' in self.qd:
                del self.qd['page']
            self.qd = self.qd.urlencode()
            if self.qd: self.qd = '?'+self.qd
            return super(HomeView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)
        ctx['main_active_link'] = True
        ctx['page_suffix'] = '&page=' if self.search_query or self.tags or self.btypes or self.tags else '?page='
        ctx['active_search_query'] = self.search_query
        ctx['active_tags'] = self.tags
        ctx['active_btypes'] = self.btypes
        ctx['active_competences'] = self.competences
        ctx['query_dict'] = self.qd
        ctx['tags'] = UserTag.objects.all()
        ctx['btypes'] = BusinessType.objects.all()
        ctx['competences'] = Competence.objects.all()
        return ctx

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
    success_url = '/user/add/'

    def form_invalid(self, form):
        return super(AddUserView, self).form_invalid(form)

    def form_valid(self, form):
        username = u'username{}'.format(User.objects.count()+1)
        password = User.objects.make_random_password()
        first_name = form.cleaned_data['firstname']
        last_name = form.cleaned_data['lastname']
        phone = form.cleaned_data['phone']
        new_user = User.objects.create_user(
            username=username,
            password=password,
            email=form.cleaned_data['email'],
            first_name = first_name,
            last_name = last_name
        )
        for tag_name in form.cleaned_data['tags']:
            tag = UserTag.objects.get(name=tag_name)
            tag.author=self.request.user
            tag.target = new_user
            tag.save()

        new_user_profile = UserProfile.objects.create(
            user=new_user,
            phone=form.cleaned_data['phone']
        )

        for name in form.cleaned_data['businesstypes']:
            btype = BusinessType.objects.get(name=name)
            new_user_profile.bTypes.add(btype)
        for name in form.cleaned_data['competences']:
            comp = Competence.objects.get(name=name)
            new_user_profile.competences.add(comp)
        imageForm = ImageForm(self.request.POST, self.request.FILES, instance=new_user_profile)
        imageForm.save()
        new_user_profile.save()
        ctx = self.get_context_data()
        ctx['added'] = True
        return self.render_to_response(ctx)

    def get_context_data(self, **kwargs):
        ctx = super(AddUserView, self).get_context_data(**kwargs)
        ctx['add_active_link'] = True
        return ctx

class UserDetailView(DetailView):
    model = User
    template_name = 'user-detail.html'
    context_object_name = 'usr'


    def get_object(self, queryset=None):
        return User.objects.get(username=self.kwargs['username'])

class PersonalView(TemplateView):
    template_name = 'personal.html'
    message = u''

    def post(self, request, *args, **kwargs):
        if request.POST.get('send_password'):
            newpassword = User.objects.make_random_password()
            request.user.set_password(newpassword)
            request.user.save()
            plaintxt = get_template('email/get_access_email.txt')
            c = Context({'username': request.user.username, 'password': newpassword})
            txt = plaintxt.render(c)
            self.message = u'Пароль отправлен'
            send_mail(u'Данные для входа в систему', txt, settings.DEFAULT_FROM_EMAIL, [request.user.email])
        else:
            userForm = UpdateUserForm(request.POST, request.FILES, instance=request.user)
            if userForm.is_valid():
                userForm.save()
            profileForm = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if profileForm.is_valid():
                profileForm.save()
                self.message = u'Данные сохранены'
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(PersonalView, self).get_context_data(**kwargs)
        print dir(self.request.user)
        form = UpdateProfileForm(instance=self.request.user.profile)
        userForm = UpdateUserForm(instance=self.request.user)
        ctx['updateForm'] = form
        ctx['userForm'] = userForm
        ctx['message'] = self.message
        return ctx