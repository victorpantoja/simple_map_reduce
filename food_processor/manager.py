# -*- coding: utf-8 -*-
"""
This is the class responsible for call all tasks and log results.
"""
import heapq
import logging
import os
from datetime import datetime

import simplejson

import settings
from food_processor.daemon import Daemon
from food_processor.task.reducer import ReducerTask
from food_processor.task.mapper import MapperTask


class TaskManager(Daemon):

    def __init__(self, pidfile):
        return Daemon.__init__(self, pidfile)

    def stop(self):
        logging.debug(">>>>>>>>> (Kill) Food Processor")
        Daemon.stop(self)

    def run(self):
        logging.debug("====================\nInitializing Food Processor\n\n")
        start = datetime.now()

        try:
            logging.debug("====================\n Startiing mapping\n\n")
            MapperTask().run()

            logging.debug("====================\n Startiing reducing\n\n")
            ReducerTask().run()

            with open(os.path.join(settings.FILE_PATH, "category_reduce.txt"), "r") as reduce_file:
                content = simplejson.loads(reduce_file.read())

            #heap resolves in o(n lg n)
            top_categories = heapq.nlargest(5, content, key=lambda k: content[k])

            with open(os.path.join(settings.FILE_PATH, "food_reduce.txt"), "r") as reduce_file:
                content = simplejson.loads(reduce_file.read())

            top_foods = heapq.nlargest(100, content, key=lambda k: content[k])

            logging.info("\tTop Foods: {}".format(",".join(top_foods)))
            logging.info("\tTop categories: {}".format(",".join(top_categories)))

        except Exception, e:
            logging.exception("====================\nThere were some problemas while processing food information\n")
        finally:
            logging.info("Process took %s\n--------------------\n" % (datetime.now() - start))
            self.delpid()

    def delpid(self):
        if not os.path.isfile(self.pidfile):
            print "pidfile %s not exist" % self.pidfile
            return

        try:
            os.remove(self.pidfile)
        except Exception, e:
            logging.info("pid file not removed")
