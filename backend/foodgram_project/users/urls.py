from django.urls import include, path
from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from users import views

userrouter = SimpleRouter()
userrouter.register(
    r'subscriptions',
    views.SubscriptionViewset,
    basename='subscriptions'
)


urlpatterns = [
    path('users/', include(userrouter.urls)),
    url('', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
]