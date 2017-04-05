class Options(dict):
    def __init__(self, strings, line=None):
        for pair in strings.split(','):
            key, val = pair.split('=')
            if key:
                self[key] = val
            # TODO(david): error
