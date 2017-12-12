from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from api.views import CPFBlacklistViewSet, server_status


schema_view = get_swagger_view(title='CPF Blacklist API')
router = routers.DefaultRouter()
router.register(r'cpf-blacklist', CPFBlacklistViewSet, 'blacklist')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^docs/', schema_view, name='docs'),
    url(r'^server-status', server_status, name='server-status'),
]
