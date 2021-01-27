from django.shortcuts import render
from .experiments import *
from .models import Adult_original
from .models import Adult_test

'''
Experiment 1: prediction experiment
Test whether excluding the sensitive data affect the effectiveness of the decision making algorithm
This experiment use supervised learning classifiers to predict the income of individuals
'''
def prediction():
    # train classifier with the original data
    clf = GaussianNB()
    train_x = Adult_original.objects.values_list("age", "workclass", "fnlwgt", "education", "education_num", "marital_status", "occupation", "relationship", "race", "sex", "capital_gain", "capital_loss", "hours_per_week", "native_country")
    test_x = Adult_test.objects.values_list("age", "workclass", "fnlwgt", "education", "education_num", "marital_status", "occupation", "relationship", "race", "sex", "capital_gain", "capital_loss", "hours_per_week", "native_country")
    test_y = Adult_test.objects.values_list("income")

    return prediction_experiment(train_x, test_x, test_y)

def prediction_experiment_view(request, *args, **kwargs):
    original_score, processed_score = prediction()
    my_context = {
		'original_score': original_score,
        'processed_score': processed_score
	}
    return render(request, "experiments\home.html", my_context)


# Create your views here.

# keys = ["age", "name", "fnlwgt", "education", "education_num", "marital_status", "occupation", "relationship", "race", "sex", "capital_gain", "capital_loss", "hours_per_week", "native_country", "income"]
# f = open('adult.test', 'r')
# for adult in f:
#     adult = adult.split(", ")
#     adult[-1] = adult[-1].rstrip().replace(".", "")
#     Adult_test.objects.create(**dict(zip(keys, adult)))

# f.close()


