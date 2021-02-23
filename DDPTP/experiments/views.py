from django.shortcuts import render
from .experiments import *
from .models import Adult_original
from .models import Adult_test
from .models import Statlog
from django.db import connection
from django.http import HttpResponse
from DP_library import laplace
import json


'''
Experiment 1: prediction experiment
Test whether excluding the sensitive data affect the effectiveness of the decision making algorithm
This experiment use decision tree classifier to predict the income of individuals (the adult dataset) and the type of customers (the german dataset)
'''
def statlog_prediction():
    x = Statlog.objects.values_list("account_status", "duration", "credit_history", "purpose", "credit_amount", "savings_account", "present_employment_since", "installment_rate_in_income", "personal_status_and_sex", 
        "guarantors", "present_residence_since", "property", "age", "other_installment_plans", "housing", "existing_credits", "job", "maintenance_provider_number", "telephone", "foreign_worker")
    y = Statlog.objects.values_list("result")
    return statlog_prediction_experiment(x, y)

def adult_prediction():
    # train classifier with the original data
    test_x = Adult_test.objects.values_list("age", "workclass", "fnlwgt", "education", "education_num", "marital_status", "occupation", "relationship", "race", "sex", "capital_gain", "capital_loss", "hours_per_week", "native_country")
    test_y = Adult_test.objects.values_list("income")
    return adult_prediction_experiment(test_x, test_y)

'''
Experiment 2: differential privacy performance experiment
Test the performance of differential privacy with the above two datasets
Execute different type of queries and show the returned result and the real value
'''
def get_dp_result(query, epsilon=1):
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
    dp_result = laplace(result, 1, epsilon)
    return result, dp_result

def run_experiments(request, *args, **kwargs):
    if request.method == 'POST':
        if request.POST.get("action")=="run_e1_d1":
            original_score, processed_score = statlog_prediction()
            ctx = {'statlog_original_score': original_score, 'statlog_processed_score': processed_score}
        elif request.POST.get("action")=="run_e1_d2":
            original_score, processed_score, abstracted_score = adult_prediction()
            ctx = {'adult_original_score': original_score, 'adult_processed_score': processed_score, 'adult_abstracted_score': abstracted_score}
        else:
            ctx = {}
        return HttpResponse(json.dumps(ctx), content_type='application/json')
    else:
        return HttpResponse(json.dumps({}), content_type='application/json')


def experiments_view(request, *args, **kwargs):
    texts = {
        'e1_title' : "1. Prediction experiment",
        'e1_description' : "This experiment runs machine learning models on two real-world dataset, models for both the original data and processed data are prepared.",
        'e1_dataset1' : "Statlog (German Credit Data) Data Set",
        'e1_dataset2' : "Adult Data Set",
        'e1_dataset2_abstraction_description': "Apart from removing the sensitive data, abstraction is also an option. In this example we abstract age(young age:<=35, middle age: 36-55, older age: >=56) and relationship(husband: husband-or-wife, wife: husband-or-wife).",
        'e2_title': "2. Differential privacy experiment"
    }
    my_context = {
		'texts': texts
	}
    return render(request, "experiments.html", my_context)


# ----- save the data to the database, no longer needed once saved -----

# keys = ["age", "name", "fnlwgt", "education", "education_num", "marital_status", "occupation", "relationship", "race", "sex", "capital_gain", "capital_loss", "hours_per_week", "native_country", "income"]
# f = open('adult.test', 'r')
# for adult in f:
#     adult = adult.split(", ")
#     adult[-1] = adult[-1].rstrip().replace(".", "")
#     Adult_test.objects.create(**dict(zip(keys, adult)))
# f.close()


# keys = ["account_status", "duration", "credit_history", "purpose", "credit_amount", "savings_account", "present_employment_since", "installment_rate_in_income", "personal_status_and_sex", 
#         "guarantors", "present_residence_since", "property", "age", "other_installment_plans", "housing", "existing_credits", "job", "maintenance_provider_number", "telephone", "foreign_worker", "result"]
# f = open('german.data', 'r')
# for german in f:
#     german = german.split(" ")
#     german[-1] = german[-1].rstrip()
#     print(german)
#     Statlog.objects.create(**dict(zip(keys, german)))
# f.close()


