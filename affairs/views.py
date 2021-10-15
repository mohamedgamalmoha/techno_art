from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.backends import get_user_model

from .models import Month
from .forms import MonthAddForm


User = get_user_model()


def home(request):
    return render(request, 'home.html')


class MonthCreate(CreateView):
    model = Month
    form_class = MonthAddForm
    template_name = 'affairs/month_create.html'
    success_url = '/'
