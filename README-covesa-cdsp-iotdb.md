# Support for Apache IoTDB and the COVESA Central Data Service Playground (CDSP)
This work adds support for the CAN Provider to write to the Apache IoTDB timeseries database used in the COVESA Central Data Service Playground as a new northbound client type `apache_iotdb`.


## Features supported
+ Supports `--dbc2val` mode to write CAN converted VSS data northbound to Apache IoTDB.

+ Currently does not support `--val2dbc` mode to write southbound from Apache IoTDB back to CAN as the behaviour for values written into the database would be use-case specific.

+ Does not currently support the CAN Provider subscriptions feature. Although that could be easily added once IoTDB v1.3.4 is adopted which supports subscriptions via SQL.


## Config
IoTDB server connection defaults are assumed when creating an IoTDB session.

IP address and port for the IoTDB server connection are set using the standard Provider controls.

IoTDB specific configuration defaults are set in the `iotdbclientwrapper.py` `init` method:
```
self._username_ = "root"
self._password_ = "root"
self._fetch_size = 1024
self._zone_id = "GMT+00:00"
self._device_id_ = "root.test2.vin123test.can"
```

### IoTDB timeseries path
`_device_id` is the path to which the VSS data will be written in IoTDB,
e.g. for `_device_id_ = "root.test2.vin123test.can"` the VSS node `Vehicle.Speed` will be written as the IoTDB timeseries `` root.test2.vin123test.can.`Vehicle.Speed` ``

## Runtime
Set the `--server-type` parameter to `apache_iotdb` either on the CLI or in the config file e.g:
```
./dbcfeeder.py --server-type apache_iotdb
```

Tip: By default the provider configuration will playback the CAN recording `candump.log`

## Notes
1) CAN Provider does not pass the CAN message timestamp to the client interface. As a result currently we use the host system time in ms as the timestamp when writing data to IoTDB.