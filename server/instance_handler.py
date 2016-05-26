import sys
import time
from oauth2client.client import GoogleCredentials
from googleapiclient.discovery import build
# [START list_instances]
def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items']
# [END list_instances]
# [START create_instance]
def create_instance(compute, project, zone, name):
    source_disk_image = \
        "projects/grand-reference-93404/zones/asia-east1-b/disks/node"
    machine_type = "zones/%s/machineTypes/n1-standard-1" % zone
    startup_script = open('startup-script.sh', 'r').read()
    image_url = "http://storage.googleapis.com/gce-demo-input/photo.jpg"
    image_caption = "Ready for dessert?"
    config = {
        'name': name,
        'machineType': machine_type,
        # Specify the boot disk and the image to use as a source.
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'source': source_disk_image,
            }
        ],

        # Specify a network interface with NAT to access the public
        # internet.
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],
        # Allow the instance to access cloud storage and logging.
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_write',
                'https://www.googleapis.com/auth/logging.write'
            ]
        }],
        # Metadata is readable from the instance and allows you to
        # pass configuration from deployment scripts to instances.
        'metadata': {
            'items': [{
                # Startup script is automatically executed by the
                # instance upon startup.
                'key': 'startup-script',
                'value': startup_script
            }, {
                'key': 'url',
                'value': image_url
            }, {
                'key': 'text',
                'value': image_caption
            }, {

                # Every project has a default Cloud Storage bucket that's
                # the same name as the project.
                'key': 'bucket',
                'value': project
            }]
        }
    }
    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()
# [END create_instance]
# [START delete_instance]
def delete_instance(compute, project, zone, name):
    return compute.instances().delete(
        project=project,
        zone=zone,
        instance=name).execute()
# [END delete_instance]
# [START wait_for_operation]

# [START wait_for_operation]
def wait_for_operation(compute, project, zone, operation):
    sys.stdout.write('Waiting for operation to finish')
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()
        if result['status'] == 'DONE':
            print "done."
            if 'error' in result:
                raise Exception(result['error'])
            return result
        else:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1)
# [END wait_for_operation]
