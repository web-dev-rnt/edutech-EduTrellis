"""
URL configuration for the Infinite360 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include, re_path
from django.conf import settings
from django.http import Http404
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('', include('adminpanel.urls')),
    path('', include('video_courses.url')),
    path('', include('elibrary.urls')),
]

# Paid e-library PDFs live under media/ too, but must only be reachable through the
# access-checked /pdf/<id>/view|download/ views, never by guessing the file URL.
PRIVATE_MEDIA_PREFIXES = ('elibrary/pdfs/',)


def serve_public_media(request, path, document_root=None):
    if path.lstrip('/').lower().startswith(PRIVATE_MEDIA_PREFIXES):
        raise Http404
    return serve(request, path, document_root=document_root)


# Uploaded images still need serving when DEBUG is off (there is no separate media server on this host).
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve_public_media, {'document_root': settings.MEDIA_ROOT}),
]

handler403 = 'base.views.error_403'
handler404 = 'base.views.error_404'
handler500 = 'base.views.error_500'
