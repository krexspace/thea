
LOG_ENABLED = True
DEBUG_ENABLED = True

def log(*params):
    if LOG_ENABLED:
        print(*params)

def debug(*params):
    if DEBUG_ENABLED:
        print(*params)