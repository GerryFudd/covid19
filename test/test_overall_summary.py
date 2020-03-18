from ..helpers.summary import OverallSummary, CategorySummary, CategoryReport

def test_constructor():
  assert OverallSummary() != None

def test_add_category():
  overall_summary = OverallSummary()
  category_summary = CategorySummary('foo')
  category_summary.add_day(1, 8)
  category_summary.add_day(2, 12)
  category_summary.add_day(3, 18)
  category_summary.add_day(4, 27)
  report = overall_summary.add_category(category_summary)
  assert report == category_summary.report()
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

def test_identify_slowdowns():
  overall_summary = OverallSummary()
  category_summary = CategorySummary('foo')
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
  report = overall_summary.add_category(category_summary)
  assert report == category_summary.report()
  assert overall_summary.reports == [report]
  assert overall_summary.highest_ratio.overall.ratio > 1.1
  assert overall_summary.in_slowdown == [report]

def test_report():
  overall_summary = OverallSummary()
  category_summary = CategorySummary('foo')
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
  overall_summary.add_category(category_summary)
  overall_report = overall_summary.report()
  assert type(overall_report) == dict
  assert type(overall_report['highest_ratio']) == CategoryReport
  assert overall_report['highest_ratio'].location == 'foo'
  assert overall_report['highest_ratio'].overall.ratio > 1.1
  assert type(overall_report['in_slowdown']) == list
