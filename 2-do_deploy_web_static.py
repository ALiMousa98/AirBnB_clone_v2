#!/usr/bin/python3
"""
Fabric script to deploy an archive to web servers
"""


from fabric.api import env, put, run
from os.path import exists

env.hosts = ['100.25.36.37', '54.166.10.168']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/authorized_keys'


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, "/tmp/")

        # Get the archive filename without extension
        archive_name = archive_path.split("/")[-1]
        archive_base = archive_name.split(".")[0]

        # Create the target directory for the deployment
        run("mkdir -p /data/web_static/releases/{}/".format(archive_base))

        # Uncompress the archive to the target directory
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
            archive_name, archive_base))

        # Remove the uploaded archive from /tmp/
        run("rm /tmp/{}".format(archive_name))

        # Delete the old symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the deployed code
        run("ln -s /data/web_static/releases/{}/ "
            "/data/web_static/current".format(archive_base))

        return True

    except Exception as e:
        return False
