from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:id>', views.home, name='home-by-user'),
    path('api/person/<int:id>', views.family_tree, name='family-tree-by-id'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
