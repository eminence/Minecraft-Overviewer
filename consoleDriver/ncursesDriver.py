import random
import curses

class ncursesDriver(object):
    def __init__(self):
        print "init curses driver"

        self.data = random.randint(0,9999)
        self.win = curses.initscr();
        curses.start_color()
       
        self.INFO_COLOR = 1
        curses.init_pair(self.INFO_COLOR, curses.COLOR_WHITE, curses.COLOR_BLACK)


        self.WARNING_COLOR = 2
        curses.init_pair(self.WARNING_COLOR, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        self.DEBUG_COLOR = 3
        curses.init_pair(self.DEBUG_COLOR, curses.COLOR_CYAN, curses.COLOR_BLACK)

        self.ERROR_COLOR = 4
        curses.init_pair(self.ERROR_COLOR, curses.COLOR_RED, curses.COLOR_BLACK)

        self.PROGRESS_COLOR1 = 5
        curses.init_pair(self.PROGRESS_COLOR1, curses.COLOR_WHITE, curses.COLOR_GREEN)
        self.PROGRESS_COLOR2 = 6
        curses.init_pair(self.PROGRESS_COLOR2, curses.COLOR_WHITE, curses.COLOR_BLUE)

        self.maxyx = self.get_term_size()
        width = self.maxyx[0]
        height = self.maxyx[1]

        self.log_win = curses.newwin(height - 10, width, 0, 0)
        self.log_win.scrollok(True)


        # create our status bar window.  this will sit on the bottom 10 linues of the terminal
        self.status_win = curses.newwin(10, width, height-10+1, 0)
        self.status_win.hline(0,0,curses.ACS_HLINE, width)
        self.status_win.addstr(1, 0, "this is the background window")
        self.status_win.refresh()

        curses.doupdate()

    def finish(self):
        #curses.nocbreak(); self.win.keypad(0); curses.echo()
        curses.endwin()
        print "del curses driver"

    def display_statusbar(self, **data):
        self.status_win.erase()
        width = self.maxyx[0]
        self.status_win.hline(0,0,curses.ACS_HLINE, width)

        level_percent = data['level_complete'] / float(data['level_total'])
        total_percent = data['total_complete'] / float(data['total'])

        self.status_win.addstr(1, 0, "Level: %d of %d" % (data['level'], data['total_levels']))
        self.status_win.addstr(2, 0, "This level: %d/%d" % (data['level_complete'], data['level_total']))

        # string lengths.  bleh
        level_text_size = len("This level: %d/%d" % (data['level_total'], data['level_total'])) + 2
        level_text_size = max(level_text_size, 
                len("Total: %d/%d" % (data['total'], data['total'])) + 2)

        
        # total length of the progress bar. 
        bar_width = width - level_text_size - 10

        self.status_win.addstr(3, 0, "Total: %d/%d" % (data['total_complete'], data['total']))
        #self.status_win.addstr(3, 0, "Total: %d" % (total_percent * 100))

        #self.status_win.addstr(5, 0, "Total: ")
        self.status_win.addstr(2, level_text_size, "[")
        self.status_win.addstr(2, level_text_size + 1, "=" * int(level_percent * bar_width), curses.color_pair(self.PROGRESS_COLOR1))
        self.status_win.addstr(2, level_text_size + 2 + bar_width, "]")
        self.status_win.addstr(2, level_text_size + 2 + bar_width + 2, "%d%%" % int(level_percent * 100))

        self.status_win.addstr(3, level_text_size, "[")
        self.status_win.addstr(3, level_text_size + 1, "=" * int(total_percent * bar_width), curses.color_pair(self.PROGRESS_COLOR2))
        self.status_win.addstr(3, level_text_size + 2 + bar_width, "]")
        self.status_win.addstr(3, level_text_size + 2 + bar_width + 2, "%d%%" % int(total_percent * 100))

        self.status_win.refresh()
        

    def print_info(self, msg):
        self.log_win.addstr("\n", curses.color_pair(self.INFO_COLOR))
        self.log_win.addstr(msg, curses.color_pair(self.INFO_COLOR))
        self.log_win.refresh()
        #self.win.update()
    
    def print_debug(self, msg):
        self.log_win.addstr("\n", curses.color_pair(self.DEBUG_COLOR))
        self.log_win.addstr(msg, curses.color_pair(self.DEBUG_COLOR))
        self.log_win.refresh()
    
    def print_error(self, msg):
        self.log_win.addstr("\n", curses.color_pair(self.ERROR_COLOR))
        self.log_win.addstr(msg, curses.color_pair(self.ERROR_COLOR))
        self.log_win.refresh()

    def print_warning(self, msg):
        self.log_win.addstr("\n", curses.color_pair(self.INFO_COLOR))
        self.log_win.addstr(msg, curses.color_pair(self.WARNING_COLOR))
        self.log_win.refresh()

    def get_term_size(self):
        yx= self.win.getmaxyx()
        return yx[1], yx[0]
