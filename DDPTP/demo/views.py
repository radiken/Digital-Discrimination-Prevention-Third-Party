from django.shortcuts import render
from experiments.models import Statlog
from .forms import *
from django.http import HttpResponse
from django.db import connection
import json
import pandas as pd
from sklearn import tree
import re

def home_view(request, *args, **kwargs):
	my_context = {}
	return render(request, "home.html", my_context)

def demo_index_view(request, *args, **kwargs):
    if request.POST.get("submission"):
        context = {"submission_data": request.POST}
    else:
        context = {}
    return render(request, "demo_index.html", context)

def demo_contract_view(request, *args, **kwargs):
	my_context = {}
	return render(request, "contract.html", my_context)

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
        'description': "Your data will be collected through the DDPTP, we cooperate with this company to ensure that you will be fairly treated by the company's decision-making algorithm. The information with the \"protected\" label will not be sent to the company."
    }
    context = {'form': form, 'result': result, 'texts': texts}
    return render(request, "submission.html", context)

def demo_api_view(request, *args, **kwargs):
	my_context = {}
	return render(request, "api.html", my_context)

def api_result(request, *args, **kwargs):
    if request.method == 'GET':
        query = request.GET.get("query")
        if check_query(query, "experiments_statlog") == True:
            if "where" in query.lower():
                try:
                    condition = re.split("where", query, flags=re.IGNORECASE)[1]
                    count_query = "select count(*) from experiments_statlog where" + condition
                    if get_query_result(count_query)<10:
                        result = "Unable to return a result because the number of entries that satisfy the 'WHERE' condition is less than 10."
                        return HttpResponse(json.dumps(result), content_type='application/json')
                except:
                    result = "Invalid query! Please enter a MySQL query that returns a number with correct syntax."
                    return HttpResponse(json.dumps(result), content_type='application/json')
            try:
                result = get_query_result(query)
                result = float(result)
            except:
                result = "Invalid query! Please enter a MySQL query that returns a number with correct syntax."
        else:
            result = "Invalid query! Please refer to the rules of making queries."
    else:
        result= "Error! Please make query through GET method."
    return HttpResponse(json.dumps(result), content_type='application/json')

def check_query(query, table_name):
    lowered_query = query.lower()
    if any(keyword in lowered_query for keyword in ("limit", "join", "insert", "update", "delete", " on ")):
        return False
    if "select" and table_name in lowered_query:
        if any(keyword in lowered_query for keyword in ("count", "sum", "avg", "stddev", "variance")):
            return True
    return False

def get_query_result(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
    return float(result[0])

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
            if result==0:
                result = "bad costomer"
            else:
                result = "good costomer"
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