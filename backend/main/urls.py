from django.urls import include, path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'messages', views.MessagesAPI, 'MessagesAPI')
router.register(r'tokens', views.TokensAPI, 'TokensAPI')
urlpatterns = [
    path('', views.index, name='index'),
    path('create/token', views.token, name='token'),
    path('registration/', views.registration, name='registration'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
]
