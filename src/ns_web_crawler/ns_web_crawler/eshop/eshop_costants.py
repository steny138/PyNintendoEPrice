import re

def check_nsuid(nsuid):
    if not nsuid:
        return False

    match = re.match(r'7\d+$', nsuid)

    return not match is None