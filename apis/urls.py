from django.urls import path
from . import views


urlpatterns = [
	path('', views.home, name='home'),
	path('geoapi', views.geoapi, name='geoapi'),
	path('github', views.github, name='github'),
	path('dog', views.dog, name='dog'),
]