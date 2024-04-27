from django.contrib import admin
from django.urls import path, include
from api.views import ArticlesModelViewSet, register
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

# Маршрутизатор DRFпо умолчанию
router = routers.DefaultRouter()
router.register(r'articles', ArticlesModelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),

    # URL для получения пары токенов JWT (access и refresh) при аутентификации
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # URL для обновления access токена с использованием refresh
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # URL для верификации токена, чтобы проверить валидность access
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # URL для регистрации новых пользователей через функцию-представление 'register'
    path('api/register/', register, name='user_register'),

]
