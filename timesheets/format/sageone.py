# coding=utf-8

from builtins import object
from timesheets.timesheet import BaseTimeRecord, BaseTimeRecordDialect


class SageOneTimeRecord(BaseTimeRecord):

    class Meta(object):
        fields_mapping = {
            'date': 'Date',
            'customer': 'Customer',
            'project': 'Project Name',
            'task': 'Task',
            'duration': 'Hours',
            'notes': 'Comment'
        }
        dialect = BaseTimeRecordDialect
        date_format = '%d/%m/%Y'


SageOneTimeRecord.register_dialect()
