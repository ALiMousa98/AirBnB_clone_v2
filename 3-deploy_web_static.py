#!/usr/bin/python3
"""Fabric script that generates and distributes an archive to web servers"""

from fabric.api import local, env, put, run
from datetime import datetime
import os

env.hosts = ['<100.25.36.37', '54.166.10.168']


def do_pack():
    """Compresses web_static contents into a .tgz archive"""
    try:
        current_time = datetime.now()
        archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
            current_time.year, current_time.month, current_time.day,
            current_time.hour, current_time.minute, current_time.second)
        local("mkdir -p versions")
        local("tar -cvzf versions/{} web_static".format(archive_name))
        return "versions/{}".format(archive_name)
    except Exception:
        return None


def do_deploy(archive_path):
    """Deploys the archive to web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = archive_path.split("/")[-1]
        archive_base = archive_name.split(".")[0]

        put(archive_path, "/tmp/")
        run("mkdir -p /data/web_static/releases/{}/".format(archive_base))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(archive_name, archive_base))
        run("rm /tmp/{}".format(archive_name))
        run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(archive_base, archive_base))
        run("rm -rf /data/web_static/releases/{}/web_static".format(
            archive_base))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(archive_base))
        return True
    except Exception:
        return False


def deploy():
    """Creates and distributes an archive to web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
