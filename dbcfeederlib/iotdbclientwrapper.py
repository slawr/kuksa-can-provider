#!/usr/bin/env python3

# SPDX-FileCopyrightText: Copyright (c) 2025 Renesas Electronics
# SPDX-License-Identifier: MPL-2.0

import logging
from typing import Any, List

from dbcfeederlib import clientwrapper

from iotdb.Session import Session
import time

log = logging.getLogger(__name__)

class ApacheIoTDBClientWrapper(clientwrapper.ClientWrapper):
    """
    Client Wrapper using the Apache IoTDB Native Session API from the IoTDB Python client
    """
    # No default token path given as no default token included in packages/containers
    def __init__(self, ip: str = "127.0.0.1", port: int = 6667,
                 token_path: str = "",
                 tls: bool = False):
        """
        Init Databroker client wrapper, by default with TLS
        """
        log.info("IoTDB client wrapper init")
        super().__init__(ip, port, token_path, tls)
        self._connected = False
        self._token = ""
        # IoTDB configuration in addition to ip and port
        self._username_ = "root"
        self._password_ = "root"
        self._fetch_size = 1024
        self._zone_id = "GMT+00:00"
        self._device_id_ = "root.test2.vin123test.can"


    def _do_init(self):
        """
        Set up any additional init for IoTDB client wrapper
        """
## Todo: get IoTDB path?
        log.debug("No additional initialization necessary for Apache IoTDB server")


    def start(self):
        """
        Start connection to IoTDB server and authorize
        """
        log.info(f"Connecting to IoTDB server using {self._ip}:{self._port}")
        self._session = Session(self._ip, self._port, self._username_, self._password_, self._fetch_size, self._zone_id)
        self._session.open(False)


    def is_connected(self) -> bool:
        return self._session.is_open()

    def is_signal_defined(self, vss_name: str) -> bool:
        """
        Check if the signal is registered. If not log an error.
        Returns True if check succeeds.
        """
        log.debug("IoTDB: Checking if signal %s is registered", vss_name)
        return True

    def update_datapoint(self, name: str, value: Any) -> bool:
        """
        Update datapoint.
        Supported format for value is still a bit unclear/undefined.
        Like an a bool VSS signal both be fed as a Python bool and a string representing json true/false value
        (possibly with correct case)
        """
# todo: add session check before query
        vss_value_ = str(value)
        # Quote the VSS leaf node name
        iotdb_vss_name_ = '`{}`'.format(name)
# todo: Strangely the provider is not writing the TS. For now just write the current time in milliseconds.
        ts_ = time.time_ns() // 1_000_000
        # IoTDB does data type inference for basic types based on the timeseries schema
        log.debug(f"IoTB: update_datapoint({name}, {value}")
        log.debug(f"IoTB: insert_str is {self._device_id_}, {ts_}, {iotdb_vss_name_}, {vss_value_}")
        self._session.insert_str_record(self._device_id_, ts_, iotdb_vss_name_, vss_value_)
        return True

    def stop(self):
        log.info("Stopping databroker client")
        self._session.close()

    def supports_subscription(self) -> bool:
        log.debug("IoTB: supports_subscription() called")        
        return False

    async def subscribe(self, vss_names: List[str], callback):
        """Create a subscription and invoke the callback when data received."""
        log.error("IoTDB: subscribe() called but not implemented")