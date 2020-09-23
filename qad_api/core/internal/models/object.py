# Copyright 2020 HQS Quantum Simulations GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
