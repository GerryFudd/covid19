import math
from statistics import mean

from .regression import exponential_regression, linear_regression

class ReportSlope(dict):
  def __init__(self, slope, r2):
    dict.__init__(self, slope=slope, r2=r2)
    self.slope = slope
    self.r2 = r2

class ReportRatio(dict):
  def __init__(self, ratio, r2):
    dict.__init__(self, ratio=ratio, r2=r2)
    self.ratio = ratio
    self.r2 = r2

class CategoryReport(dict):
  def __init__(self, location, count, ratio, r2, last_week_deltas_slope, last_week_deltas_r2, expected_exponential_second_derivative):
    self.overall = ReportRatio(ratio, r2)
    self.last_week_deltas = ReportSlope(last_week_deltas_slope, last_week_deltas_r2)
    dict.__init__(
      self, location=location, count=count, overall=self.overall, 
      last_week_deltas=self.last_week_deltas,
      expected_exponential_second_derivative=expected_exponential_second_derivative
    )
    self.location = location
    self.count = count
    self.expected_exponential_second_derivative=expected_exponential_second_derivative


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
      return CategoryReport(self.location, 0, 1, 1, 1, 1, 0)
    days_summary_list = []
    for day in self.days:
      days_summary_list.append((day, self.days[day]['count']))
    regression = exponential_regression(days_summary_list)

    expected_exponential_second_derivative = self.total_count * math.log(regression[1]) ** 2

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
    last_week_deltas_regression = linear_regression(last_week_deltas_summary)

    return CategoryReport(
      self.location,
      self.total_count,
      ratio=regression[1],
      r2=regression[2],
      last_week_deltas_slope=last_week_deltas_regression[1],
      last_week_deltas_r2=last_week_deltas_regression[2],
      expected_exponential_second_derivative=expected_exponential_second_derivative
    )