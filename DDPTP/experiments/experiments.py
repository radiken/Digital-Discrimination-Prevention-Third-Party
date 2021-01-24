from sklearn.naive_bayes import GaussianNB
from sklearn.impute import SimpleImputer
import pandas as pd
'''
Experiment 1: prediction experiment
Test whether excluding the sensitive data affect the effectiveness of the decision making algorithm
This experiment use supervised learning classifiers to predict the income of individuals
'''
def prediction_experiment(train_x, train_y, test_x, test_y):
    # train classifier with the original data
    # prepare data
    train_x = pd.DataFrame(list(train_x))
    # handle missing values
    imp = SimpleImputer(missing_values="?", strategy="most_frequent")
    train_x = imp.fit_transform(train_x)
    print(train_x[:15])
    # train
    clf = GaussianNB()
    print("start")
    clf.fit(train_x, train_y)
    print("finished")
    return clf.score(test_x, test_y)



