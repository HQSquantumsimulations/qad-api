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

from __future__ import annotations
from qad_api.core.internal.util.serialization import serialize, deserialize
from typing import Union, cast


Symbolic_self = str
"""A dummy type for using a symbolic value of 'self' in function argument default 
alues (instead of self).
"""


class Module:
    def __init__(self, parent, session, subpath = ''):
        self._parent = parent
        self._session = session
        self._subpath = subpath
        self._submodules = {}

    @property
    def _path(self):
        """
        Construct the path according to the module chain.
        """
        if self._parent:
            base = self._parent._path
        else:
            base = ''
        return base + self._subpath
    


    def _submodule(self, submodule_class: type, subpath: str = ''):
        """
        Create a new or reuse an existing object for a sub-module.

        Reuses the existing instance of the submodule class if and only if that
        was requested for the same subpath.

        submodule_class(type): The class which represents the submodule.

        subpath(str): The subpath which is appended to this module's path.
            This needs to end with a slash (or be empty).
        """
        # Make sure that paths always end with a slash
        if subpath and subpath[-1] != '/':
            subpath += '/'
        instance_id = f"{submodule_class.__name__}[{subpath}]"
        if instance_id not in self._submodules:
            self._submodules[instance_id] = submodule_class(self, self._session, subpath)
        return self._submodules[instance_id]



    def _request(self, method: str, subpath: str, data: any,
            target_class: any, target_module: Module = None, target_object = None):
        """
        Performs an HTTP request with the specified method to the given subpath.
        
        If data is given, it is serialized using serialize() and encoded as JSON
        and passed as the request's body.
        
        If a target_class is specified, the response is expected to have a body
        which is parsed as JSON and deserialized by deserialize().
        """
        # Construct path (avoid double slash)
        if subpath != '' and subpath[0] == '/':
            subpath = subpath[1:]
        path = self._path + subpath

        json = serialize(data, method)

        #print(f"- method:   {method}")
        #print(f"- path:     {path}")
        #print(f"- input:    {json}")

        # Actual request
        response = self._session.request(method, path, json=json)

        # Raise an exception for HTTP(S) level errors (4xx / 5xx status codes)
        response.raise_for_status()

        #print(f"- output:   {response.text}")
        #print("")

        # Note that not all requests have a body with JSON content
        try:
            json = response.json()
        except ValueError as e:
            if response.text:
                raise
            else:
                return None

        return deserialize(json, target_class, target_module, target_object)


    
    # Different HTTP request methods:

    def _get(self, subpath: str, target_class: type = None, target_module: Union[Module, Symbolic_self] = 'self', target_object = None) -> 'target_class':
        """
        Performs an HTTP GET request with the given subpath and interprets the
        result as an instance of the specified target_class.
        """
        # Convert the symbolic 'self' into the actual self
        if target_module == 'self':
            target_module = self
        target_module = cast(Module, target_module)

        return self._request('get', subpath, None, target_class, target_module, target_object)
        
    def _post(self, subpath: str, data: any = None, target_class: type = None, target_module: Union[Module, Symbolic_self] = 'self') -> 'target_class':
        """
        Performs an HTTP POST request with the given subpath and data, and
        interprets the result as an instance of the specified target_class.
        """
        # Convert the symbolic 'self' into the actual self
        if target_module == 'self':
            target_module = self
        target_module = cast(Module, target_module)

        return self._request('post', subpath, data, target_class, target_module)

    def _put(self, subpath: str, data: any = None) -> None:
        """
        Performs an HTTP PUT request with the given subpath and data.
        """
        self._request('put', subpath, data, None)

#    def _patch(self, subpath: str, data: any = None):
#        """
#        Performs an HTTP PATCH request with the given subpath and data.
#        """
#        return self._request('patch', subpath, data, None)

    def _delete(self, subpath: str) -> None:
        """
        Performs an HTTP DELETE request with the given subpath.
        """
        self._request('delete', subpath, None, None)
