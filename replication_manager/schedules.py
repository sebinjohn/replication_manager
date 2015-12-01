import yaml
class ReplicationSchedule(object):

    def __init__(self, replication_type):
        self.replication_type = replication_type.lower()
        if self.replication_type not in ['hive', 'hdfs']:
            raise Exception('Unsupported Replication Type')


    def create_hdfs_arguments(self, user_input):
        """
        "hdfsArguments": {
            "abortOnError": false,
            "destinationPath": "/user/johns5/",
            "dryRun": false,
            "mapreduceServiceName": "MapReduce",
            "preserveBlockSize": true,
            "preservePermissions": true,
            "preserveReplicationCount": true,
            "removeMissingFiles": false,
            "replicationStrategy": "STATIC",
            "skipChecksumChecks": false,
            "skipTrash": false,
            "sourcePath": "/user/johns5/input_data",
            "sourceService": {
                "clusterName": "test-cluster",
                "peerName": "iSAAC_3",
                "serviceName": "HDFS"
            }
        },
        """
        """
        When the replication type is HDFS we have to specify the source and destination path
        When the replication type is HIVE we don't have to specify the source and destination path
        """
        repl_type = self.replication_type
        hdfsArguments = {
            'abortOnError': self.defaults['abort']['on_error']
            'dryRun': False,
            'mapreduceServiceName': self.defaults['destination']['mapreduce_service_name'],
            'preserveBlockSize': self.defaults['hdfs']['preserve_block_size'],
            'preservePermissions': self.defaults['hdfs']['preserve_permissions'],
            'preserveReplicationCount': self.defaults['hdfs']['preserve_replication_count'],
            'removeMissingFiles': self.defaults['hdfs']['remove_missing_files']
            'replicationStrategy': self.defaults['hdfs']['replication_strategy'],
            'skipChecksumChecks': self.defaults['hdfs']['skip_checksum_checks'],
            'skipTrash' = self.defaults['hdfs']['skip_trash']
        }
        if repl_type.lower() == 'hdfs':
            hdfsArguments['sourcePath'] = self.user_data['hdfs']['source_path']
            hdfsArguments['destinationPath'] = self.user_data['hdfs']['destination_path']
            hdfsArguments['sourceService'] = {
                'clusterName': self.defaults['source']['cluster_name'],
                'peerName': self.defaults['source']['peer_name'],
                'serviceName': self.defaults['source']['hdfs_service_name']
            }

    def create_hive_argument(data):
        o = {}
        """"hiveArguments": {
        "dryRun": false,
        "force": false,
        "hdfsArguments": {
            "abortOnError": false,
            "dryRun": false,
            "mapreduceServiceName": "mapreduce1",
            "preserveBlockSize": true,
            "preservePermissions": true,
            "preserveReplicationCount": true,
            "removeMissingFiles": false,
            "replicationStrategy": "STATIC",
            "skipChecksumChecks": false,
            "skipTrash": false
        },
        "replicateData": true,
        "replicateImpalaMetadata": false,
        "sourceService": {
            "clusterName": "cluster",
            "peerName": "Scoring",
            "serviceName": "hive01"
        },
        "tableFilters": [
            {
                "database": "pd_features",
                "tableName": ".*"
            }
        ]
    }"""
        hiveArguments = {
            'dryRun': False,
            'force': False,
            'hdfsArguments': self.create_hdfs_arguments(self.user_data),
            'replicateData': True,
            'replicateImpalaMetadata': self.defaults['hive']['replicate_impala_metadata'],
            'sourceService': {
                'clusterName': self.defaults['source']['cluster_name'],
                'peerName': self.defaults['cluster']['peer_name'],
                'serviceName': self.defaults['source']['hive_service_name']
            },
            'tableFilters': {
                'database': self.user_input['hive']['hive_database'],
                'tableName': self.user_input['hive']['hive_tables']
            }
        }

    def validate_user_input(self):
        errors = True
        return errors

    def create_replication_schedule_from_input(self, user_input):
        self.user_input = user_input
        errors = validate_user_input()
        if not errors:
            raise Exception(str(errors))

        repl = {}
        if self.replication_type == 'HIVE':
            db_name = user_input['hive']['source_db']
            table_names = user_input['hive']['source_tables']
            hive_args = self.create_hive_argument(user_input)
            if hive_args:
                repl['hiveArguments'] = hive_args['hiveArguments']
            else:
                raise Exception('Hive Argument creation failed')
        elif replication_type == 'HDFS':
            hdfs_args = self.create_hdfs_arguments()
            if hdfs_args:
                repl['hdfsArguments'] = hdfs_args['hdfsArguments']
        else:
            print "Unknown replication type : " + replication_type

        repl["alertOnAbort"] = self.default['alert']['on_abort']
        repl["alertOnFail"] = self.default['alert']['on_fail']
        repl["alertOnStart"] = self.default['alert']['on_start']
        repl["alertOnSuccess"] = self.default['alert']['on_success']

        repl["interval"] = user_input['schedule']['interval']
        repl["intervalUnit"] = user_input['schedule']['interval_unit']
        repl["startTime"] = user_input['schedule']['start_time']
        repl["paused"] = False
        return repl
