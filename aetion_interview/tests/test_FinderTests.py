import unittest
from datetime import datetime
from Finder import Finder
from Thing import Thing
from FT import FT
from safe_timezone import safe_timestamp

class TestFinder(unittest.TestCase):
    def setUp(self):
        self.sue = Thing()
        self.sue.name = "Sue"
        self.sue.birth_date = datetime(1950, 1, 1)

        self.greg = Thing()
        self.greg.name = "Greg"
        self.greg.birth_date = datetime(1952, 6, 1)

        self.sarah = Thing()
        self.sarah.name = "Sarah"
        self.sarah.birth_date = datetime(1982, 1, 1)

        self.mike = Thing()
        self.mike.name = "Mike"
        self.mike.birth_date = datetime(1979, 1, 1)

    def test_returns_empty_results_when_given_empty_list(self):
        list_ = []
        finder = Finder(list_)

        result = finder.find(FT.One)
        self.assertIsNone(result.P1)

        self.assertIsNone(result.P2)

    def test_returns_empty_results_when_given_one_person(self):
        list_ = []
        list_.append(self.sue)

        finder = Finder(list_)

        result = finder.find(FT.One)

        self.assertIsNone(result.P1)
        self.assertIsNone(result.P2)

    def test_returns_closest_two_for_two_people(self):
        list_ = []
        list_.append(self.sue)
        list_.append(self.greg)
        finder = Finder(list_)

        result = finder.find(FT.One)

        self.assertEqual(self.sue, result.P1)
        self.assertEqual(self.greg, result.P2)

    def test_returns_furthest_two_for_two_people(self):
        list_ = []
        list_.append(self.mike)
        list_.append(self.greg)

        finder = Finder(list_)

        result = finder.find(FT.Two)

        self.assertEqual(self.greg, result.P1)
        self.assertEqual(self.mike, result.P2)

    def test_returns_furthest_two_for_four_people(self):
        list_ = []
        list_.append(self.sue)
        list_.append(self.sarah)
        list_.append(self.mike)
        list_.append(self.greg)
        finder = Finder(list_)

        result = finder.find(FT.Two)

        self.assertEqual(self.sue, result.P1)
        self.assertEqual(self.sarah, result.P2)

    def test_returns_closest_two_for_four_people(self):
        list_ = []
        list_.append(self.sue)
        list_.append(self.sarah)
        list_.append(self.mike)
        list_.append(self.greg)

        finder = Finder(list_)

        result = finder.find(FT.One)

        self.assertEqual(self.sue, result.P1)
        self.assertEqual(self.greg, result.P2)
