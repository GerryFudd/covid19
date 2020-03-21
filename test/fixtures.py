from pytest import fixture
from pandas import DataFrame

from ..helpers.summary import CategorySummary

def make_dataframe(data_as_dict):
  data_as_list = []
  for key in data_as_dict:
    for pair in data_as_dict[key]:
      data_as_list.append({'location': key, 'day': pair[0], 'count': pair[1]})
  return DataFrame(data_as_list)

@fixture
def basic_dataframe():
  return make_dataframe({'World': [(0, 15)], 'United States': [(0, 5)]})

@fixture
def exponential_dataframe():
  return make_dataframe({'foo': [
    (6, 600),
    (7, 720),
    (8, 864),
    (9, 1034),
    (10, 1244),
    (11, 1493),
    (12, 1792),
    (13, 2150),
    (14, 2580),
    (15, 3096),
    (16, 3715)
  ]})

@fixture
def logistic_dataframe():
  return make_dataframe({'foo': [
    (1, 427),
    (2, 504),
    (3, 593),
    (4, 695),
    (5, 812),
    (6, 943),
    (7, 1091),
    (8, 1254),
    (9, 1433),
    (10, 1627),
    (11, 1833),
    (12, 2049),
    (13, 2273),
    (14, 2500),
    (15, 2727),
    (16, 2951)
  ]})

@fixture
def small_value_dataframe():
  return make_dataframe({'foo': [(0, 1)]})

@fixture
def category_summary_exponential():
  return CategorySummary('foo', make_dataframe({'foo': [
    (1, 8),
    (2, 12),
    (3, 18),
    (4, 27)
  ]}))

@fixture
def category_summary_in_slowdown():
  return CategorySummary('bar', make_dataframe({'bar': [
    (1, 427),
    (2, 504),
    (3, 593),
    (4, 695),
    (5, 812),
    (6, 943),
    (7, 1091),
    (8, 1254),
    (9, 1433),
    (10, 1627),
    (11, 1833),
    (12, 2049),
    (13, 2273),
    (14, 2500),
    (15, 2727),
    (16, 2951)
  ]}))

@fixture
def small_category_summary():
  return CategorySummary('foo', make_dataframe({'foo': [
    (1, 8),
    (2, 12)
  ]}))
