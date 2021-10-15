from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from affairs.models import Month


class MonthUserInlineAdmin(admin.TabularInline):
    model = Month
    show_change_link = True
    fields = ('user', 'activity', 'month')


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_name', 'is_staff')
    readonly_fields = ('password', 'last_login', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    inlines = (MonthUserInlineAdmin, )
    sortable_by = ('date_of_creation', )
    ordering = ('-date_joined', )

    def get_name(self, obj):
        return obj.get_full_name() or 'لا يوجد'

    def get_fieldsets(self, request, obj=None):
        a = list(super(CustomUserAdmin, self).get_fieldsets(request, obj))
        if obj:
            a.append(('تفاصيل الاقامة',
                      {'fields': ('nationality', 'basic_salary',
                                  ('feeding_allowance', 'housing_allowance', 'transporting_allowance'),
                                  'passport_number', 'expiration_date')
                       }))
        return tuple(a)

    def get_inlines(self, request, obj):
        lst = super(CustomUserAdmin, self).get_inlines(request, obj)
        return lst if obj else []

    def get_readonly_fields(self, request, obj=None):
        fields = super(UserAdmin, self).get_readonly_fields(request, obj)
        return fields if obj else []

    get_name.short_description = 'الاسم'


admin.site.register(User, CustomUserAdmin)
