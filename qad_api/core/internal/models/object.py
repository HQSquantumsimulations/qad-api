from datetime import datetime
from dataclasses import dataclass, field, MISSING, fields
import typing
from qad_api.core.internal.util.serialization import serialize, deserialize


def readonly_field(init_value=None, include_in_post=False, include_in_put=False, include_in_patch=False):
    include_in = []
    if include_in_post: include_in.append('post')
    if include_in_put: include_in.append('put')
    if include_in_patch: include_in.append('patch')
    return field(
        default=init_value,
        init=False,
        metadata={'qad_api': {'include_in': include_in}}
    )


@dataclass
class Object:
    id: str                = readonly_field()
    created_date: datetime = readonly_field()
    updated_date: datetime = readonly_field()


    def _refresh(self) -> None:
        self._module._get(self.id, type(self), target_object=self)
