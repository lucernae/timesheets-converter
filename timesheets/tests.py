# coding=utf-8
import os
import unittest

from timesheets.format.harvest import HarvestTimeRecord
from timesheets.format.sageone import SageOneTimeRecord
from timesheets.format.toggl import TogglTimeRecord, TogglTagsTimeRecord
from timesheets.timesheet import TimeSheets


class TestSageOne(unittest.TestCase):

    def test_load_csv(self):
        ts = TimeSheets()
        ts.time_record_type = SageOneTimeRecord
        ts.load_csv('test/timesheets-sageone.csv')
        self.assertEqual(4, len(ts.records))

    def test_dump_csv(self):
        ts = TimeSheets()
        ts.time_record_type = SageOneTimeRecord
        ts.load_csv('test/timesheets-sageone.csv')

        ts.dump_csv('test/dumped-sageone.csv')
        self.assertTrue(os.path.exists('test/dumped-sageone.csv'))


class TestHarvest(unittest.TestCase):

    def test_load_csv(self):
        ts = TimeSheets()
        ts.time_record_type = HarvestTimeRecord
        ts.load_csv('test/timesheets-harvest.csv')
        self.assertEqual(2, len(ts.records))

    def test_dump_csv(self):
        ts = TimeSheets()
        ts.time_record_type = HarvestTimeRecord
        ts.load_csv('test/timesheets-harvest.csv')

        ts.dump_csv('test/dumped-harvest.csv', one_line=True)
        self.assertTrue(os.path.exists('test/dumped-harvest.csv'))

        # multiple line a task should become one line
        ts.load_csv('test/dumped-harvest.csv')
        self.assertEqual(1, len(ts.records[1].notes.splitlines()))

    def test_convert_to_sageone(self):
        ts = TimeSheets()
        ts.time_record_type = HarvestTimeRecord
        ts.load_csv('test/timesheets-harvest.csv')
        self.assertEqual(2, len(ts.records))

        ts.dump_csv(
            'test/dumped-harvest-sageone.csv', target_type=SageOneTimeRecord)
        self.assertTrue(os.path.exists('test/dumped-harvest-sageone.csv'))


class TestToggl(unittest.TestCase):

    def test_load_csv(self):
        ts = TimeSheets()
        ts.time_record_type = TogglTimeRecord
        ts.load_csv('test/timesheets-toggl.csv')
        self.assertEqual(5, len(ts.records))
        self.assertEqual(0.37166666666666665, ts.records[0].duration)

    def test_dump_csv(self):
        ts = TimeSheets()
        ts.time_record_type = TogglTimeRecord
        ts.load_csv('test/timesheets-toggl.csv')

        ts.dump_csv('test/dumped-toggl.csv', aggregate=True)
        self.assertTrue(os.path.exists('test/dumped-toggl.csv'))

        ts.load_csv('test/dumped-toggl.csv')
        # Test that same task is merged
        self.assertEqual(4, len(ts.records))
        self.assertEqual(5.0, ts.records[3].duration)

    def test_convert_to_sageone(self):
        ts = TimeSheets()
        ts.time_record_type = TogglTimeRecord
        ts.load_csv('test/timesheets-toggl.csv')
        self.assertEqual(5, len(ts.records))

        ts.dump_csv(
            'test/dumped-toggl-sageone.csv', target_type=SageOneTimeRecord)
        self.assertTrue(os.path.exists('test/dumped-toggl-sageone.csv'))

        ts.load_csv(
            'test/dumped-toggl-sageone.csv', target_type=SageOneTimeRecord)

        self.assertEqual('11/06/2018', ts.records[0].date)


class TestTogglTags(unittest.TestCase):

    def test_load_csv(self):
        ts = TimeSheets()
        ts.time_record_type = TogglTagsTimeRecord
        ts.load_csv('test/timesheets-toggl.csv')
        self.assertEqual(5, len(ts.records))
        self.assertEqual(0.37166666666666665, ts.records[0].duration)
        self.assertTrue(ts.records[0].task)

    def test_dump_csv(self):
        ts = TimeSheets()
        ts.time_record_type = TogglTagsTimeRecord
        ts.load_csv('test/timesheets-toggl.csv')

        ts.dump_csv('test/dumped-toggl-tags.csv', aggregate=True)
        self.assertTrue(os.path.exists('test/dumped-toggl-tags.csv'))

        ts.load_csv('test/dumped-toggl-tags.csv')
        # Test that same task is merged
        self.assertEqual(4, len(ts.records))
        self.assertEqual(5.0, ts.records[3].duration)

    def test_convert_to_sageone(self):
        ts = TimeSheets()
        ts.time_record_type = TogglTagsTimeRecord
        ts.load_csv('test/timesheets-toggl.csv')
        self.assertEqual(5, len(ts.records))

        ts.dump_csv(
            'test/dumped-toggl-tags-sageone.csv',
            target_type=SageOneTimeRecord)
        self.assertTrue(os.path.exists('test/dumped-toggl-tags-sageone.csv'))

        ts.load_csv(
            'test/dumped-toggl-tags-sageone.csv',
            target_type=SageOneTimeRecord)

        self.assertEqual('11/06/2018', ts.records[0].date)
