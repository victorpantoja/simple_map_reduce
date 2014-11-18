# coding: utf-8
import os
import unittest

import simplejson

import settings
from food_processor.task.mapper import MapperTask
from food_processor.task.reducer import ReducerTask


class MapperTaskTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.path_category_file1 = os.path.join(settings.FILE_PATH, "category_0-8.txt")
        cls.path_category_file2 = os.path.join(settings.FILE_PATH, "category_9-11.txt")

        cls.path_food_file1 = os.path.join(settings.FILE_PATH, "food_0-8.txt")
        cls.path_food_file2 = os.path.join(settings.FILE_PATH, "food_9-11.txt")

        cls.food_reduce_file = os.path.join(settings.FILE_PATH, "food_reduce.txt")
        cls.category_reduce_file = os.path.join(settings.FILE_PATH, "category_reduce.txt")

        cls.content1 = [{'food_id': 1, 'id': 1, 'category_id': 1},
                        {'food_id': 1, 'id': 3, 'category_id': 1},
                        {'food_id': 1, 'id': 1, 'category_id': 1},
                        {'food_id': 3, 'id': 3, 'category_id': 1},
                        {'food_id': 3, 'id': 1, 'category_id': 1},
                        {'food_id': 4, 'id': 3, 'category_id': 2},
                        {'food_id': 5, 'id': 1, 'category_id': 2},
                        {'food_id': 6, 'id': 3, 'category_id': 3}]

        cls.content2 = [{'food_id': 1, 'id': 1, 'category_id': 1},
                        {'food_id': 6, 'id': 3, 'category_id': 3},
                        {'food_id': 7, 'id': 1, 'category_id': 2}]

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.path_category_file1):
            os.remove(cls.path_category_file1)

        if os.path.exists(cls.path_category_file2):
            os.remove(cls.path_category_file2)

        if os.path.exists(cls.path_food_file1):
            os.remove(cls.path_food_file1)

        if os.path.exists(cls.path_food_file2):
            os.remove(cls.path_food_file2)

        if os.path.exists(cls.food_reduce_file):
            os.remove(cls.food_reduce_file)

        if os.path.exists(cls.category_reduce_file):
            os.remove(cls.category_reduce_file)

    def test_map(self):
        """
        Test if I can correctly sum food and categories and if I can write file correctly
        """
        
        MapperTask().map(self.content1, 0, 8)

        self.assertTrue(os.path.exists(self.path_food_file1))
        self.assertTrue(os.path.exists(self.path_category_file1))

        with open(self.path_food_file1, "r") as map_file:
            content = simplejson.loads(map_file.read())

        self.assertDictEqual({'1': 3, '3': 2, '5': 1, '4': 1, '6': 1}, content)

        with open(self.path_category_file1, "r") as map_file:
            content = simplejson.loads(map_file.read())

        self.assertDictEqual({'1': 5, '3': 1, '2': 2}, content)

        MapperTask().map(self.content2, 9, 11)

        self.assertTrue(os.path.exists(self.path_food_file2))
        self.assertTrue(os.path.exists(self.path_category_file2))

        with open(self.path_food_file2, "r") as map_file:
            content = simplejson.loads(map_file.read())

        self.assertDictEqual({'1': 1, '6': 1, '7': 1}, content)

        with open(self.path_category_file2, "r") as map_file:
            content = simplejson.loads(map_file.read())

        self.assertDictEqual({'1': 1, '3': 1, '2': 1}, content)

    def test_reduce(self):
        """
        Test if I can correctely sum food and categories written in map files
        """

        ReducerTask().reduce("category")
        ReducerTask().reduce("food")

        with open(self.food_reduce_file, "r") as map_file:
            content = simplejson.loads(map_file.read())

        self.assertDictEqual({'1': 4, '3': 2, '5': 1, '4': 1, '7': 1, '6': 2}, content)

        with open(self.category_reduce_file, "r") as map_file:
            content = simplejson.loads(map_file.read())

        self.assertDictEqual({'1': 6, '3': 2, '2': 3}, content)
