#!/usr/bin/python

__author__ = 'Sebastien LANGOUREAUX'

from rancher_metadata import MetadataAPI
import re
import os

class ServiceRun():

    def run(self):

        # Get metadata to discovery worker
        metadata_manager = MetadataAPI()
        metadata_manager.wait_service_containers()

        # Workers must be link to me with the name worker
        linking_services = metadata_manager.get_service_links()

        service_name = None

        for linking_service in linking_services:
            search = re.search('([^/]+)/([^:])+:worker$', linking_service)
            if search:
                service_name = search.group(2)
                stack_name = search.group(1)

        if service_name is None:
            print("Standalone mode")
            return True


        # We get the list of containers in worker service
        containers = metadata_manager.get_service_containers(stack_name=stack_name, service_name=service_name)

        f = open(os.getenv('CITUS_WORKER_CONF_PATH') + '/pg_worker_list.conf', 'w')

        for container in containers:
            f.write("%s 5432\n" % container['primary_ip'])
            print("Add worker %s (%s) on Citus cluster" % (container['primary_ip'], container['name']))

        f.close()

