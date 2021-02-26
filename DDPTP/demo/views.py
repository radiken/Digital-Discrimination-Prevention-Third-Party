from django.shortcuts import render
from experiments.models import Adult_original
from experiments.models import Adult_test
from .forms import Submission_form
from DP_library import laplace
from .calculation import *

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
    form = Submission_form()
    if request.method == "POST":
    	form = Submission_form(request.POST)
    if form.is_valid():
        plain_data = form.cleaned_data
        result = plain_data
    texts = {
        'title': "A Company's Data Collection Form",
        'description': "Your data will be collected through the DDPTP, we coperate with this company to ensure that you will be fairly treated by the company's decision-making algorithm. The information with the \"protected\" label will not be sent to the company."
    }
    context = {'form': form, 'result': result, 'texts': texts}
    return render(request, "submission.html", context)