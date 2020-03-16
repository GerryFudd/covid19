from ..helpers.regression import exponential_regression

def test_basic_case():
  result = exponential_regression([(0, 2), (1, 8), (2, 32)])
  assert result[0] == 2
  assert result[1] == 4
  assert result[2] == 1
