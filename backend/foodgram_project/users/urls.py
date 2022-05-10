from django.urls import include
from django.conf.urls import url


urlpatterns = [
    url('', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
]
