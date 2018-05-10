from django.shortcuts import render
import requests
from django.conf import settings


# Create your views here.
def home(request):
	return render(request, 'apis/home.html')

def geoapi(request):
	is_cached = ('geodata' in request.session)

	if not is_cached:
		ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '')
		response = requests.get('http://freegeoip.net/json/{}'.format(ip_address))
		request.session['geodata'] = response.json()

	geodata = request.session['geodata']

	return render(request, 'apis/geoapi.html', {
		'ip': geodata['ip'],
		'country': geodata['country_name'],
		'latitude': geodata['latitude'],
		'longitude': geodata['longitude'],
		'api_key': settings.GOOGLE_MAPS_API_KEY,
		'is_cached': is_cached,
	})

def github(request):
	search_result = {}
	if 'username' in request.GET:
		username = request.GET['username']
		url = 'https://api.github.com/users/{}'.format(username)
		response = requests.get(url)
		search_result_success = (response.status_code == 200)
		search_result = response.json()
		search_result['success'] = search_result_success
		search_result['rate'] = {
			'limit': response.headers['X-RateLimit-Limit'],
			'remaining': response.headers['X-RateLimit-Remaining'],
		}
	return render(request, 'apis/github.html', {'search_result': search_result})


def dog(request):
	url = 'https://random.dog/woof.json'
	response = requests.get(url)
	img = response.json()
	img['mp4'] = (img['url'].endswith('.mp4'))
	return render(request, 'apis/dog.html', {'img': img})
