from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn import preprocessing
import pickle

'''
Experiment 1
Test whether excluding the sensitive data affect the effectiveness of the decision making algorithm
This experiment use supervised learning classifiers to predict the income of individuals
'''
def statlog_prediction_experiment(x, y):
    x = pd.DataFrame(x)
    x.columns = ["account_status", "duration", "credit_history", "purpose", "credit_amount", "savings_account", "present_employment_since", "installment_rate_in_income", "personal_status_and_sex", 
        "guarantors", "present_residence_since", "property", "age", "other_installment_plans", "housing", "existing_credits", "job", "maintenance_provider_number", "telephone", "foreign_worker"]

    # remove sensitive information in the processed training set
    processed_x = x.drop(columns=["personal_status_and_sex", "age"])

    # one hot encode
    original_x = pd.get_dummies(x, columns=["account_status", "credit_history", "purpose", "savings_account", "present_employment_since", "personal_status_and_sex", 
        "guarantors", "property", "other_installment_plans", "housing", "job", "telephone", "foreign_worker"])
    processed_x = pd.get_dummies(processed_x, columns=["account_status", "credit_history", "purpose", "savings_account", "present_employment_since", 
        "guarantors", "property", "other_installment_plans", "housing", "job", "telephone", "foreign_worker"])

    # the statlog dataset is small, no need to save and load model each time
    original_train_x, original_test_x, original_train_y, original_test_y = train_test_split(original_x, list(y), test_size=0.33)
    processed_train_x, processed_test_x, processed_train_y, processed_test_y = train_test_split(processed_x, list(y), test_size=0.33)

    original_clf = tree.DecisionTreeClassifier()
    original_clf.fit(original_train_x, original_train_y)
    original_score = original_clf.score(original_test_x, original_test_y)

    processed_clf = tree.DecisionTreeClassifier()
    processed_clf.fit(processed_train_x, processed_train_y)
    processed_score = processed_clf.score(processed_test_x, processed_test_y)

    return original_score, processed_score
    
    

def adult_prediction_experiment(test_x, test_y):
    # preprocess data
    test_x = pd.DataFrame(list(test_x))
    test_y = list(test_y)

    # handle missing values
    imp = SimpleImputer(missing_values="?", strategy="most_frequent")
    test_x = pd.DataFrame(imp.fit_transform(test_x))

    # remove with gender, race, native country and marital status for the processed data
    test_x.columns = ['age', 'workclass', 'fnlwgt', 'education', 'education_num', 'marital_status', 'occupation', 'relationship', 'race', 'sex', 'capital_gain', 'capital_loss', 'hours_per_week', 'native_country']
    processed_test_x = test_x.drop(columns=['marital_status', 'race', 'sex', 'native_country'])

    # one hot encode
    le = preprocessing.LabelEncoder()
    test_y = le.fit_transform(test_y)
    test_x = pd.get_dummies(test_x, columns=['workclass', 'education', 'marital_status', 'occupation', 'relationship', 'race', 'sex', 'native_country'])
    processed_test_x = pd.get_dummies(processed_test_x, columns=['workclass', 'education', 'occupation', 'relationship'])

    # match columns(features)
    original_columns = pickle.load(open('ml_models/adult_original_columns', 'rb'))
    original_missing_columns = set(original_columns) - set(test_x.columns)
    for column in original_missing_columns:
        test_x[column] = 0
    test_x = test_x[original_columns]

    original_score = use_model(test_x, test_y, "original_decision_tree")
    processed_score = use_model(processed_test_x, test_y, "processed_decision_tree")

    return original_score, processed_score

def use_model(test_x, test_y, file_name):
    loaded_model = pickle.load(open('ml_models/'+file_name, 'rb'))
    params = loaded_model.get_params()
    result = loaded_model.score(test_x, test_y)
    return result



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

    # one hot encode
    le = preprocessing.LabelEncoder()
    train_y = le.fit_transform(train_y)
    train_x = pd.get_dummies(train_x, columns=['workclass', 'education', 'marital_status', 'occupation', 'relationship', 'race', 'sex', 'native_country'])
    processed_train_x = pd.get_dummies(processed_train_x, columns=['workclass', 'education', 'occupation', 'relationship'])
    
    save_model(train_x, train_y, "original_decision_tree")
    save_model(processed_train_x, train_y, "processed_decision_tree")


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
