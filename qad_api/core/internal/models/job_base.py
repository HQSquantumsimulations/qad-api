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

from qad_api.core.internal.models.named_object import NamedObject
from qad_api.core.internal.models.object import readonly_field
from qad_api.core.exceptions import DownloadError

import requests
import time
import asyncio
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class JobBase(NamedObject):
    execution_status: str           = readonly_field()
    """The status of the job's execution."""

    execution_start_date: datetime  = readonly_field()
    execution_end_date: datetime    = readonly_field()
    result_url: str                 = readonly_field()

    @property
    def is_created(self) -> bool:
        """Returns true if the job is in 'created' state.

        That means, it has been created, but another job of the same user is currently queued or running.
        When this other job is done, the next job will be queued for execution."""
        return self.execution_status == 'CREATED'

    @property
    def is_queued(self) -> bool:
        """Returns true if the job is being queued.

        That means, it is the next job to be executed and going to start as soon as resources are available."""
        return self.execution_status == 'QUEUED'

    @property
    def is_running(self) -> bool:
        """Returns true if the job is running.

        That means, it left the 'queued' state, but didn't finish yet. Please note that when you want to check
        if a job is pending, you should also need to take into account the 'created' and 'queued' state,
        for jobs which did not yet start running. For that, make use of the is_pending property."""
        return self.execution_status == 'STARTED' or self.execution_status == 'RUNNING'

    @property
    def is_pending(self) -> bool:
        """Returns true if the job is pending (either queued or running). The opposite is is_done."""
        return self.is_created or self.is_queued or self.is_running

    @property
    def is_successful(self) -> bool:
        """Returns true if the job finished its execution and was successful."""
        return self.execution_status == 'FINISHED'

    @property
    def is_aborted(self) -> bool:
        """Returns true if the job was aborted by a user interaction."""
        return self.execution_status == 'ABORTED'

    @property
    def is_failed(self) -> bool:
        """Returns true if the job was canceled due to a failure (for example, the available resources haven't been enough to execute it)."""
        return self.execution_status == 'FAILED'

    @property
    def is_done(self) -> bool:
        """Returns true if the job is done (either successfully or failed or aborted). The opposite is is_pending."""
        return self.is_successful or self.is_aborted or self.is_failed

    def download_result(self, filename: str) -> None:
        """Downloads the result file. Expects the status to be successful (raises DownloadError otherwise)."""
        if not self.is_successful:
            raise DownloadError("The job's status needs to be successful for the result file to be available.")

        r = requests.get(self.result_url)
        if r.status_code != 200:
            raise DownloadError(f"HTTP error while downloading the result file: {r.status_code} {r.text}")

        with open(filename, 'wb') as f:
            f.write(r.content)

    async def wait(self, check_interval: int = 30, with_console_feedback=True):
        """Asynchronously waits for the job to be done (or to fail / be aborted).

        This is a (non-blocking) coroutine which regularly checks via the API the status of the job."""
        start_time = time.time()
        while self.is_pending:
            interval = check_interval if self.is_running else 1 # Faster re-checks if job has not yet been started
            if with_console_feedback:
                for i in range(interval):
                    self._wait_console_feedback(time.time() - start_time)
                    await asyncio.sleep(1)
            else:
                await asyncio.sleep(interval)
            self._refresh()
        if with_console_feedback:
            self._wait_console_feedback(time.time() - start_time)
    
    def wait_blocking(self, check_interval: int = 30, with_console_feedback=True):
        """Synchronously waits for the job to be done (or to fail / be aborted).

        This is a blocking function which regularly checks via the API the status of the job."""
        start_time = time.time()
        while self.is_pending:
            interval = check_interval if self.is_running else 1 # Faster re-checks if job has not yet been started
            if with_console_feedback:
                for i in range(interval):
                    self._wait_console_feedback(time.time() - start_time)
                    time.sleep(1)
            else:
                time.sleep(interval)
            self._refresh()
        if with_console_feedback:
            self._wait_console_feedback(time.time() - start_time)

    def _wait_console_feedback(self, elapsed_time: Optional[int]):
        # Pretty format of time delta:
        mins = int(elapsed_time) // 60
        secs = int(elapsed_time) % 60
        elapsed_pretty: str
        elapsed_pretty = str(secs) + 's'
        if mins > 0:
            elapsed_pretty = str(mins) + 'm ' + elapsed_pretty

        # Pretty format of status:
        status_pretty: str
        if self.is_created:
            status_pretty = 'Job has been created (waiting to be queued)'
        elif self.is_queued:
            status_pretty = 'Job is queued (waiting for free resources)'
        elif self.is_running:
            status_pretty = 'Job is running'
        elif self.is_successful:
            status_pretty = 'Job has finished successfully'
        elif self.is_aborted:
            status_pretty = 'Job has been aborted'
        elif self.is_failed:
            status_pretty = 'Job has failed'
        else:
            status_pretty = f"Job is {self.execution_status}"

        line: str
        if self.is_pending:
            line = f'  Waiting... [{elapsed_pretty}]  -  {status_pretty}'
        else:
            line = f'  Done. [{elapsed_pretty}]  -  {status_pretty}'
        print(line + ' ' * (79 - len(line)), end='\r' if self.is_pending else '\n')