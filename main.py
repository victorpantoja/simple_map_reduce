#!/usr/bin/python
import os
import sys
import getopt

import settings


def usage():
    print "usage: food_processor.py [--pidfile=PIDFILE] [--help] COMMAND"
    print "\nCOMMANDS:"
    print "     start       "
    print "     stop        "
    print "     restart     "
    print "     help        \n"


def config():
    project_root = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, os.path.abspath("%s/.." % project_root))


def main():
    try:
        optlists, command = getopt.getopt(sys.argv[1:], "hp", ["help", "pidfile="])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    pidfile = settings.PIDFILE

    for opt, value in optlists:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-p", "--pidfile"):
            pidfile = value
    
    if not command or command[0] not in ["start", "stop", "restart"]:
        usage()
        sys.exit()

    config()
    
    from food_processor.manager import TaskManager
    manager = TaskManager(pidfile)

    #for debugging
    if settings.DEBUG:
        if command[0] == "start":
            manager.run()
        elif command[0] == "stop":
            manager.stop()
    else:
        if command[0] == "start":
            manager.start()

        elif command[0] == "stop":
            manager.stop()

        elif command[0] == "restart":
            manager.restart()

if __name__ == "__main__":
    main()
