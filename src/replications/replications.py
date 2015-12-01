import json
import requests
from os import listdir
import os

from cm_api.api_client import ApiResource
from cm_api.endpoints.types import ApiHdfsReplicationArguments
from cm_api.endpoints.types import ApiHiveReplicationArguments

class OmniaCluster(object):
    def __init__(self, cluster_name, api_conn):
        self.cluster_name = cluster_name
        self.api_conn = api_conn

    def get_cluster(self):
        self.cluster = self.find_cluster()
        return self.cluster

    def get_cluster_name(self):
        return self.cluster_name

    def get_api(self):
        return self.api_conn

    def get_service(self, service_name):
        return self.find_service(service_name)

    def find_cluster(self):
        api = self.api_conn.get_api()
        return next((cluster for cluster in api.get_all_clusters() if cluster.name == self.cluster_name), None)

    def find_service(self, service_name):
        cluster = self.get_cluster()
        return next((service for service in self.cluster.get_all_services() if service.name == service_name), None)

class ApiConnect(object):

    def __init__(self, api_host, api_port, api_version, auth=('admin', 'admin')):
        self.api_host = api_host
        self.api_port = api_port
        self.api_version = api_version
        if len(auth) != 2:
            raise Exception('auth should have two values and two values only')
        else:
            self.auth = auth

    def get_api_host(self):
        return self.api_host

    def get_api_port(self):
        return self.api_port

    def get_api_version(self):
        return self.api_version

    def get_auth(self):
        return self.auth

    def get_api(self):
        try:
            return ApiResource(self.api_host, str(self.api_port), self.auth[0], self.auth[1], version=self.api_version)
        except Exception as e:
            print "Exception while creating api connectivity"
            print e
            return None


class BDR_Replications(object):

    def __init__(self, api_connect, cluster, service_name):
        self.api_connect = api_connect
        self.cluster = cluster
        self.service_name = service_name
        self.service = self.cluster.get_service(service_name)

    def get_api_connect(self):
        return self.api_connect

    def get_cluster(self):
        return self.cluster

    def get_api_auth(self):
        return self.api_connect.get_auth()

    def get_service_name(self):
        return self.service_name


    def disable_replication_schedule(self, schedule):
        ok = True
        if schedule:
            base_url = self.get_replication_base_url()
            auth = self.api_connect.get_auth()
            json_dict = schedule.to_json_dict()
            if not json_dict['paused']:
                json_dict['paused'] = True
                data = json.dumps(json_dict)
                url = base_url + str(schedule.id)
                ok = self.update_replication_schedule(url, data, auth=auth)
        return ok

    def enable_replication_schedule(self, schedule):
        ok = True
        if schedule:
            base_url = self.get_replication_base_url()
            auth = self.api_connect.get_auth()
            json_dict = schedule.to_json_dict()
            if json_dict['paused']:
                json_dict['paused'] = False
                data = json.dumps(json_dict)
                url = base_url + str(schedule.id)
                ok = self.update_replication_schedule(url, data, auth=auth)
        return ok


    def get_replication_base_url(self):
        # return 'http://s025wpll8881.s4.chp.cba:7180/api/v9/clusters/test-cluster/services/HDFS/replications/4'
        api_host = self.api_connect.get_api_host()
        api_port = self.api_connect.get_api_port()
        api_version = self.api_connect.get_api_version()

        api_version = 'v' + str(api_version)
        cluster_name = self.cluster.get_cluster_name()
        service_name = self.service_name
        url = ''.join(['http://', api_host, ':', str(api_port), '/api/', api_version, '/clusters/', cluster_name, '/services/', service_name, '/replications/'])
        return url

    def get_all_replication_schedules(self):
        return [r for r in self.service.get_replication_schedules()]

    def update_replication_schedule(self, url, data, auth):
        ok = True
        r = requests.put(url, data, auth=auth)
        if r.status_code != 200:
            print "Error|",
            print url,
            print r.status_code,
            print data
            ok = False
        return ok

############################    ENABLE/DISABLE    ##############################

    def enable_replication_schedule_by_id(self, ids):
        ok = True
        for rs in self.get_all_replication_schedules():
            if rs.id in ids:
                ok = self.enable_replication_schedule(rs)
                if not ok:
                    break
        return ok

    def disable_all_replication_schedules(self):
        ok = True
        for rs in self.get_all_replication_schedules():
            ok = self.disable_replication_schedule(rs)
            if not ok:
                break
        return ok

    def enable_all_replication_schedules(self):
        ok = True
        for rs in self.get_all_replication_schedules():
            ok = self.enable_replication_schedule(rs)
            if not ok:
                break
        return ok

    def disable_replication_schedule_by_id(self, ids):
        ok = True
        for rs in self.get_all_replication_schedules():
            if rs.id in ids:
                ok = self.disable_replication_schedule(rs)
                if not ok:
                    break
        return ok

############################    CREATE/DELETE    ###############################


    def create_replication_schedule(self, schedule):
        if not schedule:
            return None
        api = self.api_connect.get_api()
        arguments = None
        service_type = self.service.type
        arg_key = service_type.lower() + "Arguments"
        if service_type == 'HIVE':
            arguments = ApiHiveReplicationArguments(api).from_json_dict(schedule[arg_key], api)
        elif service_type == 'HDFS':
            arguments = ApiHdfsReplicationArguments(api).from_json_dict(schedule[arg_key], api)
        else:
            raise Exception("Unsupported service type : " + service_type)
        if arguments:
            # print type(arguments)
            rs = self.service.create_replication_schedule(schedule['startTime'],
                    None,
                    schedule['intervalUnit'],
                    schedule['interval'],
                    schedule['paused'],
                    arguments,
                    alert_on_start=True,
                    alert_on_success=True,
                    alert_on_fail=True,
                    alert_on_abort=True)
            return rs.id
        else:
            return None

    def create_replications_from_schedules(self, schedules):
        ok = True
        for s in schedules:
            ok = self.create_replication_schedule(s)
            if not ok:
                break
        return ok

    def delete_replication_schedule_by_id(ids):
        ok = True
        for rid in ids:
            x = self.service.delete_replication_schedule(rid)
            if x.id != rid:
                ok = False
                break
        return ok

    def delete_all_replication_schedules(self):
        ok = True
        for rs in self.get_all_replication_schedules():
            x = self.service.delete_replication_schedule(rs.id)
            if not x:
                ok = False
        return ok


###########################    BACKUP/RESTORE    ###############################

    def dump_replication_schedule(self, rs, backup_dir):
        try:
            repl_id = rs.id
            json_dict = rs.to_json_dict()
            with open(''.join([backup_dir, '/', str(repl_id), '.json']), 'w') as outf:
                json.dump(json_dict, outf)
            print "Backed up: " + str(repl_id)
            return True
        except Exception as e:
            print e
            return None


    def dump_all_replications(self, backup_dir):
        ok = None
        backed_up_repls = []
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        for rs in self.get_all_replication_schedules():
            ok = self.dump_replication_schedule(rs, backup_dir)
            if not ok:
                break
            backed_up_repls.append(rs.id)
        return backed_up_repls


    def dump_replication_schedule_by_id(self, backup_dir, ids):
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        for rs in self.get_all_replication_schedules():
            if rs.id in ids:
                dump_replication_schedule(rs, backup_dir)


    def restore_all_replications_from_dump(self, backup_dir):
        schedule_ids = []
        try:
            for f in listdir(backup_dir):
                if f.endswith(".json"):
                    print "Processing : " + f
                    data = None
                    with open('/'.join([backup_dir, f]), 'r') as inf:
                        data = json.load(inf)
                    new_id = self.create_replication_schedule(data)
                    if new_id:
                        schedule_ids.append(new_id)
                    else:
                        print "Unable to create a replication : ",
                        print data
            return schedule_ids
        except Exception as e:
            print "Exception occured in : ",
            print e
            return None

    def restore_replications_by_id(self, backup_dir, ids):
        try:
            for rid in ids:
                data = None
                with open(''.join([backup_dir, '/', str(rid), '.json']), 'r') as inf:
                    data = json.load(inf)
                new_id = self.create_replication_schedule(data)
                return new_id
        except Exception as e:
            print e
            return None
