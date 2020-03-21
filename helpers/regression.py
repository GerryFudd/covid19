from math import log2
from sklearn.linear_model import LinearRegression
from pandas import DataFrame

def make_list_of_lists(lst):
  return list(map(lambda x: [x], lst))

def linear_regression(independent_arg, dependent):
  independent = make_list_of_lists(independent_arg)
  if len(independent) == 1 and len(dependent) == 1:
    return dependent[0], 0, None
  try:
    fit_result = LinearRegression().fit(DataFrame(independent), DataFrame(dependent))
    score = fit_result.score(independent, dependent)
    return fit_result.intercept_[0], fit_result.coef_[0][0], score
  except ValueError as e:
    print(e)
    return 0, 0, None

def exponential_regression(independent, dependent):
  log_dependents = list(map(log2, dependent))
  log_linear_regression = linear_regression(independent, log_dependents)
  return 2 ** log_linear_regression[0], 2 ** log_linear_regression[1], log_linear_regression[2]
