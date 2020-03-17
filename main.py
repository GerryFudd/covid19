import csv
from os.path import exists
from os import mkdir
from datetime import date
from json import dumps

from helpers.summary import CategorySummary
from input_output.get_latest_file import get_latest_file

directory_name = f'results/{date.today().isoformat()}'
source_file_name = f'{directory_name}/source_data.csv'

if not exists(source_file_name):
  mkdir(directory_name)
  get_latest_file(source_file_name)

summaries = {}
with open(source_file_name) as f:
  for row in csv.DictReader(f):
    location = row['Entity']
    day = int(row['Year'])
    count = int(row['Total confirmed cases of COVID-19'])
    if summaries.get(location) == None:
      summaries[location] = CategorySummary(location)
    summaries[location].add_day(day, count)

for location in summaries:
  report = summaries[location].report()
  if report.count > 0:
    with open(f'{directory_name}/{location}.json', 'w') as f:
      f.write(dumps(report, indent=2))
