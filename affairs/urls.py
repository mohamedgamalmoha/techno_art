from django.urls import path

from .views import home, MonthCreate


app_name = 'affairs'

urlpatterns = [
    path('', home, name='home'),
    path('create/month', MonthCreate.as_view(), name='create_month'),
]
