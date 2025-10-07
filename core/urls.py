from django.urls import path

from .views import IndexView

# Pag. principal
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]