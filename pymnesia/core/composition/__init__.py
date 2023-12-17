from functools import reduce


def curry(func):
    """Provides with curry like functions"""
    f_args, f_kwargs = [], {}  # pylint: disable=unused-variable

    def f(*args, **kwargs):  # pylint: disable=invalid-name
        nonlocal f_args, f_kwargs
        if args or kwargs:
            f_args += args
            f_kwargs.update(kwargs)
            return f
        result = func(*f_args, **f_kwargs)
        f_args, f_kwargs = [], {}
        return result

    return f


def runner(func, *args, **kwargs):
    """Simple composition function"""

    def f(*f_args, **f_kwargs):  # pylint: disable=invalid-name
        f_kwargs.update(kwargs)

        return func(*f_args + args, **f_kwargs)

    f.__name__ = func.__name__

    return f


def composite(*func):
    """Functional composition"""

    def compose(g, f):  # pylint: disable=invalid-name
        def h(*args, **kwargs):  # pylint: disable=invalid-name
            return g(f(*args, **kwargs), **kwargs)

        return h

    return reduce(compose, func)
