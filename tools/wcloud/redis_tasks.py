import os
import unittest
import StringIO
import celery
from redis.exceptions import ConnectionError
import redis


class AlreadyDeployedException(Exception):
    """
    Thrown when an attempt to deploy REDIS is done, but the specified instance
    is already deployed.
    """
    def __init__(self):
        self.msg = "REDIS instance is apparently already deployed (the config file exists already)."


@celery.task
def deploy_redis_instance(redis_env_folder, port):
    """
    Deploys a new redis instance in the specified folder. A redis instance will be able to serve
    16 different databases. An instance is linked to a port. The folder should exist.

    Remarks: A redis conf file will be created in the folder, whose name will depend on the port chosen.
    A redis instance for the same port cannot be deployed on the same folder.

    This task will not check whether the redis instance is deployed properly. That will be done
    in a different task.

    As of now it is not possible to customize the Redis config files. If that feature is ever needed
    it could be easily added in the future.


    @param redis_env_folder: Folder on which to create the redis conf files that will define the instance,
    and that eventually will be used to start the same instance easily.
    @param port: Port under which the new Redis instance will listen.

    @return: True if the instance is supposedly deployed successfully. An exception is otherwise thrown.
    """

    # Ensure that the specified folder exists already.
    if not os.path.isdir(redis_env_folder):
        raise Exception(
            "The specified folder (%s) does not exist. We cannot deploy the Redis instance." % redis_env_folder)

    # Generate the config file.
    conf = StringIO.StringIO()
    conf.write("port %d \n" % port)
    conf.write("daemonize yes \n")
    conf.write("logfile redis_%d_logfile.txt \n" % port)

    config_file_name = "redis_%d.conf" % port

    # Make sure the config file doesn't exist already.
    if os.path.exists(os.path.join(redis_env_folder, config_file_name)):
        raise AlreadyDeployedException()

    # Write it to disk.
    f = file(os.path.join(redis_env_folder, config_file_name), "w")
    f.write(conf.getvalue())
    f.close()

    return True


@celery.task
def check_redis_deployment(redis_env_folder, port):
    """
    Verifies that a Redis instance has been deployed properly by doing a PING against the server.
    If the instance hasn't been started already then this method will start it itself and will
    close it once the verification is done.

    @param redis_env_folder: Folder where the Redis config files are stored.
    @param port: Port under which the redis instance deployment to verify is running or is supposed to run.

    @return True if the check passes. Otherwise an exception is thrown.
    """

    started_by_us = False

    # Find out whether it's running.
    try:
        r = redis.StrictRedis(host="127.0.0.1", port=port, db=0)
        r.ping()
    except ConnectionError:
        # The server seems to be down, we start it.
        os.system("redis-server %s" % os.path.join(redis_env_folder, "redis_%d.conf" % port))
        started_by_us = True

    r = redis.StrictRedis(host="127.0.0.1", port=port, db=0)
    r.ping()

    if started_by_us:
        r.shutdown()

    return True





######################################
#
# UNIT TESTS BELOW
#
######################################

from nose.tools import assert_is_not_none


class TestDatabaseTasks(unittest.TestCase):
    def test_deploy_redis_instance(self):
        deploy_redis_instance("redis_env", 15000)
        assert os.path.exists("redis_env/redis_15000.conf")

    def test_check_redis_instance(self):
        deploy_redis_instance("redis_env", 15000)
        check_redis_deployment("redis_env", 15000)

    def _clearTestDatabases(self):
        pass

    def setUp(self):
        try:
            os.remove("redis_env/redis_15000.conf")
        except:
            pass

    def tearDown(self):
        try:
            os.remove("redis_env/redis_15000.conf")
        except:
            pass


