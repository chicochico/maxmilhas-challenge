from django.contrib import admin
from cpf.models import CPF, CPFBlacklist


class CPFBlacklistAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'added_on')
    readonly_fields = ('added_on',)

admin.site.register(CPF)
admin.site.register(CPFBlacklist, CPFBlacklistAdmin)
