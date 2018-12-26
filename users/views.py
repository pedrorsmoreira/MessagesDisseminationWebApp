from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from management.models import Buildings, Users, Messages
from math import sin, cos, sqrt, atan2, radians
from django.db.models import Count, Q
import fenixedu
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import requests
from django.utils.timezone import now


# para a cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page



import json
import os
import string

from django.db import connection
from django.conf import settings
from django.utils import timezone




client_id ='1695915081465930'
redirect_uri = 'http://127.0.0.1:8000/app/auth/'
request_url = 'https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=' + client_id + '&redirect_uri=' + redirect_uri
secret= 'XXknAbAk2nTLFdYByKqjDXVC+k94NYc5t34EUGYAxD4qaWUB+aopdY2z/9j5oRvDoTJFpaHhg42dsQ+mf6Gesg=='


def index(request):
	return render(request, './login.html')



# def login(request):
#	_buildx=Buildings.objects.get(id=2448131361155)
#	print("olaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
#	_user = Users(ist_id = 'ist000', name = 'pedro', build_id=_buildx, range_user=10,lat= -15.3888, longit=-40.777)
#	_user.save()
#	return HttpResponse('<h1>Login Page</h1>')





def login(request):
	return redirect(request_url)


def auth(request):
	
	code = request.GET.get('code')
	access_token_request_url = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'
	_data = {'client_id': client_id, 'client_secret': secret,'redirect_uri': redirect_uri, 'code': code, 'grant_type': 'authorization_code'}
	
	request_access_token = requests.post(access_token_request_url, data=_data)


	if request_access_token.status_code != 200 or 'error' in request_access_token.json():
		return render(request, './invalid.html')
	else:
		access_token = request_access_token.json().get('access_token')
		refresh_token = request_access_token.json().get('refresh_token')
		token_expires = request_access_token.json().get('expires_in')

		params = {'access_token': access_token}
		request_info = requests.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person', params=params)
		_ist_id = request_info.json().get('username')
		_name = request_info.json().get('name')


		nr={}
		nr['ist_id']=_ist_id
		nr['name']=_name
		context ={'user':nr}
		if not Users.objects.filter(ist_id=_ist_id).exists():
			_user= User(ist_id=_ist_id, name= _name)
			_user.save()
		return render(request, './userInterface.html',context)

def logout(request):
	# é para retirar isto:
	ist_id='ist425000'
	if request.method=='POST':
		print('x')
		Users.objects.filter(ist_id=ist_id).delete()
		return render(request, './GoodBye.html')







def range(request):
	if request.method == 'POST':
		# e para ir buscar a var. sessao
		ist_id='ist425412'
		_range= request.POST.get('range', '')
		Users.objects.filter(ist_id=ist_id).update(range_user = _range)
		return HttpResponse('<h1>oii/h1>')


def checkDistance(_lat1,_lat2,_long1,_long2,_range):
	R = 6373.0

	lat1 = radians(_lat1)
	lon1 = radians(_long1)
	lat2 = radians(_lat2)
	lon2 = radians(_long2)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	_distance = R * c*1000
	if _distance <_range:
		return 1
	return 0


def nearbyRange(request):
	ist_id='ist425412'
	_data= Users.objects.filter(ist_id=ist_id)
	for aux in _data:
		_range=aux.range_user
		_lat=aux.lat
		_longit=aux.longit
	# Q is to exclude the user with this ist_id
	_allUsers=Users.objects.all().filter(~Q(ist_id=ist_id))

	nearMe=[]
	for item in _allUsers:
		if checkDistance(item.lat,_lat,item.longit,_longit,_range)==1:
			print(item.ist_id)
			nearMe.append(item.ist_id)
			print('laaakjlkjlkjl')	

	print(nearMe)
	return HttpResponse('<p>olaa</p>')
	


def nearbyBuilding(request):
	ist_id='ist425412'
	_me=Users.objects.filter(ist_id=ist_id)
	for aux in _me:
		print(aux.build_id)
		_users=Users.objects.filter(build_id=aux.build_id).filter(~Q(ist_id=ist_id))
	response = serialize("json", _users)
	return HttpResponse(response, content_type = 'application/json')
	

# @login_required(login_url='users:home')
def sendMessage(request):
	ist_id='ist425412'
	if request.method == 'POST':
		_content=request.POST.get('message', '')
		_data= Users.objects.filter(ist_id=ist_id)
		for aux in _data:
			_range=aux.range_user
			_lat=aux.lat
			_longit=aux.longit
	# Q is to exclude the user with this ist_id
		_allUsers=Users.objects.all().filter(~Q(ist_id=ist_id))

		for item in _allUsers:
			if checkDistance(item.lat,_lat,item.longit,_longit,_range)==1:
				_message=Messages(content=_content,receiver=item,date=now())
				_message.save()
			
	allMessages=Messages.objects.all()
	response = serialize("json", allMessages)
	return HttpResponse(response, content_type = 'application/json')




# def login(request):
#	_buildx=Buildings.objects.get(id=2448131361155)
#	print("olaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
#	_user = Users(ist_id = 'ist000', name = 'pedro', build_id=_buildx, range_user=10,lat= -15.3888, longit=-40.777)
#	_user.save()
#	return HttpResponse('<h1>Login Page</h1>')




