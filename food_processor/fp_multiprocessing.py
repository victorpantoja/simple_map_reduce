# coding: utf-8
import logging
from ctypes import c_bool
from datetime import datetime
from time import sleep
from multiprocessing import Process, Pipe, Value, current_process

"""

This class implements multiprocess as described in https://docs.python.org/2/library/multiprocessing.html

"""


class FoodStatsMultiProcessing():

    def __init__(self, size, target):
        self.size = size
        self.target = target

        #to share state
        self.aborted = Value(c_bool, False)
        self.processes = []
        self.tasks_size = 0
        self.tasks = {}

        for i in range(self.size):
            self.tasks[i] = []
            
        logging.debug("[FoodStatsMultiProcessing] __init__(size=%s)" % size)

    def add_task(self, *args):
        #share tasks between processes
        index = self.tasks_size % self.size
        self.tasks[index].append(args)
        self.tasks_size += 1

    def start(self):
        self.start_date = datetime.now()

        logging.debug("[FoodStatsMultiProcessing] start() size=%s tasks_size=%s" % (self.size, self.tasks_size))

        #starts each process and keep some meta data about them
        for i in range(self.size):
            #communication with process
            parent_conn, child_conn = Pipe()
            p = Process(name='process_%s' % i, target=self.worker, args=(self.tasks[i], child_conn))

            self.processes.append({'process': p,
                                   'index': i,
                                   'parent_conn': parent_conn,
                                   'finished': False})

            logging.debug("[FoodStatsMultiProcessing] start() process_%s process_tasks=%s" % (i, len(self.tasks[i])))

            p.start()
            sleep(.2)

    def join(self):
        """
        Controls execution and just stops when all processes stop
        """
        total_processed_items = 0
        
        while True:
            finished_processes = 0
            for p in self.processes:
                if not p['finished']:
                    if not p['process'].is_alive():
                        processed_items = p['parent_conn'].recv()
                        total_processed_items += processed_items
                        p['finished'] = True                        
                        p['process'].join()
                        p['process'].terminate()                        
                        
                        finished_processes += 1

                        #verifies if total processed items is correct
                        if processed_items != len(self.tasks[p['index']]):
                            #controls main script stopping
                            self.aborted.value = True
                            
                        logging.debug("[FoodStatsMultiProcessing] join() %s process_tasks=%s processed_items=%s" % (p['process'].name, len(self.tasks[p['index']]), processed_items))
                else:
                    finished_processes += 1

            if finished_processes == self.size:
                logging.debug("[FoodStatsMultiProcessing] terminate() size=%s tasks_size=%s total_processed_items=%s spent_time=%s" % (self.size, self.tasks_size, total_processed_items, datetime.now()-self.start_date))
                break

            sleep(1)

    def worker(self, tasks, conn):
        """
        Receives tasks to be processed and the connection with process
        """
        name = current_process().name

        #controls how many items were processed. This is important to keep track of things...
        processed_items = 0

        for task in tasks:
            try:
                self.target(*task)
                processed_items += 1
            except Exception, e:
                logging.exception("[FoodStatsMultiProcessing] worker() %s task=%s Exception=%s" % (name, task, e))
                self.aborted.value = True
            
            if self.aborted.value:
                break

        logging.debug("[FoodStatsMultiProcessing] worker() %s processed_items=%s" % (name, processed_items))
        
        conn.send(processed_items)
