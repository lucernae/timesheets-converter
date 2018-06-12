#!/usr/bin/env python
# coding=utf-8

import argparse
from datetime import timedelta, datetime

from timesheets.timesheet import TimeSheets
from timesheets.format.harvest import HarvestTimeRecord
from timesheets.format.sageone import SageOneTimeRecord
from timesheets.format.toggl import TogglTimeRecord
from timesheets.format.toggl import TogglTagsTimeRecord

parser = argparse.ArgumentParser(
    description='Get reported timesheets format and show it on screen.'
)

parser.add_argument(
    '-t',
    '--input_type',
    metavar='types',
    type=unicode,
    choices=['sageone', 'harvest', 'toggl', 'toggl-tags'],
    help="Input types: ['sageone', 'harvest', 'toggl', 'toggl-tags']",
    default='sageone',
    required=True
)
parser.add_argument(
    '-f',
    '--report_format',
    metavar='format_types',
    type=unicode,
    choices=['daily', 'weekly', 'standup'],
    help="Report format: ['daily', 'weekly', 'standup']",
    default='daily',
    required=False
)
parser.add_argument(
    '-o',
    '--output_format',
    metavar='output_types',
    type=unicode,
    choices=['markdown', 'slack'],
    help="Output format: ['markdown', 'slack']",
    default='slack',
    required=False
)
parser.add_argument(
    'csv_input',
    metavar='input_path',
    # type=argparse.FileType('r'),
    # type=basestring,
    help='CSV file as input for timesheets'
)


def get_record_type(type_name):
    if type_name == 'harvest':
        return HarvestTimeRecord
    elif type_name == 'toggl':
        return TogglTimeRecord
    elif type_name == 'toggl-tags':
        return TogglTagsTimeRecord
    elif type_name == 'sageone':
        return SageOneTimeRecord


def report_aggregate(timesheet):
    """
    Structure:


    {
        "week":
        "days": [
            {
                "date": "10/04/2018"
                "day": "Monday",
                "records": [
                    {
                        "project": "Project"
                        "notes": [
                            "task A",
                            "task B"
                        ]
                    },
                ]
            },
        ]
    }

    :param timesheet: Timesheet object
    :type timesheet: TimeSheets

    """

    dates = [r._date for r in timesheet.records]
    start_date = min(dates)
    end_date = max(dates)

    week_range = '{start:%d %b %Y} - {end:%d %b %Y}'.format(
        start=start_date,
        end=end_date)

    reports = {
        'week': week_range,
        'days': []
    }
    days = reports['days']

    sorted_records = sorted(
        timesheet.records, key= lambda x: (x.date, x.project))

    for r in sorted_records:

        date = r._date
        day = '{date:%A}'.format(date=date)

        try:
            existing_day = next(
                d for d in days if d['date'] == date)
        except StopIteration:
            existing_day = {
                'date': date,
                'day': day,
                'records': []
            }
            days.append(existing_day)

        try:
            existing_project = next(
                p for p in existing_day['records'] if p['project'] == r.project)
        except StopIteration:
            existing_project = {
                'project': r.project,
                'notes': []
            }
            existing_day['records'].append(existing_project)

        existing_project['notes'].append(r.notes)

    return reports


def format_output(report, report_type):

    if report_type == 'slack':

        print '*{week}*'.format(week=report['week'])

        for d in report['days']:

            print '*{day}*'.format(day=d['day'])

            for p in d['records']:

                print '_{project}_'.format(project=p['project'])

                for n in p['notes']:

                    print '- {note}'.format(note=n)

    elif report_type == 'markdown':

        print '# {week}'.format(week=report['week'])

        for d in report['days']:

            print '## {day}'.format(day=d['day'])

            for p in d['records']:

                print '### {project}'.format(project=p['project'])

                for n in p['notes']:

                    print '- {note}'.format(note=n)


args = parser.parse_args()

ts = TimeSheets()


ts.load_csv(args.csv_input, target_type=get_record_type(args.input_type))


today = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')


if args.report_format == 'daily':
    # Return today
    ts.records = [r for r in ts.records if r._date == today]

    report = report_aggregate(ts)

elif args.report_format == 'weekly':
    # Return whole week
    start_week = today
    while start_week.strftime('%A') != 'Monday':
        start_week -= timedelta(days=1)

    end_week = start_week + timedelta(days=6)

    ts.records = [
        r for r in ts.records
        if r._date >= start_week and r._date <= end_week]

    report = report_aggregate(ts)

elif args.report_format == 'standup':
    # Return today and yesterday
    yesterday = today - timedelta(days=1)

    ts.records = [
        r for r in ts.records
        if r._date == yesterday or r._date == today]

    report = report_aggregate(ts)


format_output(report, args.output_format)
