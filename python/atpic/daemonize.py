#!/usr/bin/python3
# http://daemonize.sourceforge.net/

# The basic idea is that write your program so that it can be started by calling one function, say main(). 
# Then you would do the following: 
# import daemonize
# def the_other_main_that_calls_the_main_function(sys.argv):
#     # Parse command line options, all that jazz...
#     # Time to start your daemon!
#     daemonize.start(main)

import os
import sys
import fcntl

def start(fun_to_start,pidfile):
    debug = True # False
    logger = None
    std_pipes_to_logger = True
    # Used docs by Levent Karakas 
    # http://www.enderunix.org/documents/eng/daemon.php
    # as a reference for this section.

    # Fork, creating a new process for the child.
    process_id = os.fork()
    if process_id < 0:
        # Fork error.  Exit badly.
        sys.exit(1)
    elif process_id != 0:
        # This is the parent process.  Exit.
        sys.exit(0)
    # This is the child process.  Continue.

    # Stop listening for signals that the parent process receives.
    # This is done by getting a new process id.
    # setpgrp() is an alternative to setsid().
    # setsid puts the process in a new parent group and detaches its
    # controlling terminal.
    process_id = os.setsid()
    if process_id == -1:
        # Uh oh, there was a problem.
        sys.exit(1)

    # Close file descriptors
    devnull = '/dev/null'
    if hasattr(os, "devnull"):
        # Python has set os.devnull on this system, use it instead 
        # as it might be different than /dev/null.
        devnull = os.devnull
    # null_descriptor = open(devnull, 'rw')
    nullfd=os.open(devnull, os.O_RDWR)
    if not debug:
        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        os.dup2(nullfd, sys.stdin.fileno())
        os.dup2(nullfd, sys.stdout.fileno())
        os.dup2(nullfd, sys.stderr.fileno())

    # Set umask to default to safe file permissions when running
    # as a root daemon. 027 is an octal number.
    # os.umask(027)

    # Change to a known directory.  If this isn't done, starting
    # a daemon in a subdirectory that needs to be deleted results
    # in "directory busy" errors.
    # On some systems, running with chdir("/") is not allowed,
    # so this should be settable by the user of this library.
    os.chdir('/')

    # Create a pidfile so that only one instance of this daemon
    # is running at any time.  Again, this should be user settable.
    # pidfile = open(pidfile, 'w')
    # Try to get an exclusive lock on the file.  This will fail
    # if another process has the file locked.
    # fcntl.lockf(pidfile, fcntl.LOCK_EX|fcntl.LOCK_NB)

    # Record the process id to the pidfile.  This is standard
    # practice for daemons.
    # pidfile.write('%s' %(os.getpid()))
    # pidfile.flush()
    fd=os.open(pidfile,os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    os.write(fd, str(os.getpid()).encode('utf8'))
    os.close(fd)
    # Logging.  Current thoughts are:
    # 1. Attempt to use the Python logger (this won't work Python < 2.3)
    # 2. Offer the ability to log to syslog
    # 3. If logging fails, log stdout & stderr to a file
    # 4. If logging to file fails, log stdout & stderr to stdout.

    fun_to_start()
