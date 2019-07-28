try:
    WindowsError
except NameError:
    WINDOWS = False
else:
    WINDOWS = True