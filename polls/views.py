from django.shortcuts import render

from . models import Poll

# Create your views here.
def home(request):
	template = 'home.html'
	context_dict = {'polls': Poll.objects.all()}
	return render(request, template, context_dict)

def poll(request, id):
	pass