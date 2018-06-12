# coding=utf-8

from timesheets.timesheet import BaseTimeRecord, BaseTimeRecordDialect


class SageOneTimeRecord(BaseTimeRecord):

    class Meta:
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
