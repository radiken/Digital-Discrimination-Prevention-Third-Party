
from django.shortcuts import render
from .models import Individual
from .forms import *
# Create your views here.

def home_view(request, *args, **kwargs):
	my_context = {
		'my_text': 'one two three',
		'my_list': [1, 2, 3]
	}
	return render(request, "home.html", my_context)

def individual_detail_view(request):
	obj = Individual.objects.get(id=1)
	my_context = {
		'object': obj
	}
	return render(request, "individual_detail.html", my_context)
	
def individual_creation_view(request):
	# form = Individual_creation_form(request.POST or None)
	# if form.is_valid():
	# 	form.save()
	# 	form = Individual_creation_form()
    form = Submission_form()
    if request.method == "POST":
        form = Submission_form(request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        # Individual.objects.create(**form.cleaned_data)
    my_context = {'form': form}
    return render(request, "individual_creation.html", my_context)