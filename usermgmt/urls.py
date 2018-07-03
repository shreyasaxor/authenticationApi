from django.conf.urls import url, include
from django.contrib import admin

from usermgmt.views import get_user

urlpatterns = [
                  url(r'^admin/', admin.site.urls),

                  # login and logout
                  url(r'^get-user$', view=get_user, name='get_user'),

                  ]