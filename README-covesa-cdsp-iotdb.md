# Support for Apache IoTDB and the COVESA Central Data Service Playground (CDSP)
> [!NOTE]
> This readme covers the extensions implemented in this fork. 
> For information on the wider upstream project see the [README.md](README.md)

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

### SocketCAN connection example
As noted in the tip above dbcfeeder can directly replay a CAN dump log file. However it can also connect to SocketCAN in linux. This enables access to the wide SocketCAN eco-system such as real and virtual CAN bus connections and user applications such as `SavvyCAN`, `Wireshark` and the SocketCAN `can-utils` user application suite including `canplayer`.

The following is an example of creating a virtual SocketCAN bus and using canplayer to play back the CAN dump `candump.log` as a data source.

1) Create virtual CAN bus:
```
./createvcan.sh vcan0
```

2) Playback `candump.log` on a loop to the virtual CAN in a separate terminal:
```
canplayer vcan0=elmcan -v -I candump.log -l i -g 1
```

3) Execute dbcfeeder to take southbound CAN msgs from the virtual CAN bus, convert the data to VSS and write it to Apache IoTDB northbound:
```
./dbcfeeder.py --server-type apache_iotdb --use-socketcan
```

## Notes
1) CAN Provider does not pass the CAN message timestamp to the client interface. As a result currently we use the host system time in ms as the timestamp when writing data to IoTDB.