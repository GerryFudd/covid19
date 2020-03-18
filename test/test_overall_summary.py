from pytest import fixture
from ..helpers.summary import OverallSummary, CategorySummary, CategoryReport

@fixture
def category_summary_exponential():
  category_summary = CategorySummary('foo')
  category_summary.add_day(1, 8)
  category_summary.add_day(2, 12)
  category_summary.add_day(3, 18)
  category_summary.add_day(4, 27)
  return category_summary

@fixture
def category_summary_in_slowdown():
  category_summary = CategorySummary('bar')
  category_summary.add_day(1, 427)
  category_summary.add_day(2, 504)
  category_summary.add_day(3, 593)
  category_summary.add_day(4, 695)
  category_summary.add_day(5, 812)
  category_summary.add_day(6, 943)
  category_summary.add_day(7, 1091)
  category_summary.add_day(8, 1254)
  category_summary.add_day(9, 1433)
  category_summary.add_day(10, 1627)
  category_summary.add_day(11, 1833)
  category_summary.add_day(12, 2049)
  category_summary.add_day(13, 2273)
  category_summary.add_day(14, 2500)
  category_summary.add_day(15, 2727)
  category_summary.add_day(16, 2951)
  return category_summary

def test_constructor():
  assert OverallSummary() != None

def test_add_category(category_summary_exponential):
  overall_summary = OverallSummary()
  report = overall_summary.add_category(category_summary_exponential)
  assert report == category_summary_exponential.report()
  assert overall_summary.reports == [report]
  assert overall_summary.highest_ratio.overall.ratio > 1.49
  assert overall_summary.in_slowdown == []

def test_small_category():
  overall_summary = OverallSummary()
  category_summary = CategorySummary('foo')
  category_summary.add_day(1, 8)
  category_summary.add_day(2, 12)
  report = overall_summary.add_category(category_summary)
  assert report == category_summary.report()
  assert overall_summary.reports == [report]
  assert overall_summary.in_slowdown == []

def test_identify_slowdowns(category_summary_in_slowdown):
  overall_summary = OverallSummary()
  report = overall_summary.add_category(category_summary_in_slowdown)
  assert report == category_summary_in_slowdown.report()
  assert overall_summary.reports == [report]
  assert overall_summary.highest_ratio.overall.ratio > 1.1
  assert overall_summary.in_slowdown == [report]

def test_report(category_summary_in_slowdown):
  overall_summary = OverallSummary()
  overall_summary.add_category(category_summary_in_slowdown)
  overall_report = overall_summary.report()
  assert type(overall_report) == dict
  assert type(overall_report['highest_ratio']) == CategoryReport
  assert overall_report['highest_ratio'].location == 'bar'
  assert overall_report['highest_ratio'].overall.ratio > 1.1
  assert type(overall_report['in_slowdown']) == list

def test_two_summaries(category_summary_exponential, category_summary_in_slowdown):
  overall_summary = OverallSummary()
  exponential_report = overall_summary.add_category(category_summary_exponential)
  in_slowdown_report = overall_summary.add_category(category_summary_in_slowdown)
  assert exponential_report == category_summary_exponential.report()
  assert in_slowdown_report == category_summary_in_slowdown.report()
  assert overall_summary.reports == [exponential_report, in_slowdown_report]
  assert overall_summary.in_slowdown == [in_slowdown_report]
