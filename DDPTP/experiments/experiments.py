from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn import preprocessing
import pickle
from DP_library import laplace
import numpy as np
from .models import Adult_original
from .models import Adult_test
from .models import Statlog
from django.db import connection

# To increase efficiency, prepare some data while initializing
statlog_data = Statlog.objects.values_list("account_status", "duration", "credit_history", "purpose", "credit_amount", "savings_account", "present_employment_since", "installment_rate_in_income", "personal_status_and_sex", 
        "guarantors", "present_residence_since", "property", "age", "other_installment_plans", "housing", "existing_credits", "job", "maintenance_provider_number", "telephone", "foreign_worker")
statlog_result = Statlog.objects.values_list("result")
adult_train_x = Adult_original.objects.values_list("age", "workclass", "fnlwgt", "education", "education_num", "marital_status", "occupation", "relationship", "race", "sex", "capital_gain", "capital_loss", "hours_per_week", "native_country")
adult_train_y = Adult_original.objects.values_list("income")
adult_test_x = Adult_test.objects.values_list("age", "workclass", "fnlwgt", "education", "education_num", "marital_status", "occupation", "relationship", "race", "sex", "capital_gain", "capital_loss", "hours_per_week", "native_country")
adult_test_y = Adult_test.objects.values_list("income")
adult_train_x = pd.DataFrame(list(adult_train_x))
adult_test_x = pd.DataFrame(list(adult_test_x))
if(len(adult_train_x)>0 and len(adult_test_x)>0):
    imp = SimpleImputer(missing_values="?", strategy="most_frequent")
    adult_train_x = pd.DataFrame(imp.fit_transform(adult_train_x))
    adult_test_x = pd.DataFrame(imp.fit_transform(adult_test_x))
    adult_train_x.columns = ['age', 'workclass', 'fnlwgt', 'education', 'education_num', 'marital_status', 'occupation', 'relationship', 'race', 'sex', 'capital_gain', 'capital_loss', 'hours_per_week', 'native_country']
    adult_test_x.columns = ["age", "workclass", "fnlwgt", "education", "education_num", "marital_status", "occupation", "relationship", "race", "sex", "capital_gain", "capital_loss", "hours_per_week", "native_country"]

'''
Discrimination Experiment
Test how excluding or abstracting the sensitive data affects the performance of the decision-making algorithm
'''


# param: 
#   classifier: a string of the machine learning classifier to use. Available choices: decision_tree, SVC, GaussianNB
#   actions: a dictionary of what to remove or abstract. E.g. {'account_status': "remove", 'age': ['<10', ' in range(10, 50)', '>=50'], 'account_status':[["A11", "A12"], ["A13", "A14"]]}
def customize_statlog_predition(classifier, actions):
    x = pd.DataFrame(statlog_data)
    y = statlog_result
    x.columns = ["account_status", "duration", "credit_history", "purpose", "credit_amount", "savings_account", "present_employment_since", "installment_rate_in_income", "personal_status_and_sex", 
        "guarantors", "present_residence_since", "property", "age", "other_installment_plans", "housing", "existing_credits", "job", "maintenance_provider_number", "telephone", "foreign_worker"]
    
    original_train_x, original_test_x, train_y, test_y = train_test_split(x, list(y), test_size=0.33, shuffle=False)

    processed_train_x = preprocess_data(original_train_x, actions)
    processed_test_x = preprocess_data(original_test_x, actions)

    # one hot encode
    to_encode = ["account_status", "credit_history", "purpose", "savings_account", "present_employment_since", "personal_status_and_sex", 
        "guarantors", "property", "other_installment_plans", "housing", "job", "telephone", "foreign_worker"]
    one_hot_original_train_x = pd.get_dummies(original_train_x, columns=to_encode)
    one_hot_original_test_x = pd.get_dummies(original_test_x, columns=to_encode)
    # see what attributes to encode for processed_x
    continuous_attributes = ["duration", "credit_amount", "installment_rate_in_income", "present_residence_since", "age", "existing_credits", "maintenance_provider_number"]
    for key in actions.keys():
        if key in continuous_attributes:
            to_encode.append(key)
        if actions[key]=="remove":
            to_encode.remove(key)
    one_hot_processed_train_x = pd.get_dummies(processed_train_x, columns=to_encode)
    one_hot_processed_test_x = pd.get_dummies(processed_test_x, columns=to_encode)

    if classifier == "decision_tree":
        original_clf = tree.DecisionTreeClassifier()
        processed_clf = tree.DecisionTreeClassifier()
    elif classifier == "SVC":
        original_clf = SVC()
        processed_clf = SVC()
    elif classifier == "GaussianNB":
        original_clf = GaussianNB()
        processed_clf = GaussianNB()
    else:
        raise Exception("classifier error")
    original_clf.fit(one_hot_original_train_x, train_y)
    original_score = original_clf.score(one_hot_original_test_x, test_y)
    original_score = original_score.round(2)
    original_result = original_clf.predict(one_hot_original_test_x)
    
    processed_clf.fit(one_hot_processed_train_x, train_y)
    processed_score = processed_clf.score(one_hot_processed_test_x, test_y)
    processed_score = processed_score.round(2)
    processed_result = processed_clf.predict(one_hot_processed_test_x)

    test_y = [i[0] for i in test_y]
    sex_original_metrics = get_result_metrics(original_test_x, original_result, test_y, "personal_status_and_sex", ["A91", "A93", "A94"], ["A92", "A95"], 1, 2)
    sex_processed_metrics = get_result_metrics(original_test_x, processed_result, test_y, "personal_status_and_sex", ["A91", "A93", "A94"], ["A92", "A95"], 1, 2)
    sex_metrics = list(zip(sex_original_metrics, sex_processed_metrics))
    age_original_metrics = get_result_metrics(original_test_x, original_result, test_y, "age", "<=37", ">=38", 1, 2)
    age_processed_metrics = get_result_metrics(original_test_x, processed_result, test_y, "age", "<=37", ">=38", 1, 2)
    age_metrics = list(zip(age_original_metrics, age_processed_metrics))
    scores = [original_score, processed_score]
    metrics = [scores, sex_metrics, age_metrics]
    return metrics


# param: 
#   actions: a dictionary of what to remove or abstract. E.g. {'account_status': "remove", 'age': ['<10', ' in range(10, 50)', '>=50'], 'account_status':[["A11", "A12"], ["A13", "A14"]]}
def adult_prediction(actions):
    # preprocess data
    train_x = adult_train_x.copy()
    test_x = adult_test_x.copy()
    processed_train_x = preprocess_data(train_x, actions)
    processed_test_x = preprocess_data(test_x, actions)

    # one hot encode
    le = preprocessing.LabelEncoder()
    train_y = le.fit_transform(adult_train_y)
    test_y = le.fit_transform(adult_test_y)
    to_encode = ['workclass', 'education', 'marital_status', 'occupation', 'relationship', 'race', 'sex', 'native_country']
    original_test_x = pd.get_dummies(test_x, columns=to_encode)
    continuous_attributes = ["age", "fnlwgt", "education_num", "capital_gain", "capital_loss", "hours_per_week"]
    for key in actions.keys():
        if key in continuous_attributes:
            to_encode.append(key)
        if actions[key]=="remove":
            to_encode.remove(key)
    processed_train_x = pd.get_dummies(processed_train_x, columns=to_encode)
    processed_test_x = pd.get_dummies(processed_test_x, columns=to_encode)

    # match columns(features)
    original_columns = pickle.load(open('ml_models/adult_original_columns', 'rb'))
    original_missing_columns = set(original_columns) - set(original_test_x.columns)
    for column in original_missing_columns:
        original_test_x[column] = 0
    original_test_x = original_test_x[original_columns]
    original_result = load_model_and_predict('original_decision_tree', original_test_x)
    original_score = load_model_and_score(original_test_x, test_y, 'original_decision_tree')

    clf = tree.DecisionTreeClassifier()
    clf.fit(processed_train_x, train_y)
    # match columns(features)
    processed_columns = processed_train_x.columns
    processed_missing_columns = set(processed_columns) - set(processed_test_x.columns)
    for column in original_missing_columns:
        processed_test_x[column] = 0
    processed_test_x = processed_test_x[processed_columns]
    processed_result = clf.predict(processed_test_x)
    processed_score = clf.score(processed_test_x, test_y)

    sex_original_metrics = get_result_metrics(test_x, original_result, test_y, "sex", ["Male"], ["Female"], 1, 0)
    sex_processed_metrics = get_result_metrics(test_x, processed_result, test_y, "sex", ["Male"], ["Female"], 1, 0)
    sex_metrics = list(zip(sex_original_metrics, sex_processed_metrics))
    race_original_metrics = get_result_metrics(test_x, original_result, test_y, "race", ["White"], ["Black", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other"], 1, 0)
    race_processed_metrics = get_result_metrics(test_x, processed_result, test_y, "race", ["White"], ["Black", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other"], 1, 0)
    race_metrics = list(zip(race_original_metrics, race_processed_metrics))
    scores = [original_score, processed_score]
    scores = [round(x,2) for x in scores]
    metrics = [scores, sex_metrics, race_metrics]
    return metrics

def adult_correlations():
    # preprocess data
    test_x = adult_test_x
    test_x.columns = ["age", "workclass", "fnlwgt", "education", "education_num", "marital_status", "occupation", "relationship", "race", "sex", "capital_gain", "capital_loss", "hours_per_week", "native_country"]

    # one hot encode
    original_test_x = pd.get_dummies(test_x, columns=['workclass', 'education', 'marital_status', 'occupation', 'relationship', 'race', 'sex', 'native_country'])

    one_hot_columns = list(original_test_x.columns.values)
    original_test_x = original_test_x.astype(int)
    test_x_values = original_test_x.values
    correlations = np.corrcoef(test_x_values.T)
    male_correlations = correlations[one_hot_columns.index("sex_Male")]
    white_correlations = correlations[one_hot_columns.index("race_White")]
    black_correlations = correlations[one_hot_columns.index("race_Black")]
    asian_correlations = correlations[one_hot_columns.index("race_Asian-Pac-Islander")]
    amer_correlations = correlations[one_hot_columns.index("race_Amer-Indian-Eskimo")]
    other_correlations = correlations[one_hot_columns.index("race_Other")]
    correlations_with_sensitive = pd.DataFrame(np.array([white_correlations, black_correlations, asian_correlations, amer_correlations, other_correlations, male_correlations]), columns=one_hot_columns)
    correlations_with_sensitive.drop(columns=['sex_Male', 'sex_Female', 'race_White', 'race_Black', 'race_Asian-Pac-Islander', 'race_Amer-Indian-Eskimo', 'race_Other'], inplace=True)
    correlations_with_sensitive = correlations_with_sensitive.append(correlations_with_sensitive.iloc[:-1].abs().mean(numeric_only=True), ignore_index=True)
    correlations_with_sensitive = correlations_with_sensitive.iloc[-2:]
    sorted_correlations = correlations_with_sensitive.abs().sum().sort_values(ascending=False)
    return sorted_correlations

# get the metrics that evaluate the discrimination level
# privileged_group and unprivileged_group are lists(discrete value) or strings(continuous values)
def get_result_metrics(test_x, prediction, real_result, attribute_name, privileged_value, unprivileged_value, privileged_group, unprivileged_group):
    test_x['prediction'] = prediction
    test_x['real_result'] = real_result
    if isinstance(privileged_value, list):
        privileged_df = test_x.loc[test_x[attribute_name].isin(privileged_value)]
        unprivileged_df = test_x.loc[test_x[attribute_name].isin(unprivileged_value)]
    elif isinstance(privileged_value, str):
        privileged_df = test_x.loc[eval("test_x[attribute_name]" + privileged_value), :]
        unprivileged_df = test_x.loc[eval("test_x[attribute_name]" + unprivileged_value), :]
    statistical_parity_difference = get_statistical_parity_difference(privileged_df, unprivileged_df, privileged_group, unprivileged_group)
    equal_opportunity_difference = get_equal_opportunity_difference(privileged_df, unprivileged_df, privileged_group, unprivileged_group)
    average_odds_difference = get_average_odds_difference(privileged_df, unprivileged_df, privileged_group, unprivileged_group)
    disparate_impact = get_disparate_impact(privileged_df, unprivileged_df, privileged_group, unprivileged_group)

    metrics = [statistical_parity_difference, equal_opportunity_difference, average_odds_difference, disparate_impact]
    metrics = [round(n, 2) for n in metrics]
    return metrics

def get_statistical_parity_difference(privileged_df, unprivileged_df, privileged_group, unprivileged_group):
    privileged_rates = privileged_df['prediction'].value_counts(normalize=True)
    privileged_rate = privileged_rates.get(key=privileged_group)
    unprivileged_rates = unprivileged_df['prediction'].value_counts(normalize=True)
    unprivileged_rate = unprivileged_rates.get(key=privileged_group)

    statistical_parity_difference = unprivileged_rate-privileged_rate
    return statistical_parity_difference

def get_equal_opportunity_difference(privileged_df, unprivileged_df, privileged_group, unprivileged_group):
    privileged_actual_positive_df = privileged_df.loc[privileged_df['real_result']==privileged_group]
    privileged_true_positive_df = privileged_actual_positive_df.loc[privileged_actual_positive_df['prediction']==privileged_group]
    unprivileged_actual_positive_df = unprivileged_df.loc[unprivileged_df['real_result']==privileged_group]
    unprivileged_true_positive_df = unprivileged_actual_positive_df.loc[unprivileged_actual_positive_df['prediction']==privileged_group]
    privileged_true_positive_rate = len(privileged_true_positive_df)/len(privileged_actual_positive_df)
    unprivileged_true_positive_rate = len(unprivileged_true_positive_df)/len(unprivileged_actual_positive_df)

    equal_opportunity_difference = unprivileged_true_positive_rate-privileged_true_positive_rate
    return equal_opportunity_difference

def get_average_odds_difference(privileged_df, unprivileged_df, privileged_group, unprivileged_group):
    privileged_actual_negative_df = privileged_df.loc[privileged_df['real_result']==unprivileged_group]
    privileged_false_positive_df = privileged_actual_negative_df.loc[privileged_actual_negative_df['prediction']==privileged_group]
    privileged_false_positive_rate = len(privileged_false_positive_df)/len(privileged_actual_negative_df)
    unprivileged_actual_negative_df = unprivileged_df.loc[unprivileged_df['real_result']==unprivileged_group]
    unprivileged_false_positive_df = unprivileged_actual_negative_df.loc[unprivileged_actual_negative_df['prediction']==privileged_group]
    unprivileged_false_positive_rate = len(unprivileged_false_positive_df)/len(unprivileged_actual_negative_df)
    false_positive_difference = unprivileged_false_positive_rate - privileged_false_positive_rate

    true_positive_difference = get_equal_opportunity_difference(privileged_df, unprivileged_df, privileged_group, unprivileged_group)

    average_odds_difference = (false_positive_difference + true_positive_difference) / 2
    return average_odds_difference

def get_disparate_impact(privileged_df, unprivileged_df, privileged_group, unprivileged_group):
    privileged_rates = privileged_df['prediction'].value_counts(normalize=True)
    privileged_rate = privileged_rates.get(key=privileged_group)
    unprivileged_rates = unprivileged_df['prediction'].value_counts(normalize=True)
    unprivileged_rate = unprivileged_rates.get(key=privileged_group)

    disparate_impact = unprivileged_rate / privileged_rate
    return disparate_impact


# Process a training set by either remove it abstract the attributes according to the actions
# param: 
#   x: a dataframe of training data
#   actions: a dictionary of what to remove or abstract. E.g. {'account_status': "remove", 'age': {'young_age': '<10', 'middle_age': ' in range(10, 50)', 'older_age': '>=50'}, 'account_status': {'husband-or-wife': ["A11", "A12"], ["A13", "A14"]}}
def preprocess_data(x, actions):
    processed_x = x.copy()
    for attribute, action in actions.items():
        if action == "remove":
            processed_x = processed_x.drop(columns=[attribute])
        else:
            if isinstance(action, list):
                # generate group name and match values
                group_number = 1
                groups = {}
                for group in action:
                    # ensure the value is treated as number in the dataframe
                    group_name = "group"+str(group_number)
                    groups[group_name] = group
                    group_number = group_number + 1
            elif isinstance(action, dict):
                # the groups have given names
                groups = action
            else:
                raise Exception("values in actions must be list or dict")
            # abstract the attribute
            if isinstance(list(groups.items())[0][1], list):
                # it's discrete data
                for i, row in processed_x.iterrows():
                    value = processed_x.at[i, attribute]
                    for group_name, values in groups.items():
                        if value in values:
                            processed_x.at[i, attribute] = group_name
                            break
            else:
                # it's continuous data
                for i, row in processed_x.iterrows():
                    value = processed_x.at[i, attribute]
                    for group_name, condition in groups.items():
                        if eval(str(value) + condition):
                            # at method works more efficient, but it doesn't work for the german data set for unknown reason
                            # loc produce same results but with lower efficiency
                            try:
                                processed_x.at[i, attribute] = group_name
                            except:
                                processed_x.loc[i, attribute] = group_name
                            break
    return processed_x

def load_model_and_score(test_x, test_y, file_name):
    loaded_model = pickle.load(open('ml_models/'+file_name, 'rb'))
    result = loaded_model.score(test_x, test_y)
    return result

def load_model_and_predict(model_name, one_hot_test_x):
    model = pickle.load(open(f'ml_models/{model_name}', 'rb'))
    result = model.predict(one_hot_test_x)
    return result

'''
Privacy Experiments 
Test the performance of differential privacy
'''
def get_dp_result(result, sensitivity=1, epsilon=1):
    return laplace(result, sensitivity=sensitivity, epsilon=epsilon)

def get_noise_n_times(n, epsilon=1):
    noise_sum = 0
    for _ in range(n):
        noise_sum = noise_sum + get_dp_result(0, epsilon=epsilon)
    return noise_sum

def epsilon_and_noise_level_chart_figures():
    figures = []
    # use epsilon = 1 as a standard, noise level = 1
    for epsilon in np.arange(0.1, 10.0, 0.1):
        figures.append([epsilon, 1/epsilon])
    return figures

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
        avg_query = "SELECT AVG(experiments_statlog.age) FROM (SELECT experiments_statlog.age from experiments_statlog LIMIT "+str(count)+") experiments_statlog"
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

# ---------------- functions to create models ---------------------

'''
USE WHEN THE MODEL IS NOT SAVED
Create and save the models for the prediction experiment
'''
def generate_prediction_experiment_model(train_x, train_y):
    # prepare data
    train_x = pd.DataFrame(list(train_x))
    train_y = list(train_y)

    # handle missing values
    imp = SimpleImputer(missing_values="?", strategy="most_frequent")
    train_x = pd.DataFrame(imp.fit_transform(train_x))
    train_x.columns = ['age', 'workclass', 'fnlwgt', 'education', 'education_num', 'marital_status', 'occupation', 'relationship', 'race', 'sex', 'capital_gain', 'capital_loss', 'hours_per_week', 'native_country']
    # remove sensitive data for the processed data
    processed_train_x = train_x.drop(columns=['marital_status', 'race', 'sex', 'native_country'])
    # abstract age and relationship for abstracted data
    abstracted_train_x = processed_train_x
    for i in range(len(abstracted_train_x)):
        age = abstracted_train_x.at[i, 'age']
        if age <= 35:
            abstracted_train_x.at[i, 'age'] = "young_age"
        elif 36 <= age <= 55:
            abstracted_train_x.at[i, 'age'] = "middle_age"
        else:
            abstracted_train_x.at[i, 'age'] = "older_age"

        relationship = abstracted_train_x.at[i, 'relationship']
        if relationship == 'Husband' or relationship == 'Wife':
            abstracted_train_x.at[i, 'relationship'] = "Husband-or-wife"

    # one hot encode
    le = preprocessing.LabelEncoder()
    train_y = le.fit_transform(train_y)
    train_x = pd.get_dummies(train_x, columns=['workclass', 'education', 'marital_status', 'occupation', 'relationship', 'race', 'sex', 'native_country'])
    processed_train_x = pd.get_dummies(processed_train_x, columns=['workclass', 'education', 'occupation', 'relationship'])
    abstracted_train_x = pd.get_dummies(abstracted_train_x, columns=['age', 'workclass', 'education', 'occupation', 'relationship'])

    save_model(train_x, train_y, "original_decision_tree")
    save_model(processed_train_x, train_y, "processed_decision_tree")
    save_model(abstracted_train_x, train_y, "abstracted_decision_tree")


'''
USED WHEN THE MODEL IS NOT SAVED
Train the sklearn decision tree classifier
and save the model
'''
def save_model(train_x, train_y, file_name):
    # train
    clf = tree.DecisionTreeClassifier()
    print('start training')
    clf.fit(train_x, train_y)
    print('finish training')

    # save model
    pickle.dump(clf, open('ml_models/'+file_name, 'wb'))


def save_columns(train_x):
    # prepare data
    train_x = pd.DataFrame(list(train_x))

    # handle missing values
    imp = SimpleImputer(missing_values="?", strategy="most_frequent")
    train_x = pd.DataFrame(imp.fit_transform(train_x))
    train_x.columns = ['age', 'workclass', 'fnlwgt', 'education', 'education_num', 'marital_status', 'occupation', 'relationship', 'race', 'sex', 'capital_gain', 'capital_loss', 'hours_per_week', 'native_country']
    # remove sensitive data for the processed data
    processed_train_x = train_x.drop(columns=['marital_status', 'race', 'sex', 'native_country'])

    # one hot encode
    le = preprocessing.LabelEncoder()
    train_x = pd.get_dummies(train_x, columns=['workclass', 'education', 'marital_status', 'occupation', 'relationship', 'race', 'sex', 'native_country'])
    processed_train_x = pd.get_dummies(processed_train_x, columns=['workclass', 'education', 'occupation', 'relationship'])

    pickle.dump(train_x.columns, open('ml_models/adult_original_columns', 'wb'))
    pickle.dump(processed_train_x.columns, open('ml_models/adult_processed_columns', 'wb'))
