
class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def create_enum(options):
    values = list([item[1] for item in options])
    constants = dict([(item[0], item[1]) for item in options])
    return values, Struct(**constants)
