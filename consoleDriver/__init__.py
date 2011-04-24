import platform

_driver = None


def getDriver():
    global _driver

    if _driver:
        print "returning existing driver"
        return _driver

    try:
        import curses
    except ImportError:
        print "we don't have curses on this platform"

    import ncursesDriver
    _driver = ncursesDriver.ncursesDriver()
    return _driver

    if platform.system() == 'Windows':
        import winConsoleDriver
        return winConsoleDriver.winConsoleDriver()
    else:
        import lnxConsoleDriver
        return lnxConsoleDriver.lnxConsoleDriver()
