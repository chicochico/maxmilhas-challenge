from django.contrib import admin
from cpf.models import CPF, CPF_Blacklist

admin.site.register(CPF)
admin.site.register(CPF_Blacklist)
