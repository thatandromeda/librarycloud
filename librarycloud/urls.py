from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from views import StackView

admin.autodiscover()

urlpatterns = patterns('',
	# App-specific
    url(r'^about/$',
        TemplateView.as_view(template_name='pages/about.html'),
        name="about"),
    url(r'^$', StackView.as_view(), name="home"),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
