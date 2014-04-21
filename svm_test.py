import logging
import numpy as np
from optparse import OptionParser
import sys
from time import time
import pylab as pl
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.svm import LinearSVC
from sms_query_1 import input_from_xml
from sklearn import svm


class L1LinearSVC(LinearSVC):
    def fit(self, X, y):
        self.transformer_ = LinearSVC(penalty="l1",
                                      dual=False, tol=1e-3)
        X = self.transformer_.fit_transform(X, y)
        return LinearSVC.fit(self, X, y)

    def predict(self, X):
        X = self.transformer_.transform(X)
        return LinearSVC.predict(self, X)

class extract_data():
    def extract_training_data(self):
        obj = input_from_xml()
        domains,questions = obj.fetch_input_from_xml_questions()
        train_target_names = domains
        train_data = []
        train_target = []
        for i in range(0,len(domains)):
          for quest in questions[domains[i]]:
            train_data.append(quest)
            train_target.append(i)
        return train_data,train_target,train_target_names

    def extract_testing_data(self):
      obj = input_from_xml()
      questions = obj.fetch_sms_queries()
      
      test_data = []
      test_target = []
      test_target_names = []

      for domain,quest,indomain in questions:
        if domain not in test_target_names:
          test_target_names.append(domain)

      for domain,quest,indomain in questions:
        if domain:
            test_target.append(test_target_names.index(domain))
            test_data.append(quest)
        else:
            test_target.append(-1)
            test_data.append(quest)

      return test_data,test_target


def main_function():
  # Display progress logs on stdout
  logging.basicConfig(level=logging.INFO,
                      format='%(asctime)s %(levelname)s %(message)s')


  # parse commandline arguments
  op = OptionParser()
  op.add_option("--report",
                action="store_true", dest="print_report",
                help="Print a detailed classification report.")
  op.add_option("--chi2_select",
                action="store", type="int", dest="select_chi2",
                help="Select some number of features using a chi-squared test")
  op.add_option("--confusion_matrix",
                action="store_true", dest="print_cm",
                help="Print the confusion matrix.")
  op.add_option("--top10",
                action="store_true", dest="print_top10",
                help="Print ten most discriminative terms per class"
                     " for every classifier.")
  op.add_option("--all_categories",
                action="store_true", dest="all_categories",
                help="Whether to use all categories or not.")
  op.add_option("--use_hashing",
                action="store_true",
                help="Use a hashing vectorizer.")
  op.add_option("--n_features",
                action="store", type=int, default=2 ** 16,
                help="n_features when using the hashing vectorizer.")
  op.add_option("--filtered",
                action="store_true",
                help="Remove newsgroup information that is easily overfit: "
                     "headers, signatures, and quoting.")
  (opts, args) = op.parse_args()
  if len(args) > 0:
      op.error("this script takes no arguments.")
      sys.exit(1)

  print(__doc__)
  op.print_help()
  print()


  ###############################################################################
  # Load some categories from the training set
  if opts.all_categories:
      categories = None
  else:
      obj = input_from_xml()
      domains,questions = obj.fetch_input_from_xml_questions()
      categories = domains

  print("Loading Data from different categories....")
  print(categories if categories else "all")


  obj = extract_data()
  train_data,train_target,train_target_names = obj.extract_training_data()
  test_data,test_target = obj.extract_testing_data()


  print('data loaded')
#  print train_target_names

  def size_mb(docs):
    return sum(len(s.encode('utf-8')) for s in docs) / 1e6

  data_train_size_mb = size_mb(train_data)
  data_test_size_mb = size_mb(test_data)

  print("%d documents - %0.3fMB (training set)" % (
     len(train_data), data_train_size_mb))
  print("%d documents - %0.3fMB (test set)" % (
     len(test_data), data_test_size_mb))
  print("%d categories" % len(categories))
  print()


  categories = train_target_names 
  y_train,y_test = train_target,test_target

  print("Extracting features from the training dataset using a sparse vectorizer")
  t0 = time()
  if opts.use_hashing:
      vectorizer = HashingVectorizer(stop_words='english', non_negative=True,
                                     n_features=opts.n_features)
      X_train = vectorizer.transform(train_data)
  else:
      vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,
                                   stop_words='english')
      X_train = vectorizer.fit_transform(train_data)
  duration = time() - t0
  print("done in %fs at %0.3fMB/s" % (duration, data_train_size_mb / duration))
  print("n_samples: %d, n_features: %d" % X_train.shape)
  print()

  print("Extracting features from the test dataset using the same vectorizer")
  t0 = time()
  X_test = vectorizer.transform(test_data)
  duration = time() - t0
  print("done in %fs at %0.3fMB/s" % (duration, data_test_size_mb / duration))
  print("n_samples: %d, n_features: %d" % X_test.shape)
  print()


  if opts.select_chi2:
      print("Extracting %d best features by a chi-squared test" %
            opts.select_chi2)
      t0 = time()
      ch2 = SelectKBest(chi2, k=opts.select_chi2)
      X_train = ch2.fit_transform(X_train, y_train)
      X_test = ch2.transform(X_test)
      print("done in %fs" % (time() - t0))
      print()

  def trim(s):
      """Trim string to fit on terminal (assuming 80-column display)"""
      return s if len(s) <= 80 else s[:77] + "..."

  if opts.use_hashing:
      feature_names = None
  else:
      feature_names = np.asarray(vectorizer.get_feature_names())

  print('_' * 80)
  print("Training the data: ")
  t0 = time()
  clf = LinearSVC()
  clf.fit(X_train,y_train)
  train_time = time() - t0
  print("train time: %0.3fs" % train_time)

  t0 = time()
  pred = clf.predict(X_test)
  scores = clf.decision_function(X_test)
  test_time = time() - t0
  print("test time:  %0.3fs" % test_time)
#  print scores[0]
  return test_data, pred, y_test, scores, train_target_names

'''
  for i in range(0,10):
      print "quest: ",test_data[i]
      print "Given class: %s" %(train_target_names[y_test[i]])
      print "Predicted class: %s" %(train_target_names[pred[i]]) 
      print "#####################"


#  to calculate efficiency
  cnt = 0
  cnt2 = 0
  for i in range(0,len(y_test)):
    if y_test[i]!=-1:
      if pred[i] == y_test[i]:
        cnt = cnt + 1
      cnt2 = cnt2 + 1

  print cnt,cnt2
  print "efficiency of classification is: %f" %((cnt + len(y_test) - cnt2)/(1.0*len(y_test))*100)
'''

if __name__ == "__main__":
  main_function()
