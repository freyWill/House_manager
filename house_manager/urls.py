from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'spending.views.home', name='home'),
    url(r'^spending/', include('spending.urls')),
    url(r'^$', include('spending.urls')),
		url(r'makeusers/', 'spending.views.createUsers', name='createUser'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login',  {'template_name': 'login.html'}, name="my_login"),
		#  the next_page argument just sends you to the homepage after you log in, otherwise you get the default django login auth
		url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name="logout")
)
