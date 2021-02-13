from django.shortcuts import render
from .experiments import *
from .models import Adult_original
from .models import Adult_test
from .models import Statlog


'''
Experiment 1: prediction experiment
Test whether excluding the sensitive data affect the effectiveness of the decision making algorithm
This experiment use supervised learning classifiers to predict the income of individuals
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

def prediction_experiment_view(request, *args, **kwargs):
    statlog_original_score, statlog_processed_score = statlog_prediction()
    adult_original_score, adult_processed_score = adult_prediction()
    my_context = {
		'statlog_original_score': statlog_original_score,
        'statlog_processed_score': statlog_processed_score,
        'adult_original_score': adult_original_score,
        'adult_processed_score': adult_processed_score
	}
    return render(request, "experiments\home.html", my_context)


# ----- experiment data insertion code, save the data to the database -----

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


