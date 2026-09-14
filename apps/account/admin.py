from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('email','username','date_joined','last_login','is_admin','is_staff')
    search_fields = ('email','username')
    readonly_fields = ('date_joined','last_login')

    filter_horizontal =()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account,AccountAdmin) 

##counting downlaods of files

# here update 
from django.contrib import admin
# from .models import Resource


# @admin.register(Resource)
# class ResourceAdmin(admin.ModelAdmin):
#     list_display  = ('title', 'category', 'is_active', 'download_count', 'created_at')
#     list_filter   = ('category', 'is_active')          # sidebar filters
#     search_fields = ('title', 'description')           # search box
#     list_editable = ('is_active',)                     # toggle active without opening record
#     readonly_fields = ('download_count', 'created_at') # don't let admin edit these

