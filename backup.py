import argparse
import datetime
from subprocess import call

parser = argparse.ArgumentParser()
parser.add_argument('--db-type', '-t', required=True, help='The type of the database to be backuped')
parser.add_argument('--db-name', '-n', required=True, help='The name of the database to be backuped')
parser.add_argument('--db-user', '-u', required=True, help='The user of the database to be backuped')
parser.add_argument('--media-path', '-m', required=False, help='The path to the media files')
parser.add_argument('--local-path', '-l', required=True, help='The local path for the backup')
parser.add_argument('--remote-path', '-r', required=True, help='The remote path for the backup')
args = parser.parse_args()
my_args = vars(args)

date = datetime.datetime.now().strftime("%Y%m%d")

if my_args["db_type"] == "postgres":
    # Create local path directory
    call("mkdir -p {}".format(my_args["local_path"]), shell=True)

    # Dump DB
    call("pg_dump -U {} -d {} | gzip > {}{}.{}.sql.gz".format(
        my_args["db_user"],
        my_args["db_name"],
        my_args["local_path"],
        date,
        my_args["db_name"],
    ), shell=True)

    # Copy DB to remote path
    call("scp {}{}.{}.sql.gz {}".format(
        my_args["local_path"],
        date,
        my_args["db_name"],
        my_args["remote_path"],
    ), shell=True)

# Pack media data
call("tar czf {}{}.media.tar.gz -C {} .".format(
    my_args["local_path"],
    date,
    my_args["media_path"],
), shell=True)


# Copy media data to remote path
call("scp {}{}.media.tar.gz {}".format(
    my_args["local_path"],
    date,
    my_args["remote_path"]
), shell=True)

# Delete older files
call("find %s -mtime +7 -exec rm {} \;" % my_args["local_path"], shell=True)
