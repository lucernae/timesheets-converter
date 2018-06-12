# Timesheets Converter Tools

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
