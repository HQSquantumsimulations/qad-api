from dataclasses import dataclass
from qad_api.core.internal.models.object import Object

@dataclass
class NamedObject(Object):
    name: str
