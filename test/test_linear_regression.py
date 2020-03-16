from ..helpers.regression import linear_regression, sum

def test_empty_list():
  assert linear_regression([]) == (0, 0, None)

def test_singleton_list():
  assert linear_regression([(7, 28)]) == (28, 0, None)

def test_two_ponts():
  point1 = (3, 2)
  point2 = (7, 5)
  result = linear_regression([point1, point2])
  assert result[0] + result[1] * point1[0] == point1[1]
  assert result[0] + result[1] * point2[0] == point2[1]
  assert result[2] == 1

def test_three_non_collinear():
  sample = [(0, 0), (1, 1), (2, 3)]
  result = linear_regression(sample)
  # Check that the r^2 value is high enough
  assert result[2] > 0.96
  # Check that the error in the regression is as small as the r^2 value says it is
  error = sum(list(map(
    lambda pair: (result[0] + result[1] * pair[0] - pair[1]) ** 2,
    sample
  )))
  avg_y = sum(list(map(lambda pair: pair[1], sample))) / len(sample)
  ss_tot = sum(list(map(
    lambda pair: (pair[1] - avg_y) ** 2, sample
  )))
  assert error / ss_tot < 0.04

def test_no_variance():
  result = linear_regression([(0,5), (2, 5), (3, 5), (15, 5)])
  assert result[0] == 5
  assert result[1] == 0
  assert result[2] == 1
