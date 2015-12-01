from flask import Flask, url_for, request
from pykwalify.core import Core
from replications.replications import *

class ReplicationManager(Flask):
    def __init__(self):
        Flask.__init__(self, __name__)
        refresh_configs()
        api = self.configs.get('api')
        self.api_connect = ApiConnect(
            api.get('host'),
            api.get('port'),
            api.get('version'),
            (api.get('user'), api.get('pass')))
        self.cluster = OmniaCluster(
            self.configs.get('cluster').get('name'), self.api_connect)

    @app.route('/')
    @app.route('/api')
    def api_root():
        return "Welcome"

    @app.route('/v1.0')
    def api_version():
        version = 1
        return "Welcome"

    @app.route('/run/<rid>', methods=['POST'])
    def run_replication(rid):
        return "Running replication with id : " + str(rid)

    @app.route('/delete/<rid>', methods=['DELETE'])
    def delete_replication(rid):
        return "Deleting replication with id: " + str(rid)

    @app.route('/view/<rid>', methods=['GET'])
    def view_replication(rid):
        return "Here is the replication with id: " + str(rid)

    @app.route('/update/<rid>', methods=['PUT'])
    def update_replication(rid):
        return "Updating the replication with id: " + str(rid)

    @app.route('/create', methods=['PUT'])
    def create_replication():
        input_data = request.json
        replication_type = None
        if input_data.has_key('type'):
            replication_type = input_data['type']
        else:
            return 'Replication type is not specified'

        if replication_type == 'HIVE':
            service_name = self.configs.get('destination').get('hive_service_name')
        elif replication_type == 'HDFS':
            service_name = self.configs.get('destination').get('hdfs_service_name')
        else:
            return "Error: Unknown replication type"

        service_repl = BDR_Replications(self.api_connect, self.cluster, service_name)
        schedule = ReplicationSchedule(replication_type)
        err = schedule.validate_user_input(user_input)
        if err:
            return str(err)
        else:
            repl = create_replication_schedule_from_input(input_data)
            rid = service_repl.create_replication_schedule(repl)
            f = {'replication_id': rid}
            return flask.jsonify(**f)

    @app.route('/refreshconf')
    def refresh_configs():
        config = validate_config()
        if not config:
            return flask.jsonify({'error': "Invalid config file"})
        for item in config:
            for k, v in item.iteritems():
                self.configs[k] = v

    def validata_config():
        try:
            c = Core(source_file="bdr_app.yml", schema_files=['schema.yml'])
            return c.validate(raise_exception=True)
        except Exception as e:
            print "LOG: ERROR: config file is not valid"
            print e
            return None
if __name__ == "__main__":
    app.run()
