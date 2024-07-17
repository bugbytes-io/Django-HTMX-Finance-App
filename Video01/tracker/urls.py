from django.urls import path
from tracker import views


urlpatterns = [
    path("", views.index, name='index'),
]
