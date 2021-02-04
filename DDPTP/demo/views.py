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
    return render(request, "demo\index.html", context)

def individual_submission_view(request, *args, **kwargs):
    result = ""
    form = Submission_form()
    if request.method == "POST":
    	form = Submission_form(request.POST)
    if form.is_valid():
        plain_data = form.cleaned_data
        result = plain_data
    context = {'form': form, 'result': result}
    return render(request, "demo\submission.html", context)