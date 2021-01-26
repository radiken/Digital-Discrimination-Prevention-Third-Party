from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn.impute import SimpleImputer
import pandas as pd
from sklearn import preprocessing
'''
Experiment 1: prediction experiment
Test whether excluding the sensitive data affect the effectiveness of the decision making algorithm
This experiment use supervised learning classifiers to predict the income of individuals
'''
def prediction_experiment(train_x, train_y, test_x, test_y):
    # prepare data
    train_x = pd.DataFrame(list(train_x))
    train_y = list(train_y)
    test_x = pd.DataFrame(list(test_x))
    test_y = list(test_y)

    # handle missing values
    imp = SimpleImputer(missing_values="?", strategy="most_frequent")
    train_x = pd.DataFrame(imp.fit_transform(train_x))
    test_x = pd.DataFrame(imp.fit_transform(test_x))

    # remove with gender(9th column) and race(8th column) for the processed data
    processed_train_x = train_x.drop(columns=[8,9])
    processed_test_x = test_x.drop(columns=[8,9])

    original_score = make_prediction(train_x, train_y, test_x, test_y)
    processed_score = make_prediction(processed_train_x, train_y, processed_test_x, test_y)
    return original_score, processed_score

'''
Make prediction with the sklearn decision tree classifier
'''
def make_prediction(train_x, train_y, test_x, test_y):
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

    # predict
    print('start predicting')
    score = clf.score(test_x, test_y)
    print('finish predicting')
    return score

