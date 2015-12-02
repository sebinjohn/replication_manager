from src.schedules.schedules import *
from src.webapp.manager import *
from src.webapp.app import *

schedule = ReplicationSchedule('HIVE')
user_data = {
    'hdfs': {
        'source_path': 'test_source_path',
        'destination_path': 'test_dest_path'
    }
}

# print schedule.create_hdfs_arguments(user_data)
