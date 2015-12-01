## Replication Manager

## DB Design

- Database Name : replications
- table Name : replications
- fields:
    - user_name, Good to group replications based on teams
    - id: integer
    - type: char (HIVE, HDFS)
    - start_time: Time
    - interval (1, 2, 3, 4,...)
    - interval_unit (MINUTE, HOUR, DAY, WEEK, MONTH, YEAR)
    - endtime
    - hdfs_source_path
    - hdfs_dest_path
    - hive_db_name
    - hive_table_name


### Testing tools and commands

*
```
    curl \
    -v \
    -H 'Content-Type: application/json' \
    -X PUT http://localhost:5000/create \
    -d '{
        "type": "HIVE",
        "start_time": ,
        "interval": ,
        "interval_unit": ,
        "endtime": ,
        "db_name": ,
        "table_name": ,
    }'
```

```
    curl \
    -v \
    -H 'Content-Type: application/json' \
    -X PUT http://localhost:5000/create \
    -d '{
        "type": "HDFS",
        "start_time": ,
        "interval": ,
        "interval_unit": ,
        "endtime": ,
        "hdfs_source_path": ,
        "hdfs_destination_path": ,
    }'
```


Users have control over the following variables
* Required values : Users should specify this to create a replication
    - type : type of replication
    - start_time : when the replication should run
    - interval : at what interval, replications should run
    - interval_unit : The unit of interval (day, hour, etc.)
    - end_time: endtime of the replication
    - hdfs_source_path : hdfs source path
    - hdfs_destination_path :  hdfs destination path
    - db_name : database name in case the replication type is Hive
    - table_name : the table names( comma separated, or regex or single name)
* Optional Values | Users may or may not specify this values, default value is True
    - alertOnSuccess
    - alertOnStart
    - alertOnAbort
    - alertOnFail

The remaining values are decided by Platform team.
These values are given to the program at the start of the process
* Required Values
    - source_clusterName
    - source_serviceName
    - peerName
    - hive_replicateData
    - hive_replicateImpalaMetadata
    - hdfs_skipChecksumChecks
    - hdfs_abortOnError
    - hdfs_mapreduceServiceName
    - hdfs_skipTrash
    - hdfs_preserveBlockSize
    - hdfs_preserveReplicationCount
    - hdfs_preservePermissions
    - hdfs_replicationStrategy
    - hdfs_removeMissingFiles

### TODO : Find out which is the key for setting up scheduler pools
