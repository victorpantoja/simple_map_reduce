# coding: utf-8
"""
This classe implements the map function of map / reduce.
"""
import logging
import os

import requests
import simplejson

import settings
from food_processor import timer
from food_processor.fp_multiprocessing import FoodStatsMultiProcessing


class RunProcessException(Exception):
    pass


class MapperTask(object):

    @timer
    def map(self, content, initial, final):
        logging.debug("Initial: {0}, Fim: {1}".format(initial, final))
        food_dict = {}
        category_dict = {}

        for item in content:
            if item['food_id'] not in food_dict:
                food_dict[item['food_id']] = 0

            food_dict[item['food_id']] += 1

            if item['category_id'] not in category_dict:
                category_dict[item['category_id']] = 0

            category_dict[item['category_id']] += 1

        with open(os.path.join(settings.FILE_PATH, "food_{0}-{1}.txt".format(initial, final)), "w") as map_file:
            map_file.write(simplejson.dumps(food_dict))

        with open(os.path.join(settings.FILE_PATH, "category_{0}-{1}.txt".format(initial, final)), "w") as map_file:
            map_file.write(simplejson.dumps(category_dict))

    def run(self):
        offset = 0
        limit = 300

        #just to control loop while testing
        index = 0

        process_size = 1
        pool = FoodStatsMultiProcessing(size=process_size, target=self.map)

        while True:
            if index == 10:
                break
            index += 1

            response = requests.get('{0}?offset={1}&limit={2}'.format(settings.API, offset, limit))
            content = simplejson.loads(response.content)

            if not content['response']:
                break

            pool.add_task(content['response'], offset+1, content['meta']['next_offset'])

            offset = content['meta']['next_offset']

            #time.sleep(1)

        pool.start()
        pool.join()

        if pool.aborted.value:
            raise RunProcessException("Something went wrong :( (MapperTask.run)")
