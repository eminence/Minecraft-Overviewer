import platform


def getDriver():
    if platform.system() == 'Windows':
        import winConsoleDriver
        return winConsoleDriver.winConsoleDriver()
    else:
        import lnxConsoleDriver
        return lnxConsoleDriver.lnxConsoleDriver()
