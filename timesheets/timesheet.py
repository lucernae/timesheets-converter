# coding=utf-8
import csv
import datetime
from collections import OrderedDict


class BaseTimeRecordDialect(csv.excel):

    dialect_name = 'base_time_record'
    quoting = csv.QUOTE_ALL


class BaseTimeRecord(object):

    def __init__(self):

        self._date = None
        self._customer = None
        self._project = None
        self._task = None
        self._duration = None
        self._notes = None

        self._meta = self.Meta()

    class Meta:
        fields_mapping = {
            'date': 'date',
            'customer': 'customer',
            'project': 'project',
            'task': 'task',
            'duration': 'duration',
            'notes': 'notes'
        }
        dialect = BaseTimeRecordDialect
        date_format = '%Y-%m-%d'

    @classmethod
    def register_dialect(cls):
        dialect = cls.Meta.dialect

        assert issubclass(dialect, BaseTimeRecordDialect)

        try:
            csv.get_dialect(dialect.dialect_name)
        except csv.Error:
            csv.register_dialect(dialect.dialect_name, dialect)

    @property
    def date(self):
        return self._date.strftime(self.date_format)

    @date.setter
    def date(self, value):
        value = self.check_date_string(value)
        self._date = value

    @property
    def date_format(self):
        return self._meta.date_format

    def check_date_string(self, value):
        return datetime.datetime.strptime(value, self.date_format)

    @property
    def customer(self):
        return self._customer

    @customer.setter
    def customer(self, value):
        self._customer = value

    @property
    def project(self):
        return self._project

    @project.setter
    def project(self, value):
        self._project = value

    @property
    def task(self):
        return self._task

    @task.setter
    def task(self, value):
        self._task = value

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = float(value)

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, value):
        self._notes = value

    @property
    def field_mappings(self):
        return self._meta.fields_mapping

    @property
    def dialect(self):
        return self._meta.dialect

    def assign_to(self, target_instance):
        target_instance._date = self._date
        target_instance._customer = self._customer
        target_instance._project = self._project
        target_instance._task = self._task
        target_instance._duration = self._duration
        target_instance._notes = self._notes

    def to_dict(self, target_type=None):
        retval = {}
        if target_type:
            target_instance = target_type()
            self.assign_to(target_instance)
            fields_mapping = target_instance._meta.fields_mapping
        else:
            target_instance = self
            fields_mapping = self._meta.fields_mapping

        for p, f in fields_mapping.iteritems():
            retval[f] = target_instance.__getattribute__(p)
        return retval

    def from_dict(self, value):
        for p, f in self._meta.fields_mapping.iteritems():
            if f in value:
                self.__setattr__(p, value[f])
            elif hasattr(self, f):
                field_value = self.__getattribute__(f)(value)
                self.__setattr__(p, field_value)


class TimeSheets(object):

    def __init__(self):
        self._time_record_type = None
        self._records = []

    @property
    def time_record_type(self):
        return self._time_record_type

    @time_record_type.setter
    def time_record_type(self, value):
        assert issubclass(value, BaseTimeRecord)
        self._time_record_type = value

    @property
    def records(self):
        return self._records

    @records.setter
    def records(self, value):
        self._records = value

    def _aggregate_same_task(self):
        mapping = OrderedDict()
        for r in self.records:
            key = (r.customer, r.project, r.task, r.notes)
            if key not in mapping:
                mapping[key] = r
            else:
                mapping[key].duration += r.duration

        self.records = [v for k, v in mapping.iteritems()]

    def _one_line_a_task(self):
        for r in self.records:
            r.notes = ' '.join(r.notes.strip().splitlines())

    def load_csv(self, filename, target_type=None, **fmtparams):
        if target_type:
            self.time_record_type = target_type
        with open(filename, 'r') as f:
            reader = csv.DictReader(f, **fmtparams)
            self.records = []
            for row in reader:
                record = self.time_record_type()
                record.from_dict(row)
                self.records.append(record)

    def dump_csv(
            self, filename, target_type=None,
            one_line=None, aggregate=None,
            **fmtparams):

        if one_line:
            self._one_line_a_task()

        if aggregate:
            self._aggregate_same_task()

        with open(filename, 'w') as f:
            if target_type:
                instance = target_type()
            else:
                instance = self.time_record_type()

            csv_fieldnames = [
                field for prop, field in instance.field_mappings.iteritems()]
            csv_dialect = instance.dialect
            writer = csv.DictWriter(
                f, dialect=csv_dialect,
                fieldnames=csv_fieldnames, **fmtparams)

            writer.writeheader()

            dict_records = [r.to_dict(target_type) for r in self.records]
            writer.writerows(dict_records)
