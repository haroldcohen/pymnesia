FILTER_FUNCTIONS_REGISTRY = {}


def register_filter_func(*, filter_name: str):
    """
    Allows to register a filter function
    :param filter_name: The filter name.
    """

    def decorator(func):
        FILTER_FUNCTIONS_REGISTRY[filter_name] = func

        return func

    return decorator
