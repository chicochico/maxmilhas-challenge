from django.conf.urls import url

from cpf_site.views import CheckCPF

urlpatterns = [
    url(r'^$', CheckCPF.as_view(), name='index'),
]
