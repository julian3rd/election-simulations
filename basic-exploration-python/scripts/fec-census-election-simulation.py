#!/usr/bin/env python

# FEC + 2010 US census data for 2012 election simulation


from __future__ import division
from collections import defaultdict
from collections import OrderedDict
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import pandas as pd
from matplotlib import rcParams
import matplotlib.cm as cm
import matplotlib as mpl
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score, accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_curve, precision_score, recall_score
import os


main_dir = \
 os.path.expanduser('~/GitHub/election-simulations/basic-exploration-python/data/')

# import data

data_file = 'obama-prediction-net-money-complete.csv'

obama_net_data = pd.read_csv(main_dir + data_file).set_index('state_name')
  
obama_net_data = obama_net_data.sort_index()

electoral_votes = \
pd.read_csv(main_dir + 'electoral_votes.csv').set_index('State')

electoral_votes = electoral_votes.sort_index()


#------------------------------------------------------------------------------ 
# general plot parameter setup

# Dark 2 scale from colorbrwer2

dark2_colors = \
  [(0.10588235294117647,0.6196078431372549,0.4666666666666667),
  (0.8509803921568627,0.37254901960784315,0.00784313725490196), 
  (0.4588235294117647,0.4392156862745098,0.7019607843137254), 
  (0.9058823529411765,0.1607843137254902,0.5411764705882353), 
  (0.4,0.6509803921568628,0.11764705882352941), 
  (0.9019607843137255,0.6705882352941176,0.00784313725490196), 
  (0.6509803921568628,0.4627450980392157,0.11372549019607843)]

rcParams['figure.figsize'] = (7, 4)
rcParams['figure.dpi'] = 150
rcParams['axes.color_cycle'] = dark2_colors
rcParams['lines.linewidth'] = 2
rcParams['axes.facecolor'] = 'white'
rcParams['font.size'] = 14
rcParams['patch.edgecolor'] = 'white'
rcParams['patch.facecolor'] = dark2_colors[0]
rcParams['font.family'] = 'Helvetica'


#------------------------------------------------------------------------------ 
# election simulation and plot functions


def simulate_election(model, n_sim, column):
    """simulate_election(model, n_sim, column)
    simulate_election creates a matrix of
    dimensions states x n_sim for a given column
    from a model (DataFrame with probabilities)"""
    prob_matrix = np.zeros((model.shape[0], n_sim))
    vote_matrix = np.zeros((model.shape[0], n_sim))
    np.random.RandomState(seed = 29393848)
    
    # generate wins
    for row, state in zip(xrange(prob_matrix.shape[0]), xrange(model.shape[0])):
        prob_matrix[row, :] = \
          np.random.binomial(n = 1, p = model.ix[state, column], size = (1, n_sim))
    
    # electoral college votes
    for row, state in zip(xrange(prob_matrix.shape[0]), xrange(model.shape[0])):
        vote_matrix[row, :] = \
          np.where(prob_matrix[row, :] >= 0.5, model.ix[state, 'Votes'], 0)
        
    return prob_matrix, vote_matrix


def plot_simulation(vote_totals, n_bins):
    """plot_simulation(vote_totals, n_bins)
    plot_simulation plots the results of the election simulations
    for n_bins of the distribution of vote toals"""
    win_sum = pd.Series(np.nansum(vote_totals, axis = 0))
    win_prob = sum(np.where(win_sum >= 269, 1, 0))/len(win_sum)
    rcParams['figure.figsize'] = (7, 4)
    rcParams['font.size'] = 10
    rcParams['font.family'] = 'Helvetica'
    spread = \
      np.abs(np.percentile(win_sum, q = 5) - np.percentile(win_sum, q = 95))
    win_sum.hist(bins = n_bins)
    plt.title('Chance of Obama victory: %f; spread: %d votes; %d bins' % \
               (win_prob, spread, n_bins))
    plt.xlabel('Obama Electoral College votes')
    plt.ylabel('Count')
    plt.axvline(269, color = 'k')
    plt.axvline(332, color = 'r', linestyle = '--')
    plt.legend(['winning threshold', '2012 outcome', 'simulation'], loc = 'best')
    pylab.show()
    
#------------------------------------------------------------------------------ 
# logistic regression to get probabilities and prediction errors for simulation


def prepare_features(data_frame, featureslist):
    """prepare_features(data_frame, featureslist)
    prepare_features prepares the features (predictors)
    in featureslist for a logistic regression
    that will calculate probability of winning.
    returns matrices y and X (target, coefficient matrix)""" 
    y = data_frame.Winner2008.values
    X = data_frame[featureslist].values
    if len(X.shape) == 1:
        X = X.reshape(-1, 1)
    return y, X

def fit_logistic(data_frame, featureslist, reg):
    """fit_logistic(data_frame, featureslist, reg)
    fit_logistic fits a logistic model with regularization
    parameter reg for the given data_frame
    and predictors in featureslist.
    returns final DataFrame and classifier"""
    y, X = prepare_features(data_frame, featureslist)
    clf2 = LogisticRegression(C = reg)
    clf2.fit(X, y)
    X_new = data_frame[featureslist]
    obama_probs = clf2.predict_proba(X_new)[:, 1]
    df = pd.DataFrame(index = data_frame.index)
    df['Obama'] = obama_probs
    return df, clf2

from sklearn.grid_search import GridSearchCV

def cv_optimize(data_frame, featureslist, n_folds, num_p):
    """cv_optimize(data_frame, featureslist, n_folds, num_p)
    cv_optimize fits the optimal parameters for the 
    parameters of the logistic function for the data
    in data_frame and predictors in features_list with
    n_folds folds and num_p points in the (log) space 
    for the grid search (C goes from -4 to 3 since
    the data are scaled).
    returns best parameters and best score"""
    y, X = prepare_features(data_frame, featureslist)
    clf = LogisticRegression()
    parameters = {'C':np.logspace(-4, 3, num = num_p)}
    gs = GridSearchCV(clf, param_grid = parameters, cv = n_folds)
    gs.fit(X, y)
    return gs.best_params_, gs.best_score_

def cv_and_fit(data_frame, featureslist, n_folds, num_p):
    """cv_and_fit(data_frame, featureslist, n_folds, num_p)
    cv_and_fit performs cross-validation on logistic fit
    for the data in data_frame for predictors in featureslist
    for n_folds and num_p in grid search.
    returns the prediction DataFrame and classifer results"""
    bp, bs = cv_optimize(data_frame, featureslist, n_folds = n_folds, num_p = num_p)
    predict, clf = fit_logistic(data_frame, featureslist, reg = bp['C'])
    return predict, clf


#------------------------------------------------------------------------------ 

# model predictors

# simple models with money and region

model0 = ['pctDollars', 'pop_density.scale']
model1 = ['pctDollars', 'economic_region_num']
model2 = ['pctDollars', 'census_region_num']
model3 = ['pctDollars', 'pop_density.scale', 'economic_region_num']
model4 = ['pctDollars', 'pop_density.scale', 'census_region_num']

# models that incorporate money, region, demographic information

model5 = ['pctDollars', 'pop_density.scale', 'economic_region_num', 'sex_ratio.scale']
model6 = ['pctDollars', 'pop_density.scale', 'census_region_num', 'sex_ratio.scale']

model7 = ['pctDollars', 'pop_density.scale', 'economic_region_num', 
          'sex_ratio.scale', 'under_18_count.scale']
model8 = ['pctDollars', 'pop_density.scale', 'census_region_num', 
          'sex_ratio.scale', 'under_18_count.scale']

model9 = ['pctDollars', 'pop_density.scale', 'economic_region_num', 
          'sex_ratio.scale', 'under_18_count.scale', 
          'forty_five_to_sixty_four_count.scale']
model10 = ['pctDollars', 'pop_density.scale', 'census_region_num', 
          'sex_ratio.scale', 'under_18_count.scale',
          'forty_five_to_sixty_four_count.scale']

model11 = ['pctDollars', 'pop_density.scale', 'economic_region_num', 
          'sex_ratio.scale', 'under_18_count.scale', 
          'forty_five_to_sixty_four_count.scale', 'sixty_five_over_count.scale']
model12 = ['pctDollars', 'pop_density.scale', 'census_region_num', 
          'sex_ratio.scale', 'under_18_count.scale',
          'forty_five_to_sixty_four_count.scale', 'sixty_five_over_count.scale']

model13 = ['pctDollars', 'pop_density.scale', 'economic_region_num', 
          'median_age.scale', 'sex_ratio.scale']
model14 = ['pctDollars', 'pop_density.scale', 'census_region_num', 
          'median_age.scale', 'sex_ratio.scale']

# models that incorporate money, region, household information

model15 = ['pctDollars', 'pop_density.scale', 'economic_region_num',
           'total_households.scale']
model16 = ['pctDollars', 'pop_density.scale', 'census_region_num',
           'total_households.scale']

model17 = ['pctDollars', 'pop_density.scale', 'economic_region_num',
           'husband_wife_household.scale']
model18 = ['pctDollars', 'pop_density.scale', 'census_region_num',
           'husband_wife_household.scale']

model19 = ['pctDollars', 'pop_density.scale', 'economic_region_num',
           'husband_wife_child_under_18.scale']
model20 = ['pctDollars', 'pop_density.scale', 'census_region_num',
           'husband_wife_child_under_18.scale']

model21 = ['pctDollars', 'pop_density.scale', 'economic_region_num',
           'female_household.scale']
model22 = ['pctDollars', 'pop_density.scale', 'census_region_num',
           'female_household.scale']

model23 = ['pctDollars', 'pop_density.scale', 'economic_region_num',
           'female_child_under_18.scale']
model24 = ['pctDollars', 'pop_density.scale', 'census_region_num',
           'female_child_under_18.scale']


model25 = ['pctDollars', 'pop_density.scale', 'economic_region_num',
           'male_household.scale']
model26 = ['pctDollars', 'pop_density.scale', 'census_region_num',
           'male_household.scale']

model27 = ['pctDollars', 'pop_density.scale', 'economic_region_num',
           'male_child_under_18.scale']
model28 = ['pctDollars', 'pop_density.scale', 'census_region_num',
           'male_child_under_18.scale']

model29 = ['pctDollars','pop_density.scale', 'economic_region_num',
                'one_person_nonfamily.scale', 'one_person_sixty_five_older.scale',
                'one_person_at_least_two.scale']

model30 = ['pctDollars','pop_density.scale', 'census_region_num',
                'one_person_nonfamily.scale', 'one_person_sixty_five_older.scale',
                'one_person_at_least_two.scale']

# omnibus household data goes here (does not converge in R or Julia without regularization)

model31 = ['pctDollars', 'pop_density.scale', 'economic_region_num', 
           'husband_wife_household.scale', 'female_household.scale', 
           'male_household.scale', 'one_person_nonfamily.scale',
           'one_person_sixty_five_older.scale', 'one_person_at_least_two.scale']

model32 = ['pctDollars', 'pop_density.scale', 'census_region_num', 
           'husband_wife_household.scale', 'female_household.scale', 
           'male_household.scale', 'one_person_nonfamily.scale',
           'one_person_sixty_five_older.scale', 'one_person_at_least_two.scale']

#------------------------------------------------------------------------------ 
# prediction, simulation and plotting

predict_model0, class_model0 = cv_and_fit(obama_net_data, model0, 10, 100)
predict_model0['Votes'] = electoral_votes.Votes
model0_prob, model0_votes = simulate_election(predict_model0, 1e6+1, 'Obama')
plot_simulation(model0_votes, 30)


predict_model1, class_model1 = cv_and_fit(obama_net_data, model1, 10, 100)
predict_model1['Votes'] = electoral_votes.Votes
model1_prob, model1_votes = simulate_election(predict_model1, 1e6+1, 'Obama')
plot_simulation(model1_votes, 30)



predict_model2, class_model2 = cv_and_fit(obama_net_data, model2, 10, 100)
predict_model2['Votes'] = electoral_votes.Votes
model2_prob, model2_votes = simulate_election(predict_model2, 1e6+1, 'Obama')
plot_simulation(model2_votes, 30)


predict_model3, class_model3 = cv_and_fit(obama_net_data, model3, 10, 100)
predict_model3['Votes'] = electoral_votes.Votes
model3_prob, model3_votes = simulate_election(predict_model3, 1e6+1, 'Obama')
plot_simulation(model3_votes, 30)



predict_model4, class_model4 = cv_and_fit(obama_net_data, model4, 10, 100)
predict_model4['Votes'] = electoral_votes.Votes
model4_prob, model4_votes = simulate_election(predict_model4, 1e6+1, 'Obama')
plot_simulation(model4_votes, 30)


predict_model5, class_model5 = cv_and_fit(obama_net_data, model5, 10, 100)
predict_model5['Votes'] = electoral_votes.Votes
model5_prob, model5_votes = simulate_election(predict_model5, 1e6+1, 'Obama')
plot_simulation(model5_votes, 30)


predict_model6, class_model6 = cv_and_fit(obama_net_data, model6, 10, 100)
predict_model6['Votes'] = electoral_votes.Votes
model6_prob, model6_votes = simulate_election(predict_model6, 1e6+1, 'Obama')
plot_simulation(model6_votes, 30)


predict_model7, class_model7 = cv_and_fit(obama_net_data, model7, 10, 100)
predict_model7['Votes'] = electoral_votes.Votes
model7_prob, model7_votes = simulate_election(predict_model7, 1e6+1, 'Obama')
plot_simulation(model7_votes, 30)


predict_model8, class_model8 = cv_and_fit(obama_net_data, model8, 10, 100)
predict_model8['Votes'] = electoral_votes.Votes
model8_prob, model8_votes = simulate_election(predict_model8, 1e6+1, 'Obama')
plot_simulation(model8_votes, 30)


predict_model9, class_model9 = cv_and_fit(obama_net_data, model9, 10, 100)
predict_model9['Votes'] = electoral_votes.Votes
model9_prob, model9_votes = simulate_election(predict_model9, 1e6+1, 'Obama')
plot_simulation(model9_votes, 30)


predict_model10, class_model10 = cv_and_fit(obama_net_data, model10, 10, 100)
predict_model10['Votes'] = electoral_votes.Votes
model10_prob, model10_votes = simulate_election(predict_model10, 1e6+1, 'Obama')
plot_simulation(model10_votes, 30)


predict_model11, class_model11 = cv_and_fit(obama_net_data, model11, 10, 100)
predict_model11['Votes'] = electoral_votes.Votes
model11_prob, model11_votes = simulate_election(predict_model11, 1e6+1, 'Obama')
plot_simulation(model11_votes, 30)


predict_model12, class_model12 = cv_and_fit(obama_net_data, model12, 10, 100)
predict_model12['Votes'] = electoral_votes.Votes
model12_prob, model12_votes = simulate_election(predict_model12, 1e6+1, 'Obama')
plot_simulation(model12_votes, 30)


predict_model13, class_model13 = cv_and_fit(obama_net_data, model13, 10, 100)
predict_model13['Votes'] = electoral_votes.Votes
model13_prob, model13_votes = simulate_election(predict_model13, 1e6+1, 'Obama')
plot_simulation(model13_votes, 30)


predict_model14, class_model14 = cv_and_fit(obama_net_data, model14, 10, 100)
predict_model14['Votes'] = electoral_votes.Votes
model14_prob, model14_votes = simulate_election(predict_model14, 1e6+1, 'Obama')
plot_simulation(model14_votes, 30)


predict_model15, class_model15 = cv_and_fit(obama_net_data, model15, 10, 100)
predict_model15['Votes'] = electoral_votes.Votes
model15_prob, model15_votes = simulate_election(predict_model15, 1e6+1, 'Obama')
plot_simulation(model15_votes, 30)


predict_model16, class_model16 = cv_and_fit(obama_net_data, model16, 10, 100)
predict_model16['Votes'] = electoral_votes.Votes
model16_prob, model16_votes = simulate_election(predict_model16, 1e6+1, 'Obama')
plot_simulation(model16_votes, 30)


predict_model17, class_model17 = cv_and_fit(obama_net_data, model17, 10, 100)
predict_model17['Votes'] = electoral_votes.Votes
model17_prob, model17_votes = simulate_election(predict_model17, 1e6+1, 'Obama')
plot_simulation(model17_votes, 30)


predict_model18, class_model18 = cv_and_fit(obama_net_data, model18, 10, 100)
predict_model18['Votes'] = electoral_votes.Votes
model18_prob, model18_votes = simulate_election(predict_model18, 1e6+1, 'Obama')
plot_simulation(model18_votes, 30)


predict_model19, class_model19 = cv_and_fit(obama_net_data, model19, 10, 100)
predict_model19['Votes'] = electoral_votes.Votes
model19_prob, model19_votes = simulate_election(predict_model19, 1e6+1, 'Obama')
plot_simulation(model19_votes, 30)


predict_model20, class_model20 = cv_and_fit(obama_net_data, model20, 10, 100)
predict_model20['Votes'] = electoral_votes.Votes
model20_prob, model20_votes = simulate_election(predict_model20, 1e6+1, 'Obama')
plot_simulation(model20_votes, 30)


predict_model21, class_model21 = cv_and_fit(obama_net_data, model21, 10, 100)
predict_model21['Votes'] = electoral_votes.Votes
model21_prob, model21_votes = simulate_election(predict_model21, 1e6+1, 'Obama')
plot_simulation(model21_votes, 30)


predict_model22, class_model22 = cv_and_fit(obama_net_data, model22, 10, 100)
predict_model22['Votes'] = electoral_votes.Votes
model22_prob, model22_votes = simulate_election(predict_model22, 1e6+1, 'Obama')
plot_simulation(model22_votes, 30)


predict_model23, class_model23 = cv_and_fit(obama_net_data, model23, 10, 100)
predict_model23['Votes'] = electoral_votes.Votes
model23_prob, model23_votes = simulate_election(predict_model23, 1e6+1, 'Obama')
plot_simulation(model23_votes, 30)


predict_model24, class_model24 = cv_and_fit(obama_net_data, model24, 10, 100)
predict_model24['Votes'] = electoral_votes.Votes
model24_prob, model24_votes = simulate_election(predict_model24, 1e6+1, 'Obama')
plot_simulation(model24_votes, 30)


predict_model25, class_model25 = cv_and_fit(obama_net_data, model25, 10, 100)
predict_model25['Votes'] = electoral_votes.Votes
model25_prob, model25_votes = simulate_election(predict_model25, 1e6+1, 'Obama')
plot_simulation(model25_votes, 30)


predict_model26, class_model26 = cv_and_fit(obama_net_data, model26, 10, 100)
predict_model26['Votes'] = electoral_votes.Votes
model26_prob, model26_votes = simulate_election(predict_model26, 1e6+1, 'Obama')
plot_simulation(model26_votes, 30)


predict_model27, class_model27 = cv_and_fit(obama_net_data, model27, 10, 100)
predict_model27['Votes'] = electoral_votes.Votes
model27_prob, model27_votes = simulate_election(predict_model27, 1e6+1, 'Obama')
plot_simulation(model27_votes, 30)


predict_model28, class_model28 = cv_and_fit(obama_net_data, model28, 10, 100)
predict_model28['Votes'] = electoral_votes.Votes
model28_prob, model28_votes = simulate_election(predict_model28, 1e6+1, 'Obama')
plot_simulation(model28_votes, 30)


predict_model29, class_model29 = cv_and_fit(obama_net_data, model29, 10, 100)
predict_model29['Votes'] = electoral_votes.Votes
model29_prob, model29_votes = simulate_election(predict_model29, 1e6+1, 'Obama')
plot_simulation(model29_votes, 30)


predict_model30, class_model30 = cv_and_fit(obama_net_data, model30, 10, 100)
predict_model30['Votes'] = electoral_votes.Votes
model30_prob, model30_votes = simulate_election(predict_model30, 1e6+1, 'Obama')
plot_simulation(model30_votes, 30)


predict_model31, class_model31 = cv_and_fit(obama_net_data, model31, 10, 100)
predict_model31['Votes'] = electoral_votes.Votes
model31_prob, model31_votes = simulate_election(predict_model31, 1e6+1, 'Obama')
plot_simulation(model31_votes, 30)


predict_model32, class_model32 = cv_and_fit(obama_net_data, model32, 10, 100)
predict_model32['Votes'] = electoral_votes.Votes
model32_prob, model32_votes = simulate_election(predict_model32, 1e6+1, 'Obama')
plot_simulation(model32_votes, 30)


#------------------------------------------------------------------------------ 
# confusion matrices, accuracy scores, classification reports

# confusion matrix: predict on classifier, features


# writing to summary file:
# create lists of predictions from classifier
# loop over predictions and print matrices to summary file

classifier_list = \
  [class_model0, class_model1, class_model2, class_model3, class_model4,
   class_model5, class_model6, class_model7, class_model8, class_model9,
   class_model10, class_model11, class_model12, class_model13, class_model14,
   class_model15, class_model16, class_model17, class_model18, class_model19,
   class_model20, class_model21, class_model22, class_model23, class_model24,
   class_model25, class_model26, class_model27, class_model28, class_model29,
   class_model30, class_model31, class_model32]

model_list = \
  [model0, model1, model2, model3, model4,
   model5, model6, model7, model8, model9,
   model10, model11, model12, model13, model14,
   model15, model16, model17, model18, model19,
   model20, model21, model22, model23, model24,
   model25, model26, model27, model28, model29,
   model30, model31, model32]
  
classifier_performance_dict = OrderedDict()

# create dict of classifier performance
for class_result, model_call in zip(classifier_list, model_list):
    classifier_performance_dict[str(model_call)] = \
      class_result.predict(obama_net_data[model_call])


results_2012 = obama_net_data.winner_binary

# create file with printed output of classifier results

output_dir = \
 os.path.expanduser('~/GitHub/election-simulations/basic-exploration-python/output/')

filename = 'obama-net-money-summary'
summary_file = open(output_dir + filename + '.class_result', 'w')

summary_file.write('Classifier results for Obama net money'  + '\n')
for class_result, idx in zip(classifier_performance_dict, xrange(len(classifier_performance_dict))):
    print >> summary_file, 'Predictors: ', classifier_performance_dict.keys()[idx], '\n'
    print >> summary_file, 'Accuracy: ' , \
      accuracy_score(results_2012, classifier_performance_dict[class_result]), '\n'
    print >> summary_file, 'Confusion matrix\n', \
      confusion_matrix(results_2012, classifier_performance_dict[class_result]), '\n'
    print >> summary_file, 'row = expected, col = predicted', '\n'
    print >> summary_file, 'F1 score: ', \
      f1_score(results_2012, classifier_performance_dict[class_result]), '\n'
    print >> summary_file, 'Precision score: ', \
      precision_score(results_2012, classifier_performance_dict[class_result]), '\n'
    print >> summary_file, 'Recall score: ', \
      recall_score(results_2012, classifier_performance_dict[class_result]), '\n'
    print >> summary_file, \
      classification_report(results_2012, classifier_performance_dict[class_result]), '\n'
    print >> summary_file, '-' * 77

summary_file.close()


# prediction accuracy

model_prediction_mtx = np.zeros((51, len(classifier_list)))

for col, model, classifier in zip(xrange(51), model_list, classifier_list):
    model_prediction_mtx[:, col] = classifier.predict(obama_net_data[model])
   
# DataFrame with prediction results (goes into Google map)

model_names = \
  ['model0', 'model1', 'model2', 'model3', 'model4',
   'model5', 'model6', 'model7', 'model8', 'model9',
   'model10', 'model11', 'model12', 'model13', 'model14',
   'model15', 'model16', 'model17', 'model18', 'model19',
   'model20', 'model21', 'model22', 'model23', 'model24',
   'model25', 'model26', 'model27', 'model28', 'model29',
   'model30', 'model31', 'model32']
    
classifier_results = \
  pd.DataFrame(np.zeros((51, len(model_list))), 
               columns = model_names, index = list(obama_net_data.index.values))


for model, col in zip(model_names, xrange(33)):
    for ind in xrange(50):
        if model_prediction_mtx[ind, col] == results_2012[ind]:
            classifier_results.ix[ind, model] = 1
        else:
            classifier_results.ix[ind, model] = 0
            

classifier_results.to_csv(output_dir + 'net-money-classifier-success.csv')

# DataFrame with classifier probabilities

predict_names = \
  ['predict_model0', 'predict_model1', 'predict_model2', 'predict_model3',
   'predict_model4', 'predict_model5', 'predict_model6', 'predict_model7',
   'predict_model8', 'predict_model9', 'predict_model10', 'predict_model11', 
   'predict_model12', 'predict_model13', 'predict_model14', 'predict_model15',
   'predict_model16', 'predict_model17', 'predict_model18', 'predict_model19',
   'predict_model20', 'predict_model21', 'predict_model22', 'predict_model23',
   'predict_model24', 'predict_model25', 'predict_model26', 'predict_model27',
   'predict_model28', 'predict_model29', 'predict_model30', 'predict_model31',
    'predict_model32']
  

predict_list = \
  [predict_model0, predict_model1, predict_model2, predict_model3, predict_model4,
   predict_model5, predict_model6, predict_model7, predict_model8, predict_model9,
   predict_model10, predict_model11, predict_model12, predict_model13, predict_model14,
   predict_model15, predict_model16, predict_model17, predict_model18, predict_model19,
   predict_model20, predict_model21, predict_model22, predict_model23, predict_model24,
   predict_model25, predict_model26, predict_model27, predict_model28, predict_model29,
   predict_model30, predict_model31, predict_model32]
  
probability_results = \
  pd.DataFrame(np.zeros((51, len(predict_list))), 
               columns = predict_names, index = list(obama_net_data.index.values))


for model, prediction in zip(predict_names, predict_list):
    probability_results[model] = prediction.Obama.values
    
probability_results.to_csv(output_dir + 'net-money-probabilities.csv')