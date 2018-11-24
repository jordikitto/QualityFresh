from django.urls import path
from . import views

urlpatterns = [
	# ex: /MC/
    path('', views.upload_file, name='index'),
]