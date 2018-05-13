
LOG_ENABLED = False

def log(*params):
    if LOG_ENABLED:
        print(*params)