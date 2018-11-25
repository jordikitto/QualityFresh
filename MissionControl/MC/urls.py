from django.urls import path
from . import views

urlpatterns = [
	# ex: /MC/
    path('', views.upload_file, name='index'),
    path('export', views.export_file, name='export_file')
]