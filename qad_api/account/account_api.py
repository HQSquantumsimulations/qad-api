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

"""API for managing the QAD user account.

*Not yet documented.*
"""

from qad_api.core.internal.module import Module
from qad_api.account.models.credits import Credits


class Account(Module):
    """API for managing the QAD user account.

    *Not yet documented.*
    """

    def get_credits(self) -> Credits:
        """*Not yet documented.*

        Returns:
            *Not yet documented.*
        """
        return self._get('credits', Credits)
