"""A collection of utility functions"""

import json
import time
from typing import Union, Tuple, MutableMapping

WAN_TX_KEY = "wan-tx_bytes"
WAN_RX_KEY = "wan-rx_bytes"
TIME_KEY = "time"

SCALING_FACTORS = {
    (0, 1024): (1, "B"),
    (1024, 1024**2): (1024, "KB"),
    (1024**2, 1024**3): (1024**2, "MB"),
    (1024**3, 1024**4): (1024**3, "GB"),
    (1024**4, 1024**5): (1024**4, "TB"),
    (1024**5, 1024**6): (1024**5, "PB"),
    (1024**6, 1024**7): (1024**6, "EB"),
    (1024**7, 1024**8): (1024**7, "ZB"),
    (1024**8, 1024**9): (1024**8, "YB"),
}

DEFAULT_SCALE = (1024**3, "GB")

def humanize_bytes(size: float) -> Tuple[float, str]:
    """Returns bytes in a humanized form"""
    scaling = -1
    unit = "B"
    # pylint: disable=dict-iter-missing-items
    # The keys of SCALING_FACTORS are tuples
    for lower, upper in SCALING_FACTORS:
        if lower <= size < upper:
            scaling, unit = SCALING_FACTORS[(lower, upper)]
            break
    if scaling == -1:
        scaling, unit = DEFAULT_SCALE

    return size / scaling, unit

class HumanizedByte:
    """Shows bytes in a human-friendly form"""
    def __init__(self,
                 size: float,
                 rounding=None):
        self._size = size
        self._size_scaled, self._size_unit = humanize_bytes(size)
        if not rounding:
            rounding = 2
        self.rounding = rounding

    @property
    def size_raw(self):
        """The raw size the instance was constructed with"""
        return self._size

    @property
    def size(self):
        """Size scaled to a human value"""
        return self._size_scaled

    @property
    def unit(self):
        """Unit of the scaled value"""
        return self._size_unit

    @property
    def size_str(self):
        """Convenience string showing the scaled value and it's unit"""
        return f'{round(self.size, self.rounding)} {self.unit}'

    def __str__(self):
        """Shows the convenience string"""
        return self.size_str

    def __repr__(self):
        """Suitable representation for recreating the instance"""
        cls_name = self.__class__.__name__
        return f"{cls_name}({self.size_raw})"

def summarize_stats(stats: dict,
                    time_fmt: str,
                    do_json=False,
                    do_list=False):
    """Collects and summarizes statistics"""
    if not stats:
        return
    total_tx = 0
    total_rx = 0
    for stat_entry in stats:
        total_tx += stat_entry[WAN_TX_KEY]
        total_rx += stat_entry[WAN_RX_KEY]
    total = total_rx + total_tx

    total_tx = HumanizedByte(total_tx)
    total_rx = HumanizedByte(total_rx)
    total = HumanizedByte(total)

    if not do_json:
        if do_list:
            for stat_entry in stats:
                t_x = stat_entry[WAN_TX_KEY]
                r_x = stat_entry[WAN_RX_KEY]
                total_i = HumanizedByte(t_x + r_x)
                t_x = HumanizedByte(t_x)
                r_x = HumanizedByte(r_x)
                time_str = time.strftime(time_fmt,
                                         time.gmtime(stat_entry["time"]))
                print(f"{time_str}: Up: {t_x}; Down: {r_x}; Total: {total_i}")
        print(f'Total: Up: {total_tx}; Down: {total_rx}; Total: {total}')
    else:
        print(json.dumps(stats))

def reorganize_site_data(data: MutableMapping) -> Union[None, MutableMapping]:
    """Attempts to reorganize the site data in a more helpful way, as a dict by name of the site"""
    if not data:
        return None
    if not 'meta' in data:
        return data

    if data['meta'] != {"rc": "ok"}:
        return data

    data = data["data"]

    sites_dict = {site["name"]: site for site in data}

    return sites_dict
