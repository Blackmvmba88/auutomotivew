"""BlackMamba AutoFactory AI: reproducible synthetic production-line baseline."""
from dataclasses import dataclass
import random

@dataclass(frozen=True)
class Shift:
    planned_minutes: int
    downtime_minutes: int
    ideal_cycle_seconds: float
    total_units: int
    good_units: int


def metrics(s: Shift) -> dict[str, float]:
    if not (s.planned_minutes > 0 and 0 <= s.downtime_minutes < s.planned_minutes):
        raise ValueError('Invalid planned or downtime minutes')
    if s.ideal_cycle_seconds <= 0 or s.total_units <= 0 or not 0 <= s.good_units <= s.total_units:
        raise ValueError('Invalid cycle time or units')
    runtime = s.planned_minutes - s.downtime_minutes
    availability = runtime / s.planned_minutes
    performance = min(1.0, s.ideal_cycle_seconds * s.total_units / (runtime * 60))
    quality = s.good_units / s.total_units
    return {'availability': availability, 'performance': performance,
            'quality': quality, 'oee': availability * performance * quality}


def simulate(seed: int = 42, shifts: int = 30) -> list[dict[str, float]]:
    if shifts < 1:
        raise ValueError('shifts must be positive')
    rng = random.Random(seed)
    result = []
    for i in range(shifts):
        downtime = rng.randint(15, 85)
        runtime = 480 - downtime
        units = int(runtime * 60 / rng.uniform(62, 75))
        good = units - rng.randint(0, max(1, units // 18))
        result.append({'shift': i + 1, **metrics(Shift(480, downtime, 60, units, good))})
    return result

if __name__ == '__main__':
    import json
    print(json.dumps(simulate()[:3], indent=2))
