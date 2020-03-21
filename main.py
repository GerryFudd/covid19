import csv
from os.path import exists
from os import mkdir
from datetime import date
from json import dumps
from pandas import read_csv

from helpers.summary import CategorySummary, OverallSummary
from input_output.get_latest_file import get_latest_file

directory_name = f'results/{date.today().isoformat()}'
source_file_name = f'{directory_name}/source_data.csv'

if not exists(source_file_name):
  if not exists(directory_name):
    mkdir(directory_name)
  get_latest_file(source_file_name)

full_dataframe = read_csv(source_file_name).rename(columns={'Entity': 'location', 'Year': 'day', 'Total confirmed cases of COVID-19 (cases)': 'count'})

overall_summary = OverallSummary()
for location in full_dataframe.location.unique():
  report = overall_summary.add_category(CategorySummary(location, full_dataframe))
  if report.count > 0:
    with open(f'{directory_name}/{location}.json', 'w') as f:
      f.write(dumps(report, indent=2))

with open(f'{directory_name}/__overallReport.json', 'w') as f:
  f.write(dumps(overall_summary.report(), indent=2))
