from ctypes import windll, Structure, c_short, c_ushort, byref, create_string_buffer

SHORT = c_short
WORD  = c_ushort


class COORD(Structure):
    """struct in wincon.h."""
    _fields_ = [
    ("X", SHORT),
    ("Y", SHORT)]

class SMALL_RECT(Structure):
  """struct in wincon.h."""
  _fields_ = [
    ("Left", SHORT),
    ("Top", SHORT),
    ("Right", SHORT),
    ("Bottom", SHORT)]


class CONSOLE_SCREEN_BUFFER_INFO(Structure):
    """struct in wincon.h."""
    _fields_ = [
    ("dwSize", COORD),
    ("dwCursorPosition", COORD),
    ("wAttributes", WORD),
    ("srWindow", SMALL_RECT),
    ("dwMaximumWindowSize", COORD)]

class winConsoleDriver:

    def __init__(self):
        self.STD_INPUT_HANDLE = -10
        self.STD_OUTPUT_HANDLE = -11
        self.STD_ERROR_HANDLE = -12

        # wincon.h
        self.FOREGROUND_BLACK     = 0x0000
        self.FOREGROUND_BLUE      = 0x0001
        self.FOREGROUND_GREEN     = 0x0002
        self.FOREGROUND_CYAN      = 0x0003
        self.FOREGROUND_RED       = 0x0004
        self.FOREGROUND_MAGENTA   = 0x0005
        self.FOREGROUND_YELLOW    = 0x0006
        self.FOREGROUND_GREY      = 0x0007
        self.FOREGROUND_INTENSITY = 0x0008 # foreground color is intensified.

        self.BACKGROUND_BLACK     = 0x0000
        self.BACKGROUND_BLUE      = 0x0010
        self.BACKGROUND_GREEN     = 0x0020
        self.BACKGROUND_CYAN      = 0x0030
        self.BACKGROUND_RED       = 0x0040
        self.BACKGROUND_MAGENTA   = 0x0050
        self.BACKGROUND_YELLOW    = 0x0060
        self.BACKGROUND_GREY      = 0x0070
        self.BACKGROUND_INTENSITY = 0x0080 # background color is intensified.

        self.stdout_handle = windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)
        self.SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute
        self.GetConsoleScreenBufferInfo = windll.kernel32.GetConsoleScreenBufferInfo
        self.GetConsoleTitle = windll.kernel32.GetConsoleTitleA

    def _win_get_console_title(self):
        s = create_string_buffer('\000' * 128)
        len = self.GetConsoleTitle(s, 128)
        return s[0:len]

    def _win_set_text_attr(self,color):
        self.SetConsoleTextAttribute(self.stdout_handle, color)


    def set_text_attr(self,fore, back):
        self._win_set_text_attr(fore | back)

    def get_term_size(self):
        csbi = CONSOLE_SCREEN_BUFFER_INFO()
        self.GetConsoleScreenBufferInfo(self.stdout_handle, byref(csbi))
        return (csbi.dwMaximumWindowSize.X, csbi.dwMaximumWindowSize.Y)
