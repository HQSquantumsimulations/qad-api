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

from dataclasses import is_dataclass, fields
from datetime import datetime
import typing


# Public interface:

def serialize(value: any, for_method: str = ''):
    """
    Given an instance of a class, returns its attributes as a dict.
    The type of the given object needs to be a dataclass.
    """
    if value is None:
        return None

    elif hasattr(value, "_serialize") and callable(value._serialize):
        return value._serialize(for_method)

    elif is_dataclass(type(value)):
        return _serialize_dataclass(value, for_method)

    elif type(value) == list:
        return _serialize_list(value, for_method)
   
    elif type(value) == datetime:
        # Serialize datetime as ISO format (to string)
        return value.isoformat()
    
    elif type(value) == int:
        # Force float for numbers (as JSON technically doesn't have an int)
        return float(value)

    elif type(value) in (float, str, bool):
        # Default case: use value as is
        return value
   
    raise Exception(f"Incompatible type: {type(value)}")


def deserialize(value: any, target_type: type, module: 'Module', target_object = None):
    """
    Creates an instance of a type / class by the value / attributes given as a primitive type / list / dict.
    """
    if target_type is None:
        return None

    elif hasattr(target_type, "_deserialize") and callable(target_type._deserialize):
        if target_object is not None:
            raise Exception(f"Serializing into existing instance of {target_type} not supported, since it implemented an instance method _serialize().")
        return target_type._deserialize(value, target_type, module)
    
    elif is_dataclass(target_type):
        if not isinstance(value, dict):
            raise Exception(f"For deserializing a {target_type}, a dict is expected, but a {type(value)} was given.")
        if target_object is not None and type(target_object) != target_type:
            raise Exception(f"For deserializing a {target_type} into an existing instance, exactly such a type needs to be passed as target_object, but a {type(target_object)} was given.")
        return _deserialize_dataclass(value, target_type, module, target_object)

    elif type(target_type) == typing._GenericAlias:
        if target_type.__origin__ == list:
            if type(value) != list:
                raise Exception(f"To deserialize a List[T], a list is expected.")
            return _deserialize_list(value, target_type, module)
#        elif is_dataclass(target_type.__origin__):
#            return _deserialize_dataclass(value, target_type)
        else:
            raise Exception(f"Generics in deserialize() are only implemented for some types. Apparently, {target_type.__origin__} is not one of them.")

    elif target_type == datetime:
        if value is None:
            return None
        # Parse datetime from ISO format (from string)
        assert type(value) == str, "A datetime field needs to be deserialized from a string."
        if value[-1] == 'Z': value = value[:-1] + '+00:00' # <-- The ISO format is allowed to use 'Z' as a synonym for '+00:00' (UTC), but datetime doesn't seem to allow that.
        return datetime.fromisoformat(value)

    elif target_type in (int, float):
        # We intentionally allow float <-> int conversion (as JSON technically doesn't have an int)
        if type(value) in (int, float):
            return target_type(value)
           
    elif target_type in (str, bool):
        # Default case: use value as is
        return value

    raise Exception(f"In dezerialize(), a {type(value)} was given, but a {target_type} was expected. They are not compatible.")



# Internal:

def _serialize_dataclass(obj, for_method: str = ''):
    serialization = {}
    for f in fields(obj):
        include = True
        if ('qad_api' in f.metadata) and ('include_in' in f.metadata['qad_api']):
            include = for_method in f.metadata['qad_api']['include_in']
        if include:
            key = _key_in_serialization(f.name)
            serialization[key] = serialize(getattr(obj, f.name), for_method)
    return serialization

def _deserialize_dataclass(serialization: dict, target_class: type, module: 'Module', target_object = None):
    assert is_dataclass(target_class)
    attributes_for_init = {}
    attributes_set_after_init = {}
    for f in fields(target_class):
        key = _key_in_serialization(f.name)
        if key not in serialization:
            raise Exception(f"Expected serialized data for deserializing a `{target_class}' to have an attribute `{key}' (for field `{f.name}'), but it doesn't have it: \n{serialization}")
        value = deserialize(serialization[key], f.type, module)
        if f.init and target_object is None:
            attributes_for_init[f.name] = value
        else:
            attributes_set_after_init[f.name] = value
    if target_object:
        obj = target_object
    else:
        obj = target_class(**attributes_for_init)
    for (name, value) in attributes_set_after_init.items():
        setattr(obj, name, value)
    obj._raw = serialization
    obj._module = module
    return obj

def _deserialize_list(serialization: list, target_class: type, module: 'Module'):
    element_class = target_class.__args__[0]
    return [deserialize(item, element_class, module) for item in serialization]

def _serialize_list(items: list, for_method: str = ''):
    return [serialize(item, for_method) for item in items]

def _key_in_serialization(internal_key: str) -> str:
    """
    Converts a name given in underscore notation (as used in python for the
    names of properties) into camel-case notation (as used by the JSON REST
    API). Names already in camel-case notation are kept unchanged.
    """
    words = internal_key.split('_')
    return words[0] + "".join([
        word[0].capitalize() + word[1:]
        for word in words[1:] if word
    ])
