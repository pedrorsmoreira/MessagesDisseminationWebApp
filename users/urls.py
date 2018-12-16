from django.urls import path
from . import views
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
	path('', csrf_exempt(views.index), name = 'home'),
	path('auth/', csrf_exempt(views.auth), name = 'auth'),
	#path('<str:ist_id>/messages/', csrf_exempt(views.messages), name = 'messages'),
    path('<str:ist_id>/range/', csrf_exempt(views.range), name = 'range'),
    path('<str:ist_id>/nearby/range/', csrf_exempt(views.nearbyRange), name = 'nearbyRange'),
    path('<str:ist_id>/nearby/building/', csrf_exempt(views.nearbyBuilding), name = 'nearbyBuilding'),
    ]





	




