import sys

class lnxConsoleDriver:
    def __init__(self):
        pass
        # wincon.h
        self.FOREGROUND_BLACK     = '30m'
        self.FOREGROUND_BLUE      = '34m'
        self.FOREGROUND_GREEN     = '32m'
        self.FOREGROUND_CYAN      = '36m'
        self.FOREGROUND_RED       = '31m'
        self.FOREGROUND_MAGENTA   = '35m'
        self.FOREGROUND_YELLOW    = '33m'
        self.FOREGROUND_GREY      = '37m'
        self.FOREGROUND_INTENSITY = '' # foreground color is intensified.

        self.BACKGROUND_BLACK     = '40m'
        self.BACKGROUND_BLUE      = '44m'
        self.BACKGROUND_GREEN     = '42m'
        self.BACKGROUND_CYAN      = '46m'
        self.BACKGROUND_RED       = '41m'
        self.BACKGROUND_MAGENTA   = '45m'
        self.BACKGROUND_YELLOW    = '43m'
        self.BACKGROUND_GREY      = '47m'
        self.BACKGROUND_INTENSITY = '' # background color is intensified.

    def set_text_attr(self, fore, back):
        sys.stdout.write("\x1b[%s\x1b[%s" % (fore,back))


    def ioctl_GWINSZ(self,fd):                  #### TABULATION FUNCTIONS
        try:                                ### Discover terminal width
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return None
        return cr

    def get_term_size(self):
        ### decide on *some* terminal size
        # try open fds
        cr = self.ioctl_GWINSZ(0) or self.ioctl_GWINSZ(1) or self.ioctl_GWINSZ(2)
        if not cr:
            # ...then ctty
            try:
                fd = os.open(os.ctermid(), os.O_RDONLY)
                cr = self.ioctl_GWINSZ(fd)
                os.close(fd)
            except:
                pass
        if not cr:
            # env vars or finally defaults
            try:
                cr = (env['LINES'], env['COLUMNS'])
            except:
                cr = (25, 80)
        # reverse rows, cols
        return int(cr[1]), int(cr[0])
        
