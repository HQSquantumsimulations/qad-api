from qad_api.core.internal.module import Module



class SCCE(Module):
    """
    Sub-API for solving lattice problems with the SCCE method.
    """

    @property
    def jobs(self):
        """
        Accessing the jobs of the current user.
        """
        from qad_api.lattice.scce.jobs import Jobs
        return self._submodule(Jobs, 'jobs/')
