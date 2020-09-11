from dataclasses import dataclass
from datetime import datetime

@dataclass
class Credits:
    credits: int
    executionTime: int
    lastRenewal: datetime
    nextRenewal: datetime
