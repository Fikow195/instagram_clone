"""URL configuration for instagram_clone project."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


def home_redirect(request):
    """Redirect the root URL to the chat list."""

    return redirect('chat_list')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    path('posts/', include('posts.urls')),
    path('stories/', include('stories.urls')),
    path('', home_redirect, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
