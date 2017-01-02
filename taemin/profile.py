""" Module to add profiling function to taemin """

import tempfile
import cProfile
import pstats
import StringIO
import time

from taemin import logger

LOGGER = logger.Logger()

def profile(func):
    """ Profile decorator:

        Add @profile.profile on a function to profile it.
    """

    tempfile.tempdir = "/tmp/taemin"
    profile_path = tempfile.gettempdir()

    def wraps(*args, **kwargs):
        """ Wrapper function"""

        profiling = cProfile.Profile()

        start = time.time()

        res = profiling.runcall(func, *args, **kwargs)

        # Execution time:
        delta = time.time() - start

        stats_file = "%s_%f_%fs_%s" % (profile_path,
                                       time.time(),
                                       delta,
                                       func.__name__)

        LOGGER.info("Dumping stats to %r" % stats_file)

        (pstats.Stats(profiling, stream=StringIO.StringIO())
                .sort_stats("cumulative")
                .dump_stats(stats_file))

        return res

    return wraps
