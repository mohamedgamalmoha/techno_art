from django.urls import path

from .views import RegistrationView, LogInView, LogOutView, UserListSearch


app_name = 'accounts'

urlpatterns = [
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('users/list/', UserListSearch.as_view(), name='list'),

]
