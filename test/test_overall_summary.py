from pytest import fixture

from .fixtures import category_summary_exponential, category_summary_in_slowdown, small_category_summary
from ..helpers.summary import OverallSummary, CategoryReport


def test_constructor():
  assert OverallSummary() != None

def test_add_category(category_summary_exponential):
  overall_summary = OverallSummary()
  report = overall_summary.add_category(category_summary_exponential)
  assert report == category_summary_exponential.report()
  assert overall_summary.reports == [report]
  assert overall_summary.highest_ratio.overall.ratio > 1.49
  assert overall_summary.in_slowdown == []

def test_small_category(small_category_summary):
  overall_summary = OverallSummary()
  report = overall_summary.add_category(small_category_summary)
  assert report == small_category_summary.report()
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
