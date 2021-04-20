from datetime import timedelta
from datetime import datetime as dt
from typing import Tuple, List


def format_timestamps(
    tick_start: str,
    num: int = 10,
    tick_step: Tuple[str, float] = ("minutes", 2),
    label_format: str = "%H:%M",
) -> Tuple[List[int], List[str]]:
    times = [dt.strptime(tick_start, "%Y-%m-%d/%H:%M:%S")]
    step = {tick_step[0]: tick_step[1]}
    for i in range(num - 1):
        times.append(times[i] + timedelta(**step))
    times_names = [dt.strftime(i, label_format) for i in times]
    times_locs = [dt.timestamp(i) for i in times]
    return times_locs, times_names