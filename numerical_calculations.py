
from models import EnergyStats
import statistics
from typing import List
    
def calculations(energy_levels: List[int]) -> EnergyStats:
    return EnergyStats(
        mean=statistics.mean(energy_levels),
        median=statistics.median(energy_levels),
        min=min(energy_levels),
        max=max(energy_levels),
        std_dev=statistics.stdev(energy_levels),
    )