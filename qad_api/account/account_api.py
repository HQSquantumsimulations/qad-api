from qad_api.core.internal.module import Module

# models:
from qad_api.account.models.credits import Credits


class Account(Module):
    """API for managing the QAD user account.
    """

    def get_credits(self):
        return self._get('credits', Credits)
