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
  summary.add_day(6, 600)
  summary.add_day(7, 720)
  summary.add_day(8, 864)
  summary.add_day(9, 1034)
  summary.add_day(10, 1244)
  summary.add_day(11, 1493)
  summary.add_day(12, 1792)
  summary.add_day(13, 2150)
  summary.add_day(14, 2580)
  summary.add_day(15, 3096)
  summary.add_day(16, 3715)
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

def test_report_logistic():
  summary = CategorySummary('foo')
  summary.add_day(1, 427)
  summary.add_day(2, 504)
  summary.add_day(3, 593)
  summary.add_day(4, 695)
  summary.add_day(5, 812)
  summary.add_day(6, 943)
  summary.add_day(7, 1091)
  summary.add_day(8, 1254)
  summary.add_day(9, 1433)
  summary.add_day(10, 1627)
  summary.add_day(11, 1833)
  summary.add_day(12, 2049)
  summary.add_day(13, 2273)
  summary.add_day(14, 2500)
  summary.add_day(15, 2727)
  summary.add_day(16, 2951)
  report = summary.report()
  assert report.overall.ratio >= 1.1
  assert report.overall.r2 >= 0.98
  assert report.location == 'foo'
  assert report.count == 2951
  assert report.days == 16
  assert report.last_week_daily_new_cases.slope < 7.5 # logistic model should display a small second derivative near inflection
  assert report.last_week_daily_new_cases.expected_slope > 38 # logistic model should display a small second derivative near inflection
  assert report.last_week_daily_new_cases.expected_slope < 39 # logistic model should display a small second derivative near inflection

def test_missing_days():
  summary = CategorySummary('foo')
  summary.add_day(0, 1)
  report = summary.report()
  assert report.count == 0
