from ..helpers.regression import exponential_regression

def test_basic_case():
  result = exponential_regression([0, 1, 2], [2, 8, 32])
  assert round(result[0], 10) == 2
  assert round(result[1], 10) == 4
  assert result[2] == 1
