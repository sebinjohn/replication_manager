from flask import Flask, url_for, request
from pykwalify.core import Core
from replications.replications import *

class Config():
    def __init__(self):
        config = self.validate_config()
        self.configs = {}
        if config:
            for item in config:
                for k, v in item.iteritems():
                    self.configs[k] = v

            api = self.configs.get('api')
        else:
            raise Exception('Unable to load config files')
    @staticmethod
    def get_config():
        return 
    def get_api(self):
        if self.api_connect:
            return self.api_connect
        else:
            self.api_connect = ApiConnect(
                api.get('host'),
                api.get('port'),
                api.get('version'),
                (api.get('user'), api.get('pass')))

    def get_cluster(self):
        if self.cluster:
            return self.cluster
        self.cluster = OmniaCluster(
            self.configs.get('cluster').get('name'),
            self.get_api)

    def validate_config(self):
        try:
            c = Core(source_file="/Users/JohnS5/dev/replication_manager/src/webapp/bdr_app.yml",
                schema_files=['/Users/JohnS5/dev/replication_manager/src/webapp/schema.yml'])
            return c.validate(raise_exception=True)
        except Exception as e:
            print "LOG: ERROR: config file is not valid"
            print e
            return None
