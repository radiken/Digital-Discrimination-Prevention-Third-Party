from django.shortcuts import render
import experiments.experiments
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

def get_query_result(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
    return float(result[0])

def get_statlog_avg_age(count = None, new_entry_age = None):
    # in the german dataset, simulate the queries for age
    if not count:
        count = Statlog.objects.count()
        avg_query = "SELECT AVG(age) FROM experiments_statlog"
    else:
        avg_query = f"SELECT AVG(experiments_statlog.age) FROM (SELECT experiments_statlog.age from experiments_statlog LIMIT {count}) experiments_statlog"
    original_result = get_query_result(avg_query)
    if new_entry_age:
        original_result = ((original_result*count)+new_entry_age)/(count+1)
        count = count+1
    dp_result = get_dp_result(original_result)
    return count, original_result, dp_result

def get_statlog_single_male_count(new_entry = None):
    # single male corespond to A93 in the data set
    single_male_query = "SELECT COUNT(*) FROM experiments_statlog WHERE personal_status_and_sex='A93'"
    original_result = get_query_result(single_male_query)
    if new_entry==1:
        original_result = original_result + 1
    dp_result = get_dp_result(original_result)
    return original_result, dp_result

def simulate_new_entry_guess_n_times(n, real_result, epsilon=1):
    correct_count = 0
    new_result = real_result+1
    for _ in range(n):
        new_dp_result = get_dp_result(new_result, epsilon=epsilon)
        if new_dp_result > real_result:
            correct_count = correct_count + 1
    return correct_count/n

'''
Experiment 3: Verification experiment
try to see if we can verify the fairness of the decision-making algorithms
By looking at the distribution of the sensitive information in the returned classifications
'''
def get_adult_models_sensitive_rates_from_experiments():
    test_x = Adult_test.objects.values_list("age", "workclass", "fnlwgt", "education", "education_num", "marital_status", "occupation", "relationship", "race", "sex", "capital_gain", "capital_loss", "hours_per_week", "native_country")
    original_zero_rates, original_one_rates, processed_zero_rates, processed_one_rates, abstracted_zero_rates, abstracted_one_rates = get_adult_models_sensitive_rates(test_x)
    rates_list = [original_zero_rates, original_one_rates, processed_zero_rates, processed_one_rates, abstracted_zero_rates, abstracted_one_rates]
    for rates in rates_list:
        for key, value in rates.items():
            value_string = ""
            for attribute, rate in value.items():
                if(rate!=0):
                    value_string = value_string+attribute+": "+str(rate)+"\n"
            rates[key] = value_string
    return rates_list

def get_statlog_models_sensitive_rates_from_experiments():
    x = Statlog.objects.values_list("account_status", "duration", "credit_history", "purpose", "credit_amount", "savings_account", "present_employment_since", "installment_rate_in_income", "personal_status_and_sex", 
        "guarantors", "present_residence_since", "property", "age", "other_installment_plans", "housing", "existing_credits", "job", "maintenance_provider_number", "telephone", "foreign_worker")
    y = Statlog.objects.values_list("result")
    original_zero_rates, original_one_rates, processed_zero_rates, processed_one_rates = get_statlog_models_sensitive_rates(x, y)
    rates_list = [original_zero_rates, original_one_rates, processed_zero_rates, processed_one_rates]
    rates_list_string = []
    for rates in rates_list:
        rates_string = ""
        for attribute, rate in rates.items():
            rates_string = rates_string+attribute+": "+str(rate)+", "
        rates_list_string.append(rates_string)
    return rates_list_string


def run_experiments(request, *args, **kwargs):
    if request.method == 'POST':
        if request.POST.get("action")=="run_e1_d1":
            original_score, processed_score = statlog_prediction()
            ctx = {'statlog_original_score': original_score, 'statlog_processed_score': processed_score}
        elif request.POST.get("action")=="run_e1_d2":
            original_score, processed_score, abstracted_score = adult_prediction()
            ctx = {'adult_original_score': original_score, 'adult_processed_score': processed_score, 'adult_abstracted_score': abstracted_score}
        elif request.POST.get("action")=="run_e2_t1_q1":
            count, original_result, dp_result = get_statlog_avg_age()
            ctx = {'count': count, 'original_result': original_result, 'dp_result': dp_result}
        elif request.POST.get("action")=="run_e2_t1_q2":
            count, original_result, dp_result = get_statlog_avg_age(new_entry_age=25)
            ctx = {'count': count, 'original_result': original_result, 'dp_result': dp_result}
        elif request.POST.get("action")=="run_e2_t1_q3":
            count, original_result, dp_result = get_statlog_avg_age(count=10)
            ctx = {'count': count, 'original_result': original_result, 'dp_result': dp_result}
        elif request.POST.get("action")=="run_e2_t1_q4":
            count, original_result, dp_result = get_statlog_avg_age(count=10, new_entry_age=25)
            ctx = {'count': count, 'original_result': original_result, 'dp_result': dp_result}
        elif request.POST.get("action")=="run_e2_t1_q5":
            original_result, dp_result = get_statlog_single_male_count()
            ctx = {'original_result': original_result, 'dp_result': dp_result}
        elif request.POST.get("action")=="run_e2_t1_q6":
            original_result, dp_result = get_statlog_single_male_count(new_entry = 1)
            ctx = {'original_result': original_result, 'dp_result': dp_result}
        elif request.POST.get("action")=="run_e2_t1_c6":
            correct_rate = simulate_new_entry_guess_n_times(1000, int(request.POST.get("real_result")))
            ctx = {'correct_rate': correct_rate}
        elif request.POST.get("action")=="run_e2_t1_c7":
            correct_rate = simulate_new_entry_guess_n_times(1000, int(request.POST.get("real_result")), epsilon=0.5)
            ctx = {'correct_rate': correct_rate}
        elif request.POST.get("action")=="run_e2_t2_c1":
            noise_sum = get_noise_n_times(100000, epsilon=1)
            ctx = {'noise_sum': noise_sum}
        elif request.POST.get("action")=="run_e2_t2_c2":
            noise_sum = get_noise_n_times(100000, epsilon=2)
            ctx = {'noise_sum': noise_sum}
        elif request.POST.get("action")=="run_e3_t1":
            rates_list = get_adult_models_sensitive_rates_from_experiments()
            ctx = {"original_zero_rates": rates_list[0], "original_one_rates": rates_list[1], "processed_zero_rates": rates_list[2], "processed_one_rates": rates_list[3], "abstracted_zero_rates": rates_list[4], "abstracted_one_rates": rates_list[5]}
        elif request.POST.get("action")=="run_e3_t2":
            rates_list = get_statlog_models_sensitive_rates_from_experiments()
            ctx = {"original_zero_rates": rates_list[0], "original_one_rates": rates_list[1], "processed_zero_rates": rates_list[2], "processed_one_rates": rates_list[3]}
        else:
            ctx = {}
        return HttpResponse(json.dumps(ctx), content_type='application/json')
    else:
        return HttpResponse(json.dumps({}), content_type='application/json')


def experiments_view(request, *args, **kwargs):
    texts = {
        'e1_title' : "1. Prediction experiment",
        'e1_description' : "This experiment aims to prove that classifiers can have good performance without some sensitive input. We observe the result by controlling the inputs of decision tree classifiers on two real-world data sets.",
        'e1_dataset1' : "Statlog (German Credit Data) Data Set",
        'e1_d1_description1': "Predict the test set with model that use all the information from inputs:",
        'e1_d1_description2': "Take out the information of \"age\", \"marital status and sex\":",
        'e1_dataset2' : "Adult Data Set",
        'e1_d2_description1': "Predict the test set with model that use all the information as inputs:",
        'e1_d2_description2': "Take out the information of \"sex\" \"race\", \"native country\" and \"marital status\" from inputs:",
        'e1_dataset2_abstraction_description': "Apart from removing the sensitive data, abstraction is also an option. In this example, abstract age(young age:<=35, middle age: 36-55, older age: >=56) and relationship(husband: husband-or-wife, wife: husband-or-wife), predict the test set again:",
        'e2_title': "2. Differential privacy experiment",
        'e2_description': "This experiment demostrate the performance of adding noise to the results of numeric queries. Results of this experiment proves it is save to provide an API to the organization end to query information about the sensitive data.",
        'e2_charts_title': "Premise",
        'e2_charts_description': '''Differential privacy is a tradeoff between privacy level(noise level) and data availability. The larger the noise is, the less accurate and meaningful the data is. 
                                This application applies the laplace machanism, where the noise distribution obeys the laplace distribution as shown on the left below. We do not modify mu, hence we only look at the first three zero-centred line. 
                                beta equals sensitivity/epsilon, under the definition of the laplace mechanism, sensitivity represents the change that a single entry can bring to the result. In this app, sensitivity is always set to 1, since in most case it satisfies the definition,
                                moreover, it is sufficient and easier to control beta only through epsilon. Therefore, in this app, noise level equals to 1/epsilon. Thereby the chart on the right can be drawn showing the relationship between epsilon (x axis) and noise level (y axis).
                                There is no standard about what noise level is too much, by intuition, this application considers epsilon=0.5, noise level=2 as the largest acceptable noise level (coresponds to the green line one the left).  ''',
        'e2_t1_title': "Test 1: Single query privacy level test",
        'e2_t1_subtitle1': "continuous return queries in a large data set",
        'e2_t1_description': "While providing an API to access certain level of the sensitive information, it is vital to ensure the result of the queries have high enough privacy level against differential attack.",
        'e2_t1_q1_description': "In the Statlog (German Credit Data) Data Set, we regard age as a sensitive information. Suppose the organization queries the average age.",
        'e2_t1_q2_description': "Now suppose there is a new entry of age 25, query the value again.",
        'e2_t1_description2': "Without differential privacy, the age of the new entry can be easily computed using the real values:",
        'e2_t1_description3': "Compute this with the processed values again:",
        'e2_t1_subtitle2': "continuous return queries in a small data set",
        'e2_t1_q3_description': "Differential privacy works well with data set of 1000 entries, now consider a smaller data set. Only take the first 10 entries of the Statlog (German Credit Data) Data Set:",
        'e2_t1_q4_description': "add 11th entry with age 25 and run the query again:",
        'e2_t1_subtitle3': "\"How many\" queries:",
        'e2_t1_q5_description': "This part tests the performance of differential privacy with queries that ask \"how many...\" questions, in this case the size of the data set does not matter, because no computation is necessary where the new entry can only affect the result by 0 or 1. Suppose the organization is querying the number of single male in the data set:",
        'e2_t1_q6_description': "Suppose another entries comes in that satisfy the requirement (he is a single male):",
        'e2_t1_description4': "Base on the mechanism of laplace differential privacy, the best guess one can do is: if the second result is larger than the first result, the new entry satisfies the requirement, else it doesn't. Try to make a guess:",
        'e2_t1_description5': "Now with the information of the processed result, test the winning rate by running the above guess 1000 times:",
        'e2_t1_description6': "The above computation use epsilon=1, choosing a smaller epsilon will increase the noise, run the test again with epsilon=0.5:",
        'e2_t2_title': "Test 2: Multiple queries privacy level test",
        'e2_t2_description': "So far, individual's privacy seems to be safe, but there is one more things to test. The laplace machenism in differential privacy means the noise follows a laplace distribution, which means the expected noise is 0. If one makes the same queries many times, it is expected to have 0 noise when calculating the average.",
        'e2_t2_c1_description': "Run the differential privacy algorithm 100,000 times with epsilon=1 (applies in continuous return queries), only takes the noise and sum them up:",
        'e2_t2_c2_description': "Run 100,000 times with epsilon=2 (applies in \"how many\" question queries):",
        'e2_t2_conclusion': "It seems in reality this is not a problem.",
        'e3_title': "3. Verification experiment",
        'e3_description': "This application attempts to verify the fairness of the decision-making algorithms by observing the distribution of the sensitive information in the classification result. The intuition is, if too many entries with the same sensitive attribute are classified to a same catogory, the algorithm is suspected to have the knowledge of that sensitive information.",
        'e3_t1_title': "Test 1: sensitive data's distribution of the adult data set classifications",
        'e3_t1_description': "In experiment 1, three models were used to predict the test set of the adult data set: the original model that use all information (model 1), the processed model that removed some attributes (model 2), and the abstracted model that abstracted two features in addition to the processed model (model 3). This test compare the sensitive information distribution of the classifications of these models.",
        'e3_t2_title': "Test 2: sensitive data's distribution of the Statlog (German credit data) set classifications",
        'e3_t2_description': '''Similarly, in experiment 1, two models were used to predict the test set of the German data set: the original model that use all information (model 1), the processed model that removed some attributes (model 2). This test compare the sensitive information distribution of the classifications of two models. 
                            Note: A91 : male, divorced/separated; A92 : female, divorced/separated/married; A93 : male, single; A94 : male, married/widowed; A95 : female, single''',
    }
    figures = epsilon_and_noise_level_chart_figures()
    figures.insert(0, ["epsilon", "noise level"])
    my_context = {
		'texts': texts,
        'epsilon_and_noise': figures
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


