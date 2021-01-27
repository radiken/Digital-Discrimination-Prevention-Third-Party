from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn.impute import SimpleImputer
import pandas as pd
from sklearn import preprocessing
import pickle

'''
Experiment 1
Test whether excluding the sensitive data affect the effectiveness of the decision making algorithm
This experiment use supervised learning classifiers to predict the income of individuals
'''
def prediction_experiment(train_x, test_x, test_y):
    # preprocess data
    train_x = pd.DataFrame(list(train_x))
    test_x = pd.DataFrame(list(test_x))
    test_y = list(test_y)

    # handle missing values
    imp = SimpleImputer(missing_values="?", strategy="most_frequent")
    train_x = pd.DataFrame(imp.fit_transform(train_x))
    test_x = pd.DataFrame(imp.fit_transform(test_x))

    # remove with gender(9th column), race(8th column) and marital status(5th column) for the processed data
    processed_train_x = train_x.drop(columns=[5,8,9])
    processed_test_x = test_x.drop(columns=[5,8,9])

    original_score = use_model(train_x, test_x, test_y, "original_model")
    processed_score = use_model(processed_train_x, processed_test_x, test_y, "processed_model")

    return original_score, processed_score

def use_model(train_x, test_x, test_y, file_name):
    # one hot encode
    # this function needs train_x to match the columns(features), a column is lost after one hot encoding
    le = preprocessing.LabelEncoder()
    test_y = le.fit_transform(test_y)
    train_length = len(train_x)
    merged_x = pd.concat([train_x, test_x], ignore_index=True)
    merged_x = pd.get_dummies(merged_x)
    test_x = merged_x.iloc[train_length:,:]

    loaded_model = pickle.load(open(file_name, 'rb'))
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

    # remove with gender(9th column), race(8th column) and marital status(5th column) for the processed data
    processed_train_x = train_x.drop(columns=[5,8,9])

    save_model(train_x, train_y, "original_model")
    save_model(processed_train_x, train_y, "processed_model")


'''
USED WHEN THE MODEL IS NOT SAVED
Train the sklearn decision tree classifier
and save the model
'''
def save_model(train_x, train_y, file_name):
    # one hot encode
    le = preprocessing.LabelEncoder()
    train_y = le.fit_transform(train_y)
    test_y = le.fit_transform(test_y)
    train_length = len(train_x)
    merged_x = pd.concat([train_x, test_x], ignore_index=True)
    merged_x = pd.get_dummies(merged_x)
    train_x = merged_x.iloc[:train_length,:]
    test_x = merged_x.iloc[train_length:,:]

    # train
    clf = tree.DecisionTreeClassifier()
    print('start training')
    clf.fit(train_x, train_y)
    print('finish training')

    # save model
    pickle.dump(clf, open(file_name, 'wb'))
