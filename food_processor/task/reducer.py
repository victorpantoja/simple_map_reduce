# coding: utf-8
"""
   This classe implements the reduce function of map / reduce.
"""
import os
import fnmatch

import simplejson

import settings
from food_processor import timer
from food_processor.fp_multiprocessing import FoodStatsMultiProcessing


class RunProcessException(Exception):
    pass


class ReducerTask(object):

    @timer
    def reduce(self, content_type):
        content_dict = {}

        for f in os.listdir(settings.FILE_PATH):
            if fnmatch.fnmatch(f, '{}*.txt'.format(content_type)):
                with open(os.path.join(settings.FILE_PATH, f), "r") as map_file:
                    content = simplejson.loads(map_file.read())

                for key in content:
                    if key not in content_dict:
                        content_dict[key] = 0
                    content_dict[key] += content[key]

        with open(os.path.join(settings.FILE_PATH, "{}_reduce.txt".format(content_type)), "w") as reduce_file:
            reduce_file.write(simplejson.dumps(content_dict))

    def run(self):
        process_size = 2

        pool = FoodStatsMultiProcessing(size=process_size, target=self.reduce)
        pool.add_task("category")
        pool.add_task("food")

        pool.start()
        pool.join()

        if pool.aborted.value:
            raise RunProcessException("Ocorreu um erro no processo de pontos e patrimônio dos times (ReducerTask.run)")
