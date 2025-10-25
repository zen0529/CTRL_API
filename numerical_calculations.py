
from models import EnergyStats
import statistics
from typing import List
from scipy.stats import linregress
import numpy as np



    
def calculations(energy_levels: List[int]) -> EnergyStats:
    
    x = np.arange(len(energy_levels))  # [0, 1, 2, 3, 4, 5, 6]
    
    #edge case where checkin is less than 2
    if len(energy_levels) < 2:
        slope = 0
        _std_dev = 0
        
    else:
       # Compute linear regression and obtaining trend slope
        slope, intercept, r_value, p_value, std_err = linregress(x, energy_levels)
        _std_dev = statistics.stdev(energy_levels)
      

    
    return EnergyStats(
        mean=statistics.mean(energy_levels),
        median=statistics.median(energy_levels),
        min=min(energy_levels),
        max=max(energy_levels),
        std_dev= _std_dev,
        trend_slope=slope
    )