from ..helpers.summary import CategorySummary
from .fixtures import basic_dataframe, exponential_dataframe, logistic_dataframe, small_value_dataframe

def test_constructor(basic_dataframe):
  instance = CategorySummary('foo', basic_dataframe)
  assert isinstance(instance, CategorySummary)

def test_resulting_dataframe(basic_dataframe):
  summary = CategorySummary('World', basic_dataframe)
  print('summary.dataframe')
  print(summary.dataframe)
  assert summary.dataframe.shape == (1, 1)
  assert list(summary.dataframe.columns) == ['count']

def test_report_exponential(exponential_dataframe):
  summary = CategorySummary('foo', exponential_dataframe)
  report = summary.report()
  assert report.overall.ratio >= 1.19
  assert report.overall.ratio <= 1.21
  assert report.overall.r2 >= 0.99
  assert report.location == 'foo'
  assert report.count == 3715
  assert report.days == 11
  assert report.last_week_daily_new_cases.slope > 64 # daily new cases is within 90% of expected
  assert report.last_week_daily_new_cases.expected_slope > 71 # predict slope from middle of last week
  assert report.last_week_daily_new_cases.expected_slope < 72 # predict slope from middle of last week
  assert report.last_week_daily_new_cases.r2 >= 0.9

def test_report_logistic(logistic_dataframe):
  summary = CategorySummary('foo', logistic_dataframe)
  report = summary.report()
  assert report.overall.ratio >= 1.1
  assert report.overall.r2 >= 0.98
  assert report.location == 'foo'
  assert report.count == 2951
  assert report.days == 16
  assert report.last_week_daily_new_cases.slope < 7.5 # logistic model should display a small second derivative near inflection
  assert report.last_week_daily_new_cases.expected_slope > 38 # expected slope based on exponential model should be larger
  assert report.last_week_daily_new_cases.expected_slope < 39

def test_missing_days(small_value_dataframe):
  summary = CategorySummary('foo', small_value_dataframe)
  report = summary.report()
  assert report.count == 0
