import math
from statistics import mean

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
  def __init__(self, location):
    self.location = location
    self.days = {}
    self.total_count = -1
    self.last_day = -1
    self.first_day = math.inf

  def add_day(self, day, count):
    # Ignore days where the count is less than 5 to avoid throwing off
    # the regression model with isolated cases that didn't spread for
    # a long time.
    if count < 5:
      return
    self.days[day] = {'count': count}
    self.total_count = max(self.total_count, count)
    self.last_day = max(self.last_day, day)
    self.first_day = min(self.first_day, day)

  def report(self):
    if self.last_day < 0:
      return CategoryReport(self.location, 0, 1, 1, 1, 1, 0, 0)
    days_summary_list = []
    for day in self.days:
      days_summary_list.append((day, self.days[day]['count']))
    regression = exponential_regression(days_summary_list)


    last_week_deltas_summary = []
    while (
      len(last_week_deltas_summary) < 7 and
      self.days.get(self.last_day - len(last_week_deltas_summary)) != None and
      self.days.get(self.last_day - len(last_week_deltas_summary) - 1) != None
    ):
      day = self.last_day - len(last_week_deltas_summary)
      delta = self.days[day]['count'] - self.days[day - 1]['count']
      last_week_deltas_summary.append((
        day,
        delta
      ))
    # Calculate the second derivative of the exponential in the middle of last week
    mid_week = self.last_day - len(last_week_deltas_summary) // 2
    expected_exponential_second_derivative = self.days[mid_week]['count'] * math.log(regression[1]) ** 2
    last_week_deltas_regression = linear_regression(last_week_deltas_summary)

    return CategoryReport(
      self.location,
      self.total_count,
      days=self.last_day - self.first_day + 1,
      ratio=regression[1],
      r2=regression[2],
      last_week_deltas_slope=last_week_deltas_regression[1],
      last_week_deltas_r2=last_week_deltas_regression[2],
      expected_exponential_second_derivative=expected_exponential_second_derivative
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
