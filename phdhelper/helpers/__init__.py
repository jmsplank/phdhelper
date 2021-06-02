from .format_timestamps import *
import numpy as np


def title_print(*args, **kwargs):
    print("################ " + " ".join(map(str, args)) + " ################")


def array_summary(arr):
    shape = arr.shape
    final_str = f"{len(shape)}-D array of length {shape}.\n"

    def arr_stats(b_arr):
        mean = b_arr.mean()
        std = b_arr.std()
        zeros = (1 - (np.count_nonzero(b_arr) / len(b_arr))) * 100
        nans = np.count_nonzero(np.isnan(b_arr)) / len(b_arr) * 100
        _ = lambda x: f"{x:07.3f}"
        out_arr = [
            f"    mean:  {_(mean)} ",
            f"    std:   {_(std)} ",
            f"    %_0:   {_(zeros)} ",
            f"    %_nan: {_(nans)} ",
        ]
        return out_arr

    if len(shape) == 1:
        final_str += "\n".join(arr_stats(arr))
    elif len(shape) == 2:
        max_panels = 4 if shape[1] > 4 else shape[1]
        out = np.empty((max_panels, 5), dtype=np.dtype("U20"))
        for i in range(max_panels):
            out[i, 0] = f"    Index: {i+1:03d}/{shape[1]:03d} "
            out[i, 1:] = arr_stats(arr[:, i])
        # return '\n'.join([''.join(a) for a in out.T])
        final_str += "\n".join(["".join(a) for a in out.T])
    else:
        raise (
            NotImplementedError(
                f"Arrays with dimension >=3 are not supported. "
                f"Array {shape} has {len(shape)} dimensions."
            )
        )
    return final_str.strip()
