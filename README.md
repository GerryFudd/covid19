# COVID 19 Tracker

This is a tool to pull data from [ourworldindata.org](https://ourworldindata.org/grapher/total-cases-covid-19-who) and analyze it to see where in the world the spread of Covid-19 is still growing exponentially and where it seems to be at the inflection point of a [logistic curve](https://en.wikipedia.org/wiki/Logistic_function).

## Setup

There are two dependencies for this project (as listed in [requirements.txt](./requirements.txt)), `pytest` and `selenium`. You can install them with

```
pip3 install -U $(cat requirements.txt)
```

Selenium also requires an appropriate chrome driver to pull the csv file from the website. The appropriate driver for the version of Chrome that you have installed may be downloaded from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads), unzipped, and then moved to somewhere on your `PATH` (eg /usr/local/bin).

## Tests

Once pytest is installed, you can run the tests with the command `pytest`. All of the test files are under the `test/` directory in files named `test_*.py`.

## Running the application

Just execute `python3 main.py` from the command line. This will download the source data from ourworldindata.org, move it to the appropriate results directory, and then generate a json file with some details about the current state of the virus in each region.