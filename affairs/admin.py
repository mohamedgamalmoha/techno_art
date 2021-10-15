from django.contrib import admin
from .models import Activity, Location, Month, Day


class DayInlineAdmin(admin.TabularInline):
    model = Day
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class MonthAdmin(admin.ModelAdmin):
    inlines = (DayInlineAdmin, )


admin.site.register(Activity)
admin.site.register(Location)
admin.site.register(Month, MonthAdmin)
