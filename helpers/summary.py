import math
from statistics import mean
from pandas import DataFrame

from .regression import exponential_regression, linear_regression

class ReportSlope(dict):
  def __init__(self, slope, r2, expected_slope):
    dict.__init__(self, slope=slope, r2=r2, expected_slope=expected_slope)
    self.slope = slope
    self.r2 = r2
    self.expected_slope = expected_slope

class ReportRatio(dict):
  def __init__(self, ratio, r2):
    dict.__init__(self, ratio=ratio, r2=r2)
    self.ratio = ratio
    self.r2 = r2

class CategoryReport(dict):
  def __init__(self, location, count, ratio, r2, last_week_deltas_slope, last_week_deltas_r2, expected_exponential_second_derivative, days):
    self.overall = ReportRatio(ratio, r2)
    self.last_week_daily_new_cases = ReportSlope(last_week_deltas_slope, last_week_deltas_r2, expected_exponential_second_derivative)
    dict.__init__(
      self, location=location, count=count, days=days, overall=self.overall, 
      last_week_daily_new_cases=self.last_week_daily_new_cases
    )
    self.location = location
    self.count = count
    self.days = days


class CategorySummary:
  def __init__(self, location, dataframe):
    self.location = location
    # only keep rows with
    # - the provided location and
    # - count at least 5
    # only keep columns 'day' and 'count'
    # set the index to day
    self.dataframe = dataframe[dataframe.location == location].query('count >= 5').filter(['day', 'count']).set_index('day')

  @property
  def last_day(self):
    if self.dataframe.shape[0] == 0:
      return -1
    return int(self.dataframe.index.max())

  @property
  def first_day(self):
    if self.dataframe.shape[0] == 0:
      return math.inf
    return int(self.dataframe.index.min())

  @property
  def total_count(self):
    if self.dataframe.shape[0] == 0:
      return -1
    return int(self.dataframe['count'].max())

  def new_cases(self):
    count_list = self.dataframe['count'].tolist()
    new_cases = list(map(lambda pair: pair[0] - pair[1], zip(count_list[1:], count_list[:-1])))
    return DataFrame(data={'day': self.dataframe.index.tolist()[1:], 'new_cases': new_cases}).set_index('day')

  def report(self):
    if self.last_day < 0:
      return CategoryReport(self.location, 0, 1, 1, 1, 1, 0, 0)
    exponential_regression_result = exponential_regression(
      self.dataframe.index.tolist(), 
      self.dataframe['count'].tolist()
    )

    new_cases_frame = self.new_cases()
    last_week_new_cases = new_cases_frame[new_cases_frame.index > self.last_day - 7]
    last_week_new_cases_linear_regression_result = linear_regression(
      last_week_new_cases.index.tolist(),
      last_week_new_cases['new_cases'].tolist()
    )

    mid_week_day = self.last_day - len(last_week_new_cases) // 2
    expected_new_cases_slope = self.dataframe.at[mid_week_day, 'count'] * math.log(exponential_regression_result[1]) ** 2

    return CategoryReport(
      self.location,
      self.total_count,
      days=self.last_day - self.first_day + 1,
      ratio=exponential_regression_result[1],
      r2=exponential_regression_result[2],
      last_week_deltas_slope=last_week_new_cases_linear_regression_result[1],
      last_week_deltas_r2=last_week_new_cases_linear_regression_result[2],
      expected_exponential_second_derivative=expected_new_cases_slope
    )

class OverallSummary:
  def __init__(self):
    self.reports = []
    self.highest_ratio = CategoryReport(
      ratio=-1,
      location=None,
      count=None,
      r2=None,
      last_week_deltas_slope=None,
      last_week_deltas_r2=None,
      expected_exponential_second_derivative=None,
      days=None
    )
    self.in_slowdown = []

  def add_category(self, summary):
    report = summary.report()
    self.reports.append(report)
    if report.overall.ratio > self.highest_ratio.overall.ratio:
      self.highest_ratio = report
    last_week_daily_new_cases = report.last_week_daily_new_cases
    if (
      report.days >= 7 and 
      last_week_daily_new_cases.slope < 0.25 * last_week_daily_new_cases.expected_slope
    ):
      self.in_slowdown.append(report)
    return report
  
  def report(self):
    return {
      'highest_ratio': self.highest_ratio,
      'in_slowdown': self.in_slowdown
    }
