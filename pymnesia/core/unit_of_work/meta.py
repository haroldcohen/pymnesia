"""Provides with a metaclass for UnitOfWork.
"""
from pymnesia.core.common.originator_interface import OriginatorInterface
from pymnesia.core.entities.registry import DEFAULT_E_CLASSES_REGISTRY


class UnitOfWorkMeta(type(OriginatorInterface)):

    # noinspection PyMethodParameters
    def __new__(mcs, name, bases, attrs):
        attrs["__slots__"] = ["__state", "__replica"]
        for entity_cls_resolver in DEFAULT_E_CLASSES_REGISTRY.all_configs():  # pylint: disable=unused-variable
            attrs["__slots__"].append(entity_cls_resolver.__tablename__)

        # noinspection PyTypeChecker
        return super().__new__(mcs, name, bases, attrs)
