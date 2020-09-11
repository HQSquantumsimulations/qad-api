from dataclasses import dataclass
from typing import TypeVar, Generic, List
import qad_api.core.internal.util as util

T = TypeVar('T')

@dataclass
class Pagination(Generic[T]):
    data: List[T]

    def _serialize(self):
        return util.serialize(self.data)

    @staticmethod
    def _deserialize(value: dict, target_class: type, module: 'Module'):
        T = target_class.__args__[0]
        assert(target_class == Pagination[T])
        return Pagination[T](util.deserialize(value['data'], List[T], module))
