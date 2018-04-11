from django.conf.urls import url
from .views import home
from .api import WebsiteList

urlpatterns = [
    url(r'^$', home, name="home"),
    url(r'^api/getWebsiteList/$', WebsiteList.as_view(),
        name="website_list"),
]
