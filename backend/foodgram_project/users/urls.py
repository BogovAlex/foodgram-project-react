from django.urls import include, path
from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from users import views

app_name = 'users'

userrouter = SimpleRouter()
userrouter.register(
    r'subscriptions',
    views.SubscriptionViewset,
    basename='subscriptions'
)


urlpatterns = [
    path('users/', include(userrouter.urls)),
    path(
        'users/',
        views.UserViewSet.as_view(
            {'get': 'list', 'post': 'create'}
        )
    ),
    path('', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
]
