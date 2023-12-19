from functools import reduce


def composite(*func):
    """Functional composition"""

    def compose(g, f):  # pylint: disable=invalid-name
        def h(*args, **kwargs):  # pylint: disable=invalid-name
            return g(f(*args, **kwargs), **kwargs)

        return h

    return reduce(compose, func)
