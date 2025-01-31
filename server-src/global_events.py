def init():
    global _global_dict
    _global_dict = {}
    set_value("Detect_on", False)
    set_value("Lights_on", False)
    set_value("Music player running", False)


def set_value(name, value):
    _global_dict[name] = value


def get_value(name, def_value=None):
    try:
        return _global_dict[name]
    except KeyError:
        return def_value


def to_string():
    if _global_dict is None:
        return None
    else:
        return str(_global_dict)
