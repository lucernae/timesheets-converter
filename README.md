# Timesheets Converter Tools

[![Build Status](https://travis-ci.org/lucernae/timesheets-converter.svg?branch=master)](https://travis-ci.org/lucernae/timesheets-converter)

[![codecov](https://codecov.io/gh/lucernae/timesheets-converter/branch/master/graph/badge.svg)](https://codecov.io/gh/lucernae/timesheets-converter)

## What is this?

This is a tool to bulk convert timesheets from different providers.

It accepts/convert:

- Harvest Timesheets CSV format
- Toggl Timesheets CSV format
- Toggl Timesheets (using tags as task) CSV format
- SageOne Timesheets CSV format

## How to install

1. Clone this repo (currently dev version)
2. Install to your virtual env or global python installation

```
pip install -e .
```

3. Create alias (mac) or link the scripts to your `/usr/local/bin`

Script link

```
ln -s ${PWD}/scripts/convert_timesheets.py /usr/local/bin/convert_timesheets.py
```

Alias

```
echo "alias convert_timesheets='${PWD}/scripts/convert_timesheets.py'" >> ~/.bash_profile
```


# How to use

I used below command to convert from toggl (with tags as project tasks) into sageone format

```
convert_timesheets.py -t toggl-tags -al <toggl-time-entries-input.csv> <sageone-output.csv>
```
