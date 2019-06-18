import os

import geopy.distance
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymysql
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize
from sklearn.svm import SVC
from sklearn.utils import shuffle


def execute_sql_query(query, records=None, log_enabled=False):
    print(query)
    try:
        sql_db = connect_to_sql_database(db_name=db_name)
        cursor = sql_db.cursor()
        if records is not None:
            print("SQL Query: %s" % query, records)
            cursor.executemany(query, records)
        else:
            if log_enabled:
                print("SQL Query: %s" % query)
            cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            if log_enabled:
                print("SQL Answer: %s" % row)
        return rows
    except Exception as e:
        print("Exeception occured:{}".format(e))


def connect_to_sql_database(db_server_name="localhost", db_user="axel", db_password="Mojjo@2015", db_name="",
                            char_set="utf8mb4", cusror_type=pymysql.cursors.DictCursor):
    # print("connecting to db %s..." % db_name)
    sql_db = pymysql.connect(host=db_server_name, user=db_user, password=db_password,
                             db=db_name, charset=char_set, cursorclass=cusror_type)
    return sql_db


def get_loneli_score(region):
    #value from visualization tool!2018 choropleth map
    if 'North East' in region:
        return 1.75748
    if 'North West' in region:
        return 0.87487
    if 'Yorkshire and The Humber' in region:
        return 0.17492
    if 'West Midlands' in region:
        return -0.50466
    if 'East Midlands' in region:
        return 0.57428
    if 'South West' in region:
        return 1.17238
    if 'South East' in region:
        return 1.58932
    if 'East of England' in region:
        return 1.38873
    if 'London' in region:
        return 0.32770


def get_loneliness_class(score):
    if score <= 0:
        return 0
    if 0 < score < 1:
        return 1
    if score >= 1:
        return 2


def purge_file(filename):
    print("purge %s..." % filename)
    try:
        os.remove(filename)
    except FileNotFoundError:
        print("file not found.")


def create_trainning_set(data):
    filename = 'training_set.data'
    purge_file(filename)
    with open(filename, 'a') as outfile:
        for i in data:
            training_str_flatten = "%f,%f,%f,%d" % (i['distance_traveled'], i['domicile_lat'], i['domicile_long'], i['class'])
            outfile.write(training_str_flatten)
            outfile.write('\n')
    outfile.close()
    return filename


def process_data_frame(data_frame):
    data_frame = data_frame.fillna(-1)
    X = data_frame[data_frame.columns[0:data_frame.shape[1] - 1]].values
    X = normalize(X)
    X = preprocessing.MinMaxScaler().fit_transform(X)
    print(X.shape, X)
    # print(DataFrame.from_records(X))
    y = data_frame["class"].values.flatten()
    train_x, test_x, train_y, test_y = train_test_split(X, y, train_size=0.7, shuffle=True)
    # print('TRAIN_X')
    # print(DataFrame(train_x))
    # print('TRAIN_Y')
    # print(DataFrame(train_y))
    # print('TEST_X')
    # print(DataFrame(test_x))
    # print('TEST_Y')
    # print(DataFrame(test_y))
    return X, y, train_x, test_x, train_y, test_y


def plot_roc_curve(fpr, tpr):
    plt.plot(fpr, tpr, color='orange', label='ROC')
    plt.plot([0, 1], [0, 1], color='darkblue', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend()
    plt.show()


def make_meshgrid(x, y, h=.02):
    x_min, x_max = x.min() - 1, x.max() + 1
    y_min, y_max = y.min() - 1, y.max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    return xx, yy


def plot_contours(ax, clf, xx, yy, **params):
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    out = ax.contourf(xx, yy, Z, **params)
    return out


def plot_2d_decision_bounderies(Xreduced, y, classifier, title=''):
    fig, ax = plt.subplots()
    if Xreduced.shape[1] > 1:
        X0, X1 = Xreduced[:, 0], Xreduced[:, 1]
        xx, yy = make_meshgrid(X0, X1)
        plot_contours(ax, classifier, xx, yy, alpha=0.8)
        ax.scatter(X0, X1, c=y, s=20, edgecolors='k')
    ax.set_title(title)
    ax.legend()
    plt.show()


def get_prec_recall_fscore_support(clf, test_x, test_y, fold):
    pred_y = cross_val_predict(clf, test_x, test_y, cv=fold)
    precision_recall_fscore_support_result = precision_recall_fscore_support(test_y, pred_y, average=None,
                                                                             labels=[False, True])
    print("precision_recall_fscore_support_result", precision_recall_fscore_support_result)
    precision_false = precision_recall_fscore_support_result[0][0]
    precision_true = precision_recall_fscore_support_result[0][1]
    print("svc precision_false %d fold cross validation is %f" % (fold, precision_recall_fscore_support_result[0][0]))
    print("svc precision_true %d fold cross validation is %f" % (fold, precision_recall_fscore_support_result[0][1]))

    recall_false = precision_recall_fscore_support_result[1][0]
    recall_true = precision_recall_fscore_support_result[1][1]
    print("svc recall_false %d fold cross validation is %f" % (fold, precision_recall_fscore_support_result[1][0]))
    print("svc recall_true %d fold cross validation is %f" % (fold, precision_recall_fscore_support_result[1][1]))

    fscore_false = precision_recall_fscore_support_result[2][0]
    fscore_true = precision_recall_fscore_support_result[2][1]
    print("svc fscore_false %d fold cross validation is %f" % (fold, precision_recall_fscore_support_result[2][0]))
    print("svc fscore_true %d fold cross validation is %f" % (fold, precision_recall_fscore_support_result[2][1]))

    support_false = precision_recall_fscore_support_result[3][0]
    support_true = precision_recall_fscore_support_result[3][1]
    print("svc support_false %d fold cross validation is %f" % (fold, precision_recall_fscore_support_result[3][0]))
    print("svc support_true %d fold cross validation is %f" % (fold, precision_recall_fscore_support_result[3][1]))
    return precision_false, precision_true, recall_false, recall_true, fscore_false, fscore_true, support_false, support_true


def process_SVC(data_frame, clf=SVC(kernel='rbf', gamma='auto', C=1000), fold=10):
    X, y, train_x, test_x, train_y, test_y = process_data_frame(data_frame)
    print("Fitting the classifier to the training set")
    param_grid = {'C': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000, 2000, 1000]}
    clf = GridSearchCV(SVC(gamma='auto', kernel='rbf'), param_grid)
    clf = clf.fit(train_x, train_y)
    print("Best estimator found by grid search:")
    print(clf.best_estimator_)
    clf = clf.best_estimator_
    print("training...")
    # clf_o.fit(train_x, train_y)
    print("predicting...")

    y_pred = clf.predict(test_x)
    print('Accuracy' + str(accuracy_score(test_y, y_pred)))
    print(clf.score(test_x, test_y))

    scores = cross_val_score(clf, test_x, test_y, cv=fold)
    print(scores)
    cross_validated_score = float(np.mean(scores))
    print("svc %d fold cross validation is %f" % (fold, cross_validated_score))
    precision_false, precision_true, recall_false, recall_true, fscore_false, fscore_true, support_false, \
    support_true = get_prec_recall_fscore_support(clf, test_x, test_y, fold)

    return train_x.shape[0], test_x.shape[0], 1000, 'SVM-rbf', precision_true, precision_false, \
           cross_validated_score, fold, recall_true, recall_false, \
           fscore_true , fscore_false, support_true, support_false, X, y


def process_SVC_PCA(data_frame, clf=SVC(kernel='rbf', gamma='auto', C=1000), fold=10):
    X, y, train_x, _, _, _ = process_data_frame(data_frame)
    y = y.astype(int)
    Xreduced = PCA(n_components=2).fit_transform(X)
    s = train_x.shape[0]
    train_x = Xreduced[0:s]
    train_y = y[0:s]
    test_x = Xreduced[s:]
    test_y = y[s:]

    clf.fit(train_x, train_y)
    scores = cross_val_score(clf, test_x, test_y, cv=fold)

    cross_validated_score = float(np.mean(scores))
    print("svc %d fold cross validation is %f" % (fold, cross_validated_score))

    precision_false, precision_true, recall_false, recall_true, fscore_false, fscore_true, support_false, \
    support_true = get_prec_recall_fscore_support(clf, test_x, test_y, fold)

    plot_2d_decision_bounderies(Xreduced, y, clf, 'PCA')

    return train_x.shape[0], test_x.shape[0], 1000, 'SVM-rbf', precision_true, precision_false, \
           cross_validated_score, fold, recall_true, recall_false, \
           fscore_true , fscore_false, support_true, support_false, X, y


def process_SVC_LDA(data_frame, clf=SVC(C=100, kernel='rbf', probability=True), fold=10):
    X, y, train_x, test_x, train_y, test_y = process_data_frame(data_frame)
    y = y.astype(int)
    Xreduced = LDA(n_components=2).fit_transform(X, y)
    print(Xreduced.shape)
    s = train_x.shape[0]
    train_x = Xreduced[0:s]
    train_y = y[0:s]
    test_x = Xreduced[s:]
    test_y = y[s:]

    print("Fitting the classifier to the training set")
    param_grid = {'C': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000, 2000, 1000], 'gamma': [0.0001, 0.001, 0.01, 0.1, 1]}
    clf = GridSearchCV(SVC(gamma='auto', kernel='rbf'), param_grid)
    clf = clf.fit(train_x, train_y)
    print("Best estimator found by grid search:")
    print(clf.best_estimator_)
    clf = clf.best_estimator_

    scores = cross_val_score(clf, test_x, test_y, cv=fold)
    print(scores)
    cross_validated_score = float(np.mean(scores))
    print("svc %d fold cross validation is %f" % (fold, cross_validated_score))
    precision_false, precision_true, recall_false, recall_true, fscore_false, fscore_true, support_false, \
    support_true = get_prec_recall_fscore_support(clf, test_x, test_y, fold)

    plot_2d_decision_bounderies(Xreduced, y, clf, 'LDA')

    return train_x.shape[0], test_x.shape[0], 1000, 'SVM-rbf', precision_true, precision_false, \
           cross_validated_score, fold, recall_true, recall_false, \
           fscore_true , fscore_false, support_true, support_false, X, y


if __name__ == '__main__':
    db_server_name = "localhost"
    db_user = "root"
    db_password = "@2015"
    char_set = "utf8mb4"
    cusror_type = pymysql.cursors.DictCursor
    db_name = "loneliness"

    sql_db = pymysql.connect(host=db_server_name, user=db_user, password=db_password)
    connect_to_sql_database(db_server_name, db_user, db_password, db_name, char_set, cusror_type)

    # result = execute_sql_query("SELECT loneliness_zscore, latitude, longitude, year FROM %s WHERE year=2018" % 'final_data')
    #
    # for elem in result:
    #     print(elem['loneliness_zscore'], elem['latitude'], elem['longitude'], elem['year'])

    result = execute_sql_query("SELECT 4_way_domicile, level_of_study, mode_of_study, number, region_of_he_provider,"
                               " domicile_lat, domicile_long, region_of_he_provider_lat,"
                               " region_of_he_provider_long FROM %s WHERE academic_year=2017" % 'student_migration')
    data = {}
    for elem in result:
        # print(elem['domicile_lat'], elem['domicile_long'], elem['region_of_he_provider_lat'], elem['region_of_he_provider_long'])
        coords_1 = (elem['domicile_lat'], elem['domicile_long'])
        coords_2 = (elem['region_of_he_provider_lat'], elem['region_of_he_provider_long'])
        if 'All' in elem['level_of_study']:
            continue
        if 'All' in elem['mode_of_study']:
            continue
        if 'All' in elem['4_way_domicile']:
            continue
        if elem['number'] <= 0:
            continue
        if elem['region_of_he_provider'] not in ['North East', 'North West', 'Yorkshire and The Humber', 'West Midlands', 'East Midlands', 'South West', 'South East', 'East of England', 'London']:
            continue
        # row = [get_loneli_score(elem['region_of_he_provider']), elem['region_of_he_provider'], elem['number'], elem['level_of_study'], elem['mode_of_study'], geopy.distance.vincenty(coords_1, coords_2).km]
        # print(row)
        distance_traveled = geopy.distance.vincenty(coords_1, coords_2).km
        loneliness_score = get_loneli_score(elem['region_of_he_provider'])
        data[distance_traveled] = {"distance_traveled": distance_traveled,
                                   'domicile_lat': elem['domicile_lat'], 'domicile_long': elem['domicile_long'],
                                   'class': get_loneliness_class(loneliness_score)}
    print(data)
    fname = create_trainning_set(list(data.values()))
    data_frame = pd.read_csv(fname, sep=",", header=None)
    sample_count = data_frame.shape[1]
    hearder = ['distance_traveled', 'domicile_lat', 'domicile_long', 'class']
    data_frame.columns = hearder
    data_frame = shuffle(data_frame)
    print(data_frame)
    process_SVC(data_frame)


