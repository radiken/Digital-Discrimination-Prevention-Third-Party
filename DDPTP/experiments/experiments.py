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
    # train classifier with the original data
    # prepare data
    train_x = pd.DataFrame(list(train_x))
    train_y = list(train_y)
    test_x = pd.DataFrame(list(test_x))
    test_y = list(test_y)
    # handle missing values
    imp = SimpleImputer(missing_values="?", strategy="most_frequent")
    train_x = pd.DataFrame(imp.fit_transform(train_x))
    test_x = pd.DataFrame(imp.fit_transform(test_x))
    # one hot encode
    le = preprocessing.LabelEncoder()
    train_y = le.fit_transform(train_y)
    test_y = le.fit_transform(test_y)
    merged_x = pd.concat([train_x, test_x], ignore_index=True)
    merged_x = pd.get_dummies(merged_x, columns=[1,3,5,6,7,8,9,13])
    train_x = merged_x.iloc[:32592,:]
    test_x = merged_x.iloc[32592:,:]

    # train
    clf = tree.DecisionTreeClassifier()
    clf.fit(train_x, train_y)

    # predict
    return clf.score(test_x, test_y)



