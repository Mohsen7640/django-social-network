from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


from config import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('account/', include('account.urls', namespace='account')),
    path('post/', include('post.urls', namespace='post')),
    
    path('', views.home_view, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
