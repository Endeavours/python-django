import mobile_v1
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'login/$', 'rest_framework.authtoken.views.obtain_auth_token', name='login'),
)