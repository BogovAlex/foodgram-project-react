from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users import views

usersrouter = DefaultRouter()
usersrouter.register(
    r'users',
    views.UsersViewset,
    basename='users'
)


urlpatterns = [
    path('', include(usersrouter.urls))
]
