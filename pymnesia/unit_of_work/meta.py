"""Provides with a metaclass for UnitOfWork.
"""
from pymnesia.common.originator_interface import OriginatorInterface
from pymnesia.entities.registry import registry


class UnitOfWorkMeta(type(OriginatorInterface)):

    # noinspection PyMethodParameters
    def __new__(mcs, name, bases, attrs):
        attrs["__slots__"] = ["__state", "__replica"]
        for entity_cls_resolver in registry.all_configs():  # pylint: disable=unused-variable
            attrs["__slots__"].append(entity_cls_resolver.__tablename__)

        # noinspection PyTypeChecker
        return super().__new__(mcs, name, bases, attrs)
