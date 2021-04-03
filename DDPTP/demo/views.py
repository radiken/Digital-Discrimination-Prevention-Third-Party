from django.shortcuts import render
from experiments.models import Statlog
from .forms import *
from django.http import HttpResponse
import json
import pandas as pd
from sklearn import tree
from .api import make_query

def home_view(request, *args, **kwargs):
	return render(request, "home.html", {})

def about_view(request, *args, **kwargs):
	return render(request, "about.html", {})

def demo_index_view(request, *args, **kwargs):
    if request.POST.get("accept_return")=="True":
        context = {"submission_data": request.POST}
    else:
        context = {}
    return render(request, "demo_index.html", context)

def demo_contract_view(request, *args, **kwargs):
	return render(request, "contract.html", {})

def statlog_contract_view(request, *args, **kwargs):
	return render(request, "statlog_contract.html", {})

def verification_view(request, *args, **kwargs):
	return render(request, "verification.html", {})

def individual_submission_view(request, *args, **kwargs):
    form = Statlog_submission_form()
    accept_return = False
    if request.method == 'GET':
        if request.GET.get("accept_return") == "true":
            accept_return = True
    texts = {
        'title': "A Company's Data Collection Form",
        'description': "Your data will be collected through the DDPTP, we cooperate with this company to ensure that you will be fairly treated by the company's decision-making algorithm. The information with the \"protected\" label will not be sent to the company."

    }
    context = {'form': form, 'texts': texts, 'accept_return': accept_return}
    return render(request, "submission.html", context)

def demo_api_view(request, *args, **kwargs):
	return render(request, "api.html", {})

def api_result(request, *args, **kwargs):
    if request.method == 'GET':
        query = request.GET.get("query")
        result = make_query(query)
    else:
        result= "Error! Please make query through GET method."
    return HttpResponse(json.dumps(result), content_type='application/json')

def predict(request, *args, **kwargs):
    if request.method == 'POST':
        if request.POST.get("action")=="predict":
            data = dict(request.POST)
            data.pop("action")
            data.pop("csrfmiddlewaretoken")
            for key, value in data.items():
                data[key] = value[0]
            result = statlog_prediction(data)
            result = int(result)
            if result==1:
                result = "Good costomer"
            else:
                result = "Bad costomer"
            ctx = {'result': result}
        else:
            ctx = {}
        return HttpResponse(json.dumps(ctx), content_type='application/json')
    else:
        return HttpResponse(json.dumps({}), content_type='application/json')

def statlog_prediction(data):
    x = Statlog.objects.values_list("account_status", "duration", "credit_history", "purpose", "credit_amount", "savings_account", "present_employment_since", "installment_rate_in_income", "personal_status_and_sex", 
        "guarantors", "present_residence_since", "property", "age", "other_installment_plans", "housing", "existing_credits", "job", "maintenance_provider_number", "telephone", "foreign_worker")
    y = Statlog.objects.values_list("result")

    x = pd.DataFrame(x)
    x.columns = ["account_status", "duration", "credit_history", "purpose", "credit_amount", "savings_account", "present_employment_since", "installment_rate_in_income", "personal_status_and_sex", 
        "guarantors", "present_residence_since", "property", "age", "other_installment_plans", "housing", "existing_credits", "job", "maintenance_provider_number", "telephone", "foreign_worker"]
    x = x.drop(columns=["personal_status_and_sex", "age"])
    x = x.append(data, ignore_index=True)
    one_hot_x = pd.get_dummies(x, columns=["account_status", "credit_history", "purpose", "savings_account", "present_employment_since", 
        "guarantors", "property", "other_installment_plans", "housing", "job", "telephone", "foreign_worker"])
    data = one_hot_x.iloc[-1]
    one_hot_x = one_hot_x.iloc[:-1]
    y = list(y)

    clf = tree.DecisionTreeClassifier()
    clf.fit(one_hot_x, y)
    return clf.predict([data])