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

from qad_api.core.internal import Module
from qad_api.core.session import Session


class QAD_API(Module):
    """Main handler and entry point for all interactions with the QAD API.

    Usually, when using the QAD API, you start with:

    .. code-block:: python

        from qad_api import QAD_API

        qad = QAD_API()

    Then, access the specific API functionality you want to use:

    .. code-block:: python

        qad.lattice.unit_cells.create(...)

    For a list of API functionalities, see the attributes of this class.
    """

    def __init__(
        self,
        session: Session = None
    ):
        """Construct a new API handler and authenticate with the backend.

        During initialization of the new object, the user is authenticated with
        the backend. For this, an attempt is being made to re-authenticate
        using a session handler stored in a file (similar to "cookies" in your
        browser). After some while (currently: 30 days), the stored session
        gets invalidated and a new authentication is required.

        For a fresh authentication, the user is prompted via console
        interaction to open up a URI in their browser, log in using their
        credentials in that browser window and copy-paste the code from the
        browser window back into the console prompt to finish the process.

        Args:
            session: Pass a :class:`Session` instance if you want more control over
                how the user is authenticated.
        """
        if session is None:
            # Create a new session and ask for authorization.
            session = Session()
            if not session.resume():
                if not session.authorize():
                    raise Exception("Failed to authorize!")

        super().__init__(None, session)

    @property
    def account(self):
        """API for managing the QAD user account.

        This attribute is an instance of the :class:`.Account` class.
        For the list of available sub-functionalities of this API
        see the attribute's documentation of :class:`.Account`.
        """
        from qad_api.account.account_api import Account
        return self._submodule(Account, f'users/{self._session.userid}/')

    @property
    def lattice(self):
        """Sub-API for solving lattice problems.

        This attribute is an instance of the :class:`.Lattice` class.
        For the list of available sub-functionalities of this API
        see the attribute's documentation of :class:`.Lattice`.
        """
        from qad_api.lattice.lattice_api import Lattice
        return self.account._submodule(Lattice, 'lattice/')
