from pandas import DataFrame
from functools import reduce

from ..helpers.regression import linear_regression
def sum(num_list):
  return reduce(
    lambda acc, num: acc + num,
    num_list
  )
def test_empty_list():
  assert linear_regression([], []) == (0, 0, None)

def test_singleton_list():
  assert linear_regression([7], [28]) == (28, 0, None)

def test_two_ponts():
  inputs = [3, 7]
  outputs = [2, 5]
  result = linear_regression(inputs, outputs)
  assert result[0] + result[1] * inputs[0] == outputs[0]
  assert result[0] + result[1] * inputs[1] == outputs[1]
  assert result[2] == 1

def test_three_non_collinear():
  inputs = [0, 1, 2]
  outputs = [0, 1, 3]
  result = linear_regression(inputs, outputs)
  # Check that the r^2 value is high enough
  assert result[2] > 0.96
  # Check that the error in the regression is as small as the r^2 value says it is
  error = 0
  i = 0
  while i < len(inputs):
    error += (result[0] + result[1] * inputs[i] - outputs[i]) ** 2
    i += 1
  
  avg_y = sum(outputs) / len(outputs)
  ss_tot = sum(list(map(
    lambda output: (output - avg_y) ** 2, outputs
  )))
  assert error / ss_tot < 0.04

def test_no_variance():
  result = linear_regression([0, 2, 3, 15], [5, 5, 5, 5])
  assert result[0] == 5
  assert result[1] == 0
  assert result[2] == 1
