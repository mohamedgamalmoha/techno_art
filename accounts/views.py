from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.backends import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic import CreateView, ListView
from django.http import HttpResponseRedirect

from .forms import RegistrationForm, UserListSearchForm


User = get_user_model()


class LogInView(SuccessMessageMixin, LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('affairs:home')
    redirect_authenticated_user = True
    success_message = 'تم نسجيل الدخول'


class RegistrationView(SuccessMessageMixin, CreateView):
    form_class = RegistrationForm
    template_name = 'accounts/registration.html'
    success_message = 'تم ادخال البيانات بطريقة صحيحة'
    success_url = reverse_lazy('affairs:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(self.success_url)


class LogOutView(SuccessMessageMixin, LogoutView):
    template_name = 'accounts/logout.html'
    success_message = 'تم نسجيل الخروج'
    success_url = reverse_lazy('affairs:home')


class UserListSearch(ListView):
    model = User
    context_object_name = 'objects'
    form_class = UserListSearchForm
    queryset = model.objects.filter(is_superuser=False)
    template_name = 'affairs/user_list.html'

    def get_form_class(self):
        return self.form_class

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class()

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        queryset = self.queryset
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                Q(email__icontains=form.cleaned_data['email']) |
                Q(username__icontains=form.cleaned_data['username']) |
                Q(first_name__icontains=form.cleaned_data['first_name']) |
                Q(last_name__icontains=form.cleaned_data['last_name'])
            )
        return queryset
