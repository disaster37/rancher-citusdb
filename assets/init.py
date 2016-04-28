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
        services = metadata_manager.get_stack_services()
        service =  metadata_manager.get_service()
        my_name = service['name']
        service_name = None
        stack_name = None


        # We search container that is in sidekick with me
        for service in services:
            for sidekick in service['sidekicks']:
                if sidekick == my_name:
                        # We search the worker service that must be linked with the master as name worker
                        for linking_service in service['links']:
                                if  service['links'][linking_service] == 'worker':
                                        search = re.search('^([^/]+)/([^/]+)$', linking_service)
                                        if search:
                                                service_name = search.group(2)
                                                stack_name = search.group(1)
                                                break

                        break



        if service_name is None:
            print("Standalone mode")
            return True


        # We get the list of containers in worker service
        containers = metadata_manager.get_service_containers(stack_name=stack_name, service_name=service_name)

        f = open(os.getenv('CITUS_WORKER_CONF_PATH') + '/pg_worker_list.conf', 'w')


        for name, container in containers.iteritems():
            f.write("%s 5432\n" % container['primary_ip'])
            print("Add worker %s (%s) on Citus cluster" % (container['primary_ip'], container['name']))

        f.close()

if __name__ == '__main__':

    serviceRun = ServiceRun()
    serviceRun.run()
