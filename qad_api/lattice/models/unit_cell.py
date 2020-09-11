from dataclasses import dataclass
from qad_api.core.internal.models.named_object import NamedObject

@dataclass
class UnitCell(NamedObject):
    """Not yet documented."""
    configuration: str

