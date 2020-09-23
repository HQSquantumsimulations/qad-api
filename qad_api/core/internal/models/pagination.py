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
