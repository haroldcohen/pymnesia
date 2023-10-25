from pymnesia.composition import curry


def order_by(entities: list, direction: str, order_by_key: str):
    return sorted(entities, key=lambda e: getattr(e, order_by_key), reverse=direction == "desc")


curried_order_by = curry(order_by)
