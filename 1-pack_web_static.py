#!/usr/bin/python3
"""
Fabric script to generate a .tgz archive from web_static folder
"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from web_static folder
    """
    # Create the versions directory if it doesn't exist
    if not os.path.exists("versions"):
        os.makedirs("versions")

    # Create the archive filename
    time_format = "%Y%m%d%H%M%S"
    archive_name = "web_static_{}.tgz".format(
            datetime.now().strftime(time_format))

    # Generate the .tgz archive from web_static folder
    result = local("tar -czvf versions/{} web_static".format(archive_name))

    if result.failed:
        return None
    else:
        return "versions/{}".format(archive_name)
