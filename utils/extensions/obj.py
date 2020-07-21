import inspect


def get_obj_attrs(obj):
    for attr_name in dir(obj):
        if not inspect.ismethod(attr_name) \
                and not attr_name.startswith('_'):
            yield getattr(obj, attr_name)
