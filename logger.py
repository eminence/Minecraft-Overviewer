import consoleDriver
import time


_logger = None


def getLogger():
    global _logger
    if _logger:
        #print "returning existing logger"
        return _logger


    #print "getting new logger"
    l = logger()
    _logger = l
    return l

class logger(object):
    def __init__(self):
        print "init logger"
        self.driver = consoleDriver.getDriver()
        self.last_status = 0

        self.bottom_total=None  # number of tiles on the bottom layer
        self.big_total=None     # number of tiles on all layers

    def finish(self):
        self.driver.finish()


    def info(self, msg, *args):
        self.driver.print_info("[info] %s" % (msg % args)) 

    def debug(self, msg, *args):
        self.driver.print_debug("[debug] %s" % (msg % args)) 

    def warning(self, msg, *args):
        self.driver.print_warning("[warning] %s" % (msg % args)) 

    def error(self, msg, *args):
        self.driver.print_error("[error] %s" % (msg % args))

    def update_status(self, level, complete, total, force=False):
        self.current_level = level
        self.current_levelcomplete = complete
        self.current_leveltotal = total
        if (time.time() - self.last_status) > 0.3 or force:
            self.last_status = time.time()
            # calculate progress
            previous_complete = sum(map(lambda x: self.bottom_total/pow(4,x), range(self.current_level - 1)))
            percent = (previous_complete + self.current_levelcomplete) / float(self.big_total)

            self.driver.display_statusbar(level=level, total_levels=self.total_levels,
                    level_complete=complete,
                    level_total=total,
                    total_complete=(previous_complete + self.current_levelcomplete), 
                    total = self.big_total
                    )

    def print_statusbar(self):
        self.last_status = time.time()
        sys.stdout.write("\r[")
        previous_complete = sum(map(lambda x: self.bottom_total/pow(4,x), range(self.current_level - 1)))
        #print "bottom_total:      ", self.bottom_total
        #print "current_level:     ", self.current_level
        #print "previous_complete: ", previous_complete
        #print "current_complete:  ", self.current_levelcomplete
        percent = (previous_complete + self.current_levelcomplete) / float(self.big_total)
        #print percent
        bars = int(percent * (self.term_cols - 4))
        right = self.term_cols-bars - 4
        sys.stdout.write("=" * bars)
        sys.stdout.write("." * right)
        sys.stdout.write("]")
        sys.stdout.flush()
        ##print "cats"
        #print 

    def update():
        pass
