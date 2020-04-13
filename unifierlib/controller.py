"""Controller Interface Class"""

import time
import datetime
import json
from typing import Union, Any, MutableSequence, MutableMapping
from types import SimpleNamespace
import requests
import urllib3

MAX_ERRORS = 1000

class Controller:
    """Provides an interface to the Ubqiuiti Unifi API"""
    # pylint: disable=too-many-arguments
    def __init__(self,
                 host: str,
                 port: int,
                 user: str,
                 password: str,
                 site: str = "default",
                 ssl_verify=False):
        """Class to interact with the controller API"""
        config = dict()
        config["host"] = host
        config["port"] = port
        config["site"] = site
        config["user"] = user
        config["password"] = password
        config["root_url"] = f"https://{host}:{port}"
        config["ssl_verify"] = ssl_verify

        session = requests.Session()
        session.verify = ssl_verify
        if not ssl_verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self._session = session
        self._config = SimpleNamespace(**config)

        self._logged_in = False
        self._error_stack = list()

        self.login()

    @property
    def logged_in(self):
        """The logged in state"""
        return self._logged_in

    def _push_error(self,
                    url: str,
                    response: requests.Response,
                    method: str,
                    parameters: Any = None):
        while len(self._error_stack) >= MAX_ERRORS:
            self._error_stack.pop(0)

        stack_entry = {
            "url": url,
            "response": response,
            "method": method,
            "parameters": parameters
        }
        stack_entry = SimpleNamespace(**stack_entry)

        self._error_stack.append(stack_entry)

    def login(self):
        """Log into the controller"""
        params = {
            "username": self._config.user,
            "password": self._config.password
        }

        login_url = f"{self._config.root_url}/api/login"

        result = self._session.post(login_url, json=params)

        if not result.ok:
            self._logged_in = False
            result.close()
            self._push_error(login_url,
                             result,
                             "POST",
                             parameters=params)
        else:
            self._logged_in = True

        return self._logged_in

    def _write_to_api(self,
                      relative_url: str,
                      method: str,
                      parameters: Union[dict, None] = None) -> Union[MutableMapping, None]:
        if not self._logged_in:
            return None
        url = f'{self._config.root_url}/api/s/{self._config.site}/{relative_url}'

        _method = self._session.post
        if method == "GET":
            _method = self._session.get

        if parameters:
            response = _method(url, json=parameters)
        else:
            response = _method(url)

        data = {}
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            pass
        if not response.ok:
            response.close()
            self._push_error(relative_url,
                             response,
                             "POST",
                             parameters=parameters)

        return data

    def get_daily_stats(self,
                        start: Union[float, None] = None,
                        end: Union[float, None] = None,
                        stat_attributes: list = None) -> Union[MutableSequence, None]:
        """Will return either a list of time-sorted daily stats or None"""
        if not self._logged_in:
            return None
        stats_url = f'stat/report/daily.site'

        if not stat_attributes:
            stat_attributes = [
                'wan-tx_bytes',
                'wan-rx_bytes',
                "time"
            ]
        if "time" not in stat_attributes:
            stat_attributes.append("time")
        if not end or end <= 0.0:
            end = time.time()

        # Shave the last hour, the controller seems to want this
        # This is also in keeping with Art-of-Wifi's library
        end = end - (end % 3600)

        if not start or start >= end:
            # Go to the beginning of this month
            end_t = time.localtime(end)
            start_dt = datetime.date(end_t.tm_year,
                                     end_t.tm_mon,
                                     1)
            start = time.mktime(start_dt.timetuple())

        # Time is in milliseconds since the Epoch
        end *= 1000
        start *= 1000

        params = {
            "attrs": stat_attributes,
            "end": end,
            "start": start
        }

        data = self._write_to_api(stats_url, "POST", parameters=params)

        if not data:
            return None

        meta = data["meta"]
        if meta["rc"] != "ok":
            return None

        data = data["data"]

        dailies = dict()

        for item in data:
            item_t = item.get("time", 0) / 1000 # Go Back to Seconds
            if item_t == 0:
                continue
            item["time"] = item_t
            dailies[item_t] = item

        return [dailies[key] for key in sorted(dailies.keys())]
