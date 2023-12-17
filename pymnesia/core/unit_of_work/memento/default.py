"""Provides with a memento for UnitOfWork.
"""
from pymnesia.core.unit_of_work.memento.meta import unit_of_work_metaclass
from pymnesia.core.entities.registry import registry  # pylint: disable=unused-import

__all__ = ["UnitOfWorkMemento"]


class UnitOfWorkMemento(metaclass=unit_of_work_metaclass(registry_=registry)):
    """Base class for UnitOfWorkMemento.

    @DynamicAttrs"""

    def __init__(self, **kwargs):
        pass
