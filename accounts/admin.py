from django.contrib import admin
from .models import Profile, Sfide

#@admin.register(Profile)
#class ProfileAdmin(admin.ModelAdmin):
#    list_display = ['user', 'sfide']       #serve a visualizzare nel db admin tabella con i due campi inseriti


admin.site.register(Profile)
admin.site.register(Sfide)