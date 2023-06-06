from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:id>', views.home, name='home-by-user'),
    path('api/person/descendants/<int:id>', views.descendants, name='descendants-by-id'),
    path('api/person/ancestors/<int:id>', views.ancestors, name='ancestors-by-id'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
