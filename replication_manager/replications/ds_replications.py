from replications import *
import sys
from argparse import ArgumentParser

parser = ArgumentParser(description='DS BDR Client')
def parse_args(sys_args):
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--backup-all-replications', action='store_true')
    parser.add_argument('--to-dir', nargs=1)

    group.add_argument('--disable-all-replications', action='store_true')
    group.add_argument('--enable-all-replications', action='store_true')
    group.add_argument('--delete-all-replications', action='store_true')

    group.add_argument('--restore-all-replications', action='store_true')
    parser.add_argument('--from-dir', nargs=1)

    parser.add_argument('--service-name', nargs=1, required=True)
    parser.add_argument('--cluster-name', nargs=1, required=True)

    parser.add_argument('--api-host', nargs=1, required=True)
    parser.add_argument('--api-port', default=7180, type=int)
    parser.add_argument('--api-version', default=9, type=int)
    parser.add_argument('--api-user', nargs=1, default='admin')
    parser.add_argument('--api-pass', nargs=1, default='admin')
    return parser.parse_args()

def main(sys_args):
    args = parse_args(sys_args)
    service_name = args.service_name[0]
    cluster_name = args.cluster_name[0]
    api_host = args.api_host[0]
    api_user = args.api_user[0]
    api_pass = args.api_pass[0]
    api_port = args.api_port
    api_version = args.api_version
    auth = (api_user, api_pass)
    api_connect = ApiConnect(api_host, api_port, api_version, auth)
    cluster = OmniaCluster(cluster_name, api_connect)
    service_repl = BDR_Replications(api_connect, cluster, service_name)

    if args.backup_all_replications:
        if args.to_dir:
            backup_dir = args.to_dir[0]
            print service_repl.dump_all_replications(backup_dir)
        else:
            parser.print_usage()
            print "Missing --to-dir argument"
            return None
    elif args.disable_all_replications:
        print service_repl.disable_all_replication_schedules()
    elif args.enable_all_replications:
        print service_repl.enable_all_replication_schedules()
    elif args.delete_all_replications:
        print service_repl.delete_all_replication_schedules()
    elif args.restore_all_replications:
        if args.from_dir:
            backup_dir = args.from_dir[0]
            result = service_repl.restore_all_replications_from_dump(backup_dir)
            print "Restored " + str(len(result)) + " replications. Ids given below",
            print result
        else:
            parser.print_usage()
            print "Missing --from-dir argument"
            return None
    else:
        print parser.print_help()
        sys.exit(1)

if __name__  == '__main__':
    main(sys.argv[1:])
