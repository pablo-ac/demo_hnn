from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import loader, Context, Template
import xml.etree.ElementTree as ET
import os 

def index(request):
	template = loader.get_template('index.html')
	return HttpResponse(template.render(None), content_type="text/html")

@csrf_exempt
def run_neural_model(request):
	rate = request.POST["rate"]
	start = request.POST["start"]
	os.system('cd demo')
	os.system('C:\Python27\python model.py '+rate+" "+start)
	os.system('mv *png demo\static\img')
	return HttpResponse("OK", content_type="text/plain")
