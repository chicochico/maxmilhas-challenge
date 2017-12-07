from django.contrib import admin
from cpf.models import CPF, CPFBlacklist

admin.site.register(CPF)
admin.site.register(CPFBlacklist)
