from math import log

from ..helpers.summary import CategorySummary

def test_constructor():
  instance = CategorySummary('foo')
  assert isinstance(instance, CategorySummary)

def test_add_day():
  summary = CategorySummary('foo')
  summary.add_day(1, 5)
  assert summary.days[1]['count'] == 5

def test_add_day_count_too_small():
  summary = CategorySummary('foo')
  summary.add_day(2,4)
  assert summary.days.get(2) == None

def test_report_exponential():
  summary = CategorySummary('foo')
  summary.add_day(1, 5)
  summary.add_day(2, 6)
  summary.add_day(3, 7)
  summary.add_day(4, 9)
  summary.add_day(5, 10)
  summary.add_day(6, 12)
  summary.add_day(7, 15)
  summary.add_day(8, 18)
  summary.add_day(9, 21)
  summary.add_day(10, 25)
  summary.add_day(11, 30)
  report = summary.report()
  assert report.overall.ratio >= 1.19
  assert report.overall.ratio <= 1.21
  assert report.overall.r2 >= 0.99
  assert report.location == 'foo'
  assert report.count == 30
  assert report.last_week_deltas.slope >= 0.3
  assert report.last_week_deltas.r2 >= 0.9

def test_report_logistic():
  summary = CategorySummary('foo')
  summary.add_day(2, 6)
  summary.add_day(3, 7)
  summary.add_day(4, 8)
  summary.add_day(5, 9)
  summary.add_day(6, 11)
  summary.add_day(7, 13)
  summary.add_day(8, 14)
  summary.add_day(9, 16)
  summary.add_day(10, 18)
  summary.add_day(11, 20)
  summary.add_day(12, 23)
  summary.add_day(13, 25)
  summary.add_day(14, 27)
  summary.add_day(15, 30)
  summary.add_day(16, 32)
  report = summary.report()
  assert report.overall.ratio >= 1.1
  assert report.overall.r2 >= 0.98
  assert report.location == 'foo'
  assert report.count == 32
  assert report.last_week_deltas.slope < 0.05 # logistic model should display a small second derivative near inflection
  assert report.last_week_deltas.r2 < 0.1 # regression on a flat line will have a small r

def test_missing_days():
  summary = CategorySummary('foo')
  summary.add_day(0, 1)
  report = summary.report()
  assert report.count == 0
