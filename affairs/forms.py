from django import forms
from django.contrib.auth.backends import get_user_model

from .models import Month, Day


User = get_user_model()


class MonthAddForm(forms.ModelForm):
    user = forms.ModelChoiceField(User.objects.filter(is_superuser=False))

    class Meta:
        model = Month
        fields = ('user', 'activity', 'month')

    def clean(self,):
        user = self.cleaned_data.get('user')
        activity = self.cleaned_data.get('activity')
        month = self.cleaned_data.get('month')
        year = self.cleaned_data.get('year')
        print(year)
        if Month.objects.filter(user=user, activity=activity, month=month).exists():
            raise forms.ValidationError('هذا المستخدم لديه جدول مسجل بالفعل لهذا الشهر')


class DayFormSet(forms.BaseModelFormSet):
    class Meta:
        model = Month
        fields = ('user', 'activity', 'month')
