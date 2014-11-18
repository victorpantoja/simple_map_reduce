import logging
from datetime import datetime


def timer(fn):
    """
        This is just a simple timer to help profiling
    """
    def timer_fn(*arguments, **kwarguments):
        start = datetime.now()
        result = fn(*arguments, **kwarguments)
        logging.info("[timer][%s] - executed in %s " % (fn.__name__, (datetime.now()-start)))

        return result
    return timer_fn
