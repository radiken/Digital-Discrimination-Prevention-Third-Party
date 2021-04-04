from django.shortcuts import render
import experiments.experiments
from .experiments import *
from .models import Adult_test
from .models import Statlog
from django.db import connection
from django.http import HttpResponse
from DP_library import laplace
import json

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

def run_experiments(request, *args, **kwargs):
    if request.method == 'POST':
        if request.POST.get("action")=="run_e1_d1":
            metrics = customize_statlog_predition("decision_tree", {"age": "remove", "personal_status_and_sex": "remove"})
            ctx = {'metrics': metrics}
        elif request.POST.get("action")=="run_e1_d2":
            # abstract age(young age:<=35, middle age: 36-55, older age: >=56) and relationship(husband: husband-or-wife, wife: husband-or-wife) and remove gender, race, native country and marital status
            age_abstract = {"young_age": "<=35", "middle_age": " in range(36, 56)", "older_age": ">=56"}
            relationship_abstract = {"Husband-or-wife": ["Husband", "Wife"]}
            actions = {"marital_status": "remove", "race": "remove", "sex": "remove", "native_country": "remove", "age": age_abstract, "relationship": relationship_abstract}
            metrics = adult_prediction(actions)
            ctx = {'metrics': metrics}
        elif request.POST.get("action")=="run_e1_d2_improvement":
            correlations = adult_correlations()
            correlations = correlations.to_json(orient="split")
            ctx = {'correlations': correlations}
        elif request.POST.get("action")=="run_e1_d2_improved":
            occupation_abstract = {"group_1": ["Adm-clerical", "Craft-repair"]}
            actions = {"marital_status": "remove", "race": "remove", "sex": "remove", "occupation": occupation_abstract, "relationship": "remove"}
            metrics = adult_prediction(actions)
            ctx = {'metrics': metrics}
        elif request.POST.get("action")=="run_e1_d2_customize":
            classifier = request.POST.get("classifier")
            actions = json.loads(request.POST.get("actions"))
            metrics = customize_statlog_predition(classifier, actions)
            ctx = {'metrics': metrics}
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
            noise_sum = get_noise_n_times(100000, epsilon=0.5)
            ctx = {'noise_sum': noise_sum}
        elif request.POST.get("action")=="run_e2_t2_customize":
            noise_sum = get_noise_n_times(100000, epsilon=float(request.POST.get("epsilon")))
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
        'e1_title' : "Discrimination Experiments",
        'e1_description' : "Data set used in these experiments: the Adult Data Set (https://archive.ics.uci.edu/ml/datasets/adult) and the Statlog (German Credit Data) Data Set (https://archive.ics.uci.edu/ml/datasets/statlog+(german+credit+data)).",
        'e1_introduction_description': '''The model prevents discrimination by removing or abstracting input data of decision-making algorithms, as it requires no access to the training data set. The DDP app controls what data is sent to organizations so that organizations can only train their algorithms with the given attributes.
                                        The discrimination experiments aims to prove that imposing restrictions on the inputs indeed helps to reduce or prevent discrimination. To achieve so, four metrics are used to measure the discrimination level of a algorithm (More information about the metrics refers to: https://aif360.mybluemix.net/).''',
        'e1_introduction_m1_description': "1. Statistical Parity Difference: Computed as the difference of the rate of favorable outcomes received by the unprivileged group to the privileged group. The ideal value is 0, the acceptable range is -0.1 to 1.",
        'e1_introduction_m2_description': "2. Equal Opportunity Difference: The difference of true positive rates between the unprivileged and the privileged groups. The ideal value is 0, the acceptable range is -0.1 to 1.",
        'e1_introduction_m3_description': "3. Computed as average difference of false positive rate (false positives / negatives) and true positive rate (true positives / positives) between unprivileged and privileged groups. The ideal value is 0, the acceptable range is -0.1 to 1.",
        'e1_introduction_m4_description': "4. Disparate Impact: Computed as average difference of false positive rate (false positives / negatives) and true positive rate (true positives / positives) between unprivileged and privileged groups. The ideal value is 1, the acceptable range is 0.8 to 1.25.",
        'e1_dataset1' : "Statlog (German Credit Data) Data Set",
        'e1_d1_description': "This experiment compares an original machine learning that use all the information of the German Credit Data Set as input and a processed model that removes age, personal status and sex to protect these two sensitive attributes.",
        'e1_dataset2' : "Adult Data Set",
        'e1_d2_description': '''This experiment compares an original machine learning that use all the information of the Adult Data Set as input and a processed model that removes marital status, race, sex, native country and abstracts abstract age (young age:<=35, middle age: 36-55, older age: >=56) and relationship (husband: husband-or-wife, wife: husband-or-wife).
                             The sensitive attributes are sex and race. But in order to protect sex and race, the processed model processes other attributes that are potential sensitive attributes, from which sex and race could potentially be inferred by the algorithm. At this step the proxy variables are selected manually.''',
        'e1_d2_improvement_description': "The the processed model does not seems to be effective. In this situation, the model will calculate the correlations among the sensitive values and other attributes according to the existing data to seek better solutions.",
        'e1_d2_improvement_description2': "From the correlations, we observe the followings. Except for 'husband' and 'wife', other relationship attributes shows high corraltions as well, therefore, it is better to be removed. Two occupation values have over 0.2 correlations, abstract these two values to a group may also help. The correlation between the sensitive attributes and age is not high, therefore it is not necessary to abstract age. Make changes accordingly and run again:",
        'e1_d2_customize_description': "Remove or abstract any attributes you want. \nAt the moment, you can abstract continuous attribute to 2 groups and discrete attribute to 3 groups.",
        'e1_d2_customize_s3_description': "Note: The decision tree classifier involves randomness, result may be different each time.",
        'e2_title': "Privacy Experiments",
        'e2_description': "Data set used in these experiments: The Statlog (German Credit Data) Data Set (https://archive.ics.uci.edu/ml/datasets/statlog+(german+credit+data)).",
        'e2_charts_description': '''While the model restricts algorithms' inputs, it allows organizations to make statistical queries about the sensitive data. Therefore, the task is to ensure individuals' privacy while providing statistical information. To achieve so, the model implements the technique of differential privacy. 
                                Differential privacy is a tradeoff between privacy level(noise level) and data availability. The larger the noise is, the less accurate and meaningful the data is. 
                                This application applies the laplace machanism, where the noise distribution obeys the laplace distribution as shown on the left below. We do not modify mu, hence we only look at the first three zero-centred line. 
                                beta equals sensitivity/epsilon, under the definition of the laplace mechanism, sensitivity represents the change that a single entry can bring to the result. In this app, sensitivity is always set to 1, since in most case it satisfies the definition,
                                moreover, it is sufficient and easier to control beta only through epsilon. Therefore, in this app, noise level equals to 1/epsilon. Thereby the chart on the right can be drawn showing the relationship between epsilon (the x axis) and noise level (the y axis).
                                This application considers epsilon=0.5, noise level=2 as the largest acceptable noise level.  ''',
        'e2_t1_title': "Test 1: Single query privacy level test",
        'e2_t1_subtitle1': "a). continuous return queries in a large data set",
        'e2_t1_description': "While providing an API to access certain level of the sensitive information, it is vital to ensure the result of the queries have high enough privacy level against differential attack.",
        'e2_t1_q1_description': "In the Statlog (German Credit Data) Data Set, we regard age as a sensitive information. Suppose the organization queries the average age.",
        'e2_t1_q2_description': "Now suppose there is a new entry of age 25, query the value again.",
        'e2_t1_description2': "Without differential privacy, the age of the new entry can be easily computed using the real values:",
        'e2_t1_description3': "Compute this with the processed values again:",
        'e2_t1_subtitle2': "b). continuous return queries in a small data set",
        'e2_t1_q3_description': "Differential privacy works well with data set of 1000 entries, now consider a smaller data set. Only take the first 10 entries of the Statlog (German Credit Data) Data Set:",
        'e2_t1_q4_description': "add 11th entry with age 25 and run the query again:",
        'e2_t1_subtitle3': "c). \"How many\" queries:",
        'e2_t1_q5_description': "This part tests the performance of differential privacy with queries that ask \"how many...\" questions, in this case the size of the data set does not matter, because no computation is necessary where the new entry can only affect the result by 0 or 1. Suppose the organization is querying the number of single male in the data set:",
        'e2_t1_q6_description': "Suppose another entries comes in that satisfy the requirement (he is a single male):",
        'e2_t1_description4': "Based on the mechanism of laplace differential privacy, the best guess one can do is: if the second result is larger than the first result, the new entry satisfies the requirement, else it doesn't. Try to make a guess:",
        'e2_t1_description5': "Now with the information of the processed result, test the winning rate by running the above guess 1000 times:",
        'e2_t1_description6': "The above computation use epsilon=1, choosing a smaller epsilon will increase the noise, run the test again with epsilon=0.5:",
        'e2_t2_title': "Test 2: Multiple queries privacy level test",
        'e2_t2_description': "So far, individual's privacy seems to be safe, but there is one more things to test. The laplace machenism in differential privacy means the noise follows a laplace distribution, which means the expected noise is 0. If one makes the same queries many times, it is expected to have 0 noise when calculating the average.",
        'e2_t2_c1_description': "Run the differential privacy algorithm 100,000 times with epsilon=1 (applies in continuous return queries), only takes the noise and sum them up:",
        'e2_t2_c2_description': "Run 100,000 times with epsilon=0.5 (applies in \"how many\" question queries):",
        'e2_t2_customize_description': "Try to run this experiment with another epsilon value:",
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
    statlog_attributes = ["account_status", "duration", "credit_history", "purpose", "credit_amount", "savings_account", "present_employment_since", "installment_rate_in_income", "personal_status_and_sex", 
        "guarantors", "present_residence_since", "property", "age", "other_installment_plans", "housing", "existing_credits", "job", "maintenance_provider_number", "telephone", "foreign_worker"]
    statlog_discrete_values = {
        "account_status": {"A11": "Less than 0 DM", "A12": "0 to 200 DM", "A13": "Greater than 200 DM", "A14": "No checking account"},
        "credit_history": {"A30": "no credits taken/all credits paid back duly", "A31": "all credits at this bank paid back duly", "A32": "existing credits paid back duly till now", "A33": "delay in paying off in the past", "A34": "critical account/other credits existing (not at this bank)"},
        "purpose": {"A40": "car(new)", "A41": "car(used)", "A42": "furniture/equipment", "A43": "radio/television", "A44": "domestic appliances", "A45": "repairs", "A46": "education", "A48": "retraining", "A49": "business", "A410": "others"},
        "savings_account": {"A61": "Less than 100 DM", "A62": "100 to 500 DM", "A63": "500 to 1000 DM", "A64": "Greater than 1000 DM", "A65": "Unknown/no saving account"},
        "present_employment_since": {"A71": "Unemployed", "A72": "Less than 1 year", "A73": "1 to 4 years", "A74": "4 to 7 years", "A75": "More than 7 years"},
        "personal_status_and_sex": {"A91": "Male, divorced/separated", "A92": "Female, divorced/separated/married", "A93": "Male, single", "A94": "Male, married/widowed", "A95": "Female, single"},
        "guarantors": {"A101": "None", "A102": "Co-applicant", "A103": "guarantor"},
        "property": {"A121": "Real estate", "A122": "Building society savings agreement/life insurance", "A123": "Car or other", "A124": "Unknown/no property"}, 
        "other_installment_plans": {"A141": "Bank", "A142": "Stores", "A143": "None"},
        "housing": {"A151": "Rent", "A152": "Own", "A153": "For free"},
        "job": {"A171": "Unemployed/ unskilled  - non-resident", "A172": "Unskilled - resident", "A173": "Skilled employee/official", "A174": "Management/self-employed/highly qualified employee/officer"},
        "telephone": {"A191": "None", "A192": "Yes, registered under the customers name"},
        "foreign_worker": {"A201": "Yes", "A202": "No"}
    }
    e1_d2_customize_classifiers = {
        "decision_tree": "Decision tree",
        "GaussianNB": "Gaussian naive bayes"
    }
    my_context = {
		'texts': texts,
        'epsilon_and_noise': figures,
        'statlog_attributes': statlog_attributes,
        'statlog_discrete_values': statlog_discrete_values,
        'e1_d2_customize_classifiers': e1_d2_customize_classifiers
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


