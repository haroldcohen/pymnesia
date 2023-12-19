"""Provides with miscellaneous entity test functions.
"""
import re

from tests.common_utils.helpers.entities.make.types import EntityClsParams
from tests.common_utils.helpers.entities.make.relations.types import RelatedEntityClassesParams
from tests.common_utils.helpers.types import FieldsConf

__all__ = ["generate_entity_cls_params"]


def generate_entity_cls_params(
        class_name: str,
        fields_conf: FieldsConf,
        rel_entity_classes_params: RelatedEntityClassesParams,
) -> EntityClsParams:
    """
    :param class_name:
    :param fields_conf:
    :param rel_entity_classes_params:
    :return:
    """
    lower_name = re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower()

    return EntityClsParams(
        name=class_name,
        table_name=lower_name + "s",
        fields_conf=fields_conf,
        rel_entity_classes_params=rel_entity_classes_params,
    )
