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

"""Exceptions used in the QAD API Python library."""

from requests import Response


class RestApiError(Exception):
    """Superclass for levels which occurred on the REST API level.

    This exception (or a subclass of it) might be raised by any API request wrapper.
    Note that not always a specific subclass is being raised, so do not consider this
    class being "abstract". However, for some errors the raised exception is an
    instance of a subclass which more specificly tells you what went wrong.

    Parameters:
        response: The response object on REST API (HTTP) level.
        message: A message describing what went wrong.
    """
    def __init__(self, message: str, response: Response) -> None:
        """Initialization of the exception object.

        Args:
            response: The response object on REST API (HTTP) level.
            message: A message describing what went wrong.
        """
        super().__init__(message)
        self.response = response


class NotFoundError(RestApiError):
    """Object not found.

    This exception is raised whenever an object is queried which is not
    found in the backend. This can mean that there is no such object with
    the queried ID, or that the object doesn't belong to the user which
    is currently logged in.

    Parameters:
        message: Usually, the message does not tell you more details about the error.
    """
    def __init__(self, message: str, response: Response) -> None:
        """Initialization of the exception object.

        Args:
            response: The response object on REST API (HTTP) level.
            message: A message describing what went wrong.
        """
        super().__init__(message, response)


class ConsistencyError(RestApiError):
    """Consistency check failed.

    This exception is raised whenever an attempt is being made to save
    (create or update) an object, but the content is not consistent.

    Parameters:
        message: A detailed explanation about what went wrong during the consistency check.
    """
    def __init__(self, message: str, response: Response) -> None:
        """Initialization of the exception object.

        Args:
            response: The response object on REST API (HTTP) level.
            message: A message describing what went wrong.
        """
        super().__init__(message, response)


class DownloadError(RestApiError):
    """Download failed.

    This exception is raised whenever downloading a file (usually a job's
    result file) failed.

    Parameters:
        message: A detailed explanation about what went wrong during downloading the file.
    """
    def __init__(self, message: str, response: Response) -> None:
        """Initialization of the exception object.

        Args:
            response: The response object on REST API (HTTP) level.
            message: A message describing what went wrong.
        """
        super().__init__(message, response)
