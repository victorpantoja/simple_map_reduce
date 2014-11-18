[![Travis CI](https://travis-ci.org/victorpantoja/simple_map_reduce.svg?branch=master)](victorpantoja/simple_map_reduce)


simple_map_reduce
=================

Just a Simple Script to Starting Map Reduce. This script reads data from an API and uses multiprocesses to process all
this data. Each process receives part of the data read from API, process it so as to count food_id and category_id and
save the result to a file. This is the map operation.

Then, another processes read those files and make the final process over the data (reduce operation) so as to have all
food and all categories summed.

So, this is a very simple way to perform map / reduce operations over API data.

Usage
------------
python main.py start


Tests
------------
make tests



Performance (first thoughts)
-----------------------------
This very first version took 14s to process 3000 items. So, if performance improves linearly, it would take 648 hours to
accomplish the task. This is prohibitive!

Profiling script shows that 12s are burn just to get data from API. So, clearly, this is the bottleneck and should be
improved.


TODO
-------
- The action of getting data from API could be improved. Each process should get data from API by itself instead of just
wating all the data
- tunning number of processes
- tunning limit
- hadoop!
