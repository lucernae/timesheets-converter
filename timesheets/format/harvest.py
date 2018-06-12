# coding=utf-8

from timesheets.timesheet import BaseTimeRecord, BaseTimeRecordDialect


class HarvestTimeRecord(BaseTimeRecord):

    class Meta:
        fields_mapping = {
            'date': 'Date',
            'customer': 'Client',
            'project': 'Project Code',
            'task': 'Task',
            'duration': 'Hours Rounded',
            'notes': 'Notes'
        }
        dialect = BaseTimeRecordDialect
        date_format = '%Y-%m-%d'


HarvestTimeRecord.register_dialect()
