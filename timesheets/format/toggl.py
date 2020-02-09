# coding=utf-8
from __future__ import division
from past.utils import old_div
from builtins import object
import csv

from datetime import datetime
from timesheets.timesheet import BaseTimeRecord, BaseTimeRecordDialect


class TogglTimeRecordDialect(BaseTimeRecordDialect):

    dialect_name = 'toggl'
    quoting = csv.QUOTE_NONE


class TogglTimeRecord(BaseTimeRecord):

    class Meta(object):
        fields_mapping = {
            'date': 'Start date',
            'customer': 'Client',
            'project': 'Project',
            'task': 'Task',
            'time_duration': 'Duration',
            'duration': 'calculate_duration',
            'notes': 'Description'
        }
        dialect = TogglTimeRecordDialect
        date_format = '%Y-%m-%d'

    def calculate_duration(self, raw_dict):
        time_format = '%H:%M:%S'
        duration_string = raw_dict['Duration']
        end = datetime.strptime(duration_string, time_format)
        start = datetime.strptime('00:00:00', time_format)
        diff = end - start
        hours_duration = old_div(diff.total_seconds(), 3600)
        return hours_duration


class TogglTagsTimeRecord(TogglTimeRecord):

    class Meta(object):
        fields_mapping = {
            'date': 'Start date',
            'customer': 'Client',
            'project': 'Project',
            'task': 'Tags',
            'time_duration': 'Duration',
            'duration': 'calculate_duration',
            'notes': 'Description'
        }
        dialect = TogglTimeRecordDialect
        date_format = '%Y-%m-%d'


TogglTimeRecord.register_dialect()
TogglTagsTimeRecord.register_dialect()
