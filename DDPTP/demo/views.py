from django.shortcuts import render
from experiments.models import Adult_original
from experiments.models import Adult_test
from .forms import *
from django.http import HttpResponse
import json

def home_view(request, *args, **kwargs):
	my_context = {}
	return render(request, "home.html", my_context)

def demo_index_view(request, *args, **kwargs):
    if request.POST.get("submission"):
        context = {"submission_data": request.POST}
    elif request.POST.get("run_algorithm"):
        # remove irrelevant data from the dict
        data = dict(request.POST)
        data.pop('csrfmiddlewaretoken', None)
        data.pop('run_algorithm', None)
        
        # TODO: run model to get real result
        result = "<50k"
        context = {"result": result, "submission_data": data}
    else:
        context = {}
    return render(request, "demo_index.html", context)

def individual_submission_view(request, *args, **kwargs):
    result = ""
    form = Statlog_submission_form()
    if request.method == "POST":
    	form = Statlog_submission_form(request.POST)
    if form.is_valid():
        plain_data = form.cleaned_data
        result = plain_data
    texts = {
        'title': "A Company's Data Collection Form",
        'description': "Your data will be collected through the DDPTP, we coperate with this company to ensure that you will be fairly treated by the company's decision-making algorithm. The information with the \"protected\" label will not be sent to the company."
    }
    context = {'form': form, 'result': result, 'texts': texts}
    return render(request, "submission.html", context)

def predict(request, *args, **kwargs):
    # TODO
    if request.method == 'POST':
        if request.POST.get("action")=="run_e1_d1":
            original_score, processed_score = statlog_prediction()
            ctx = {'statlog_original_score': original_score, 'statlog_processed_score': processed_score}
        else:
            ctx = {}
        return HttpResponse(json.dumps(ctx), content_type='application/json')
    else:
        return HttpResponse(json.dumps({}), content_type='application/json')