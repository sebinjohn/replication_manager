#!/usr/local/bin/python

from flask import Flask, jsonify
from config import Config

app = Flask(__name__)


@app.route('/')
@app.route('/api')
def api_root():
    return jsonify{'message': 'Welcome'}


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
    if input_data.has_key('type'):
        replication_type = input_data['type']
    else:
        return jsonify({'message': 'Replication type is not specified'})

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


@app.route('/validateconf', methods=['GET'])
def validate_conf():
    config = Config()
    config.validate_config()
    if not config:
        return jsonify({'error': "Invalid config file"})
    else:
        return jsonify({'result': 'Configuration Loaded'})

if __name__ == "__main__":
    app.run(debug=True)
