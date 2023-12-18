from django.contrib import admin
from userauths.models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'bio')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(User, UserAdmin)