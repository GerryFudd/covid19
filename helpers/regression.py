from functools import reduce
from math import log2

def sum(num_list):
  return reduce(
    lambda acc, num: acc + num,
    num_list
  )

def linear_regression(sample):
  if len(sample) == 0:
    return 0, 0, None
  if len(sample) == 1:
    return sample[0][1], 0, None
  # The best fit line a + bx = y for a list of pairs [(x_1, y_1),...,(x_n,y_n)]
  # relies on the following sums.
  # sum_xy = sum(x_iy_i)
  sum_xy = sum(list(map(lambda pair: pair[0] * pair[1], sample)))
  # sum_xx = sum(x_i^2)
  sum_xx = sum(list(map(lambda pair: pair[0] ** 2, sample)))
  # sum_x = sum(x_i)
  sum_x = sum(list(map(lambda pair: pair[0], sample)))
  # sum_y = sum(y_i)
  sum_y = sum(list(map(lambda pair: pair[1], sample)))
  # The formulas are
  # a = (sum_x sum_xy - sum_y sum_xx)/(sum_x^2 - n sum_xx)
  # b = (sum_x sum_y - n sum_xy)/(sum_x^2 - n sum_xx)
  # common denominator
  denom = sum_x ** 2 - len(sample) * sum_xx
  # numerator for a
  num_a = sum_x * sum_xy - sum_y * sum_xx
  # numerator for b
  num_b = sum_x * sum_y - len(sample) * sum_xy

  # The so called "Goodness of fit" for a linear regression is based on the relationship of three values.
  # SS_tot (the total sum of squares) is the variance of y_i from mean(y) = [y_1,...,y_n]/n with formula
  # SS_tot = sum((y_i - mean(y))^2)
  ss_tot = sum(list(map(lambda pair: (pair[1] - sum_y / len(sample)) ** 2, sample)))
  if ss_tot == 0: # if ss_tot is zero, then there is no variance in y values. This means that the horizontal line y_1 = y is a perfect fit.
    return sample[0][1], 0, 1
  # It is a measure of the overall variance in the output variables.

  # SS_reg (the sum of squares for the regression line) is the total
  # variance of a + b x_i from mean(y) with the formula
  # SS_reg = sum((a + b x_i - mean(y))^2)
  ss_reg = sum(list(map(lambda pair: (num_a / denom + num_b / denom * pair[0] - sum_y / len(sample)) ** 2, sample)))

  # SS_err (the sum of squares of the error of the regression model) is
  # the total variance of y_i from a + b x_i with the formula
  # SS_err = sum((a + b x_i - y_i)^2)
  # It turns out that SS_err + SS_reg = SS_tot. And the familiar
  # R^2 value that is reported with a linear regression model is
  # R^2 = SS_reg/SS_tot = 1 - SS_err/SS_tot
  # The formula for a and b provided above provide the line that
  # minimizes SS_err. The value SS_reg/SS_tot is essentially
  # the fraction of the variation in y_i that can be explained
  # by the linear dependence of y_i on x_i
  return num_a / denom, num_b / denom, ss_reg / ss_tot

def exponential_regression(sample):
  log_sample = list(map(lambda point: (point[0], log2(point[1])), sample))
  log_linear_regression = linear_regression(log_sample)
  return 2 ** log_linear_regression[0], 2 ** log_linear_regression[1], log_linear_regression[2]
