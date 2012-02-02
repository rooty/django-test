from django.conf.urls.defaults import patterns, include, url


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'blog.views.main', name='home'),
    url(r"^(\d+)/$", "blog.views.post", name='viewpost'),
    url(r"^add_comment/(\d+)/$", "blog.views.add_comment"),
    url(r'^admin/', include(admin.site.urls)),
)
