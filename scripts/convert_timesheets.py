#!/usr/bin/env python
# coding=utf-8

import argparse

from timesheets.timesheet import TimeSheets
from timesheets.format.harvest import HarvestTimeRecord
from timesheets.format.sageone import SageOneTimeRecord
from timesheets.format.toggl import TogglTimeRecord
from timesheets.format.toggl import TogglTagsTimeRecord

parser = argparse.ArgumentParser(
    description='Convert Timesheets CSV format to SageOne format.'
)

parser.add_argument(
    '-t',
    '--input_type',
    metavar='types',
    type=str,
    choices=['sageone', 'harvest', 'toggl', 'toggl-tags'],
    help="Input types: ['sageone', 'harvest', 'toggl', 'toggl-tags']",
    required=True
)
parser.add_argument(
    '-o',
    '--output_type',
    metavar='types',
    type=str,
    choices=['sageone', 'harvest', 'toggl', 'toggl-tags'],
    help="Input types: ['sageone', 'harvest', 'toggl', 'toggl-tags']",
    default='sageone',
    required=False
)
parser.add_argument(
    '-l',
    '--one_line',
    action='store_true',
    help='Merge multiline tasks description into one line.'
)
parser.add_argument(
    '-a',
    '--aggregate',
    action='store_true',
    help='Merge multiple tasks with the same description into one merged task'
)
parser.add_argument(
    'csv_input',
    metavar='input_path',
    # type=argparse.FileType('r'),
    # type=basestring,
    help='CSV file as input for timesheets'
)
parser.add_argument(
    'csv_output',
    metavar='output_path',
    # type=argparse.FileType('w'),
    # type=basestring,
    help='CSV file as output for SageOne timesheets'
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


args = parser.parse_args()

ts = TimeSheets()

ts.load_csv(args.csv_input, target_type=get_record_type(args.input_type))

ts.dump_csv(
    args.csv_output, target_type=get_record_type(args.output_type),
    one_line=args.one_line, aggregate=args.aggregate)
