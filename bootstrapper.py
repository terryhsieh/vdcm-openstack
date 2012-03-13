from task_worker import task, task_class
from task_worker import WorkerTask
from shutil import copytree,rmtree,ignore_patterns
import commands
import json
import time
import logging
import sys
import os


deploy_meta = {
"purpose": "deploy",

"name": "Openstack Diablo with dashboard and keystone",
"base_os": ["Ubuntu 11.04 x64"],
"min_host": 1,
"max_host": 100,

"user_config":{

	"admin_password": {
	"description": "The Admin Password",
	"type": "text",
	"max": 20,
	"min": 3,
	"required": True,
	"default": "delta",
	"order": 0
	},
	"mysql_root_password": {
	"description": "Mysql Root Password",
	"type": "text",
	"max": 20,
	"min": 3,
	"required": True,
	"default": "deltacloud",
	"order": 1
	},
	"mysql_nova_password": {
        "description": "Mysql nova Password",
        "type": "text",
        "max": 20,
        "min": 3,
        "required": True,
        "default": "deltacloud",
        "order": 2
        },
	"mysql_glance_password": {
        "description": "Mysql glance Password",
        "type": "text",
        "max": 20,
        "min": 3,
        "required": True,
        "default": "deltacloud",
        "order": 3
        },
	"mysql_keystone_password": {
        "description": "Mysql keystone Password",
        "type": "text",
        "max": 20,
        "min": 3,
        "required": True,
        "default": "deltacloud",
        "order": 4
        },
	"mysql_horizon_password": {
        "description": "Mysql horizon Password",
        "type": "text",
        "max": 20,
        "min": 3,
        "required": True,
        "default": "deltacloud",
        "order": 5
        },
	"service_token": {
        "description": "Service default token",
        "type": "text",
        "max": 20,
        "min": 3,
        "required": True,
        "default": "111222333444555666",
        "order": 6
        },
	"network_type": {
	"description": "Network Type",
	"type": "radio",
	"required": True,
	"value": ["nova.network.manager.FlatManager", "nova.network.manager.FlatDHCPManager", "nova.network.manager.VlanManager"],
	"default": "nova.network.manager.VlanManager",
	"order": 7
	},
	"libvirt_type": {
	"description": "The Virtualization Type",
	"type": "text",
	"max": 15,
	"min": 3,
	"required": True,
	"default": "qemu",
	"order": 8
	},
	"public_interface": {
        "description": "Public Interface",
        "type": "text",
        "max": 15,
        "min": 3,
        "required": True,
        "default": "eth0",
        "order": 9
        },
	"vlan_interface": {
        "description": "Vlan Interface",
        "type": "text",
        "max": 15,
        "min": 3,
        "required": True,
        "default": "eth1",
        "order": 10
        },

	"fixed_range_net": {
        "description": "Fixed range network",
        "type": "text",
        "max": 50,
        "min": 3,
        "required": True,
        "default": "172.16.0.0",
        "order": 11
        },
	"fixed_range_bits": {
        "description": "Fixed range bits",
        "type": "text",
        "max": 50,
        "min": 1,
        "required": True,
        "default": "12",
        "order": 12
        },
	"fixed_range_mask": {
        "description": "Fixed range mask",
        "type": "text",
        "max": 50,
        "min": 1,
        "required": True,
        "default": "255.240.0.0",
        "order": 13
        },

	"fixed_range_network_size": {
        "description": "Fixed range network size",
        "type": "text",
        "max": 50,
        "min": 1,
        "required": True,
        "default": "256",
        "order": 14
        },
	"fixed_range_network_count": {
        "description": "Fixed range network count",
        "type": "text",
        "max": 50,
        "min": 1,
        "required": True,
        "default": "16",
        "order": 15
        },
	"floating_range": {
        "description": "Floating range",
        "type": "text",
        "max": 50,
        "min": 8,
        "required": True,
        "default": "192.168.11.128/25",
        "order": 16
        },
	"region": {
        "description": "VDCM region name",
        "type": "text",
        "max": 50,
        "min": 3,
        "required": True,
        "default": "nova",
        "order": 17
        },



}
}

@task_class
class TestMeta(WorkerTask):
    meta = deploy_meta

    def run(self, deploy_json):
        # this is where function call starts
        # a test function, update 10% progess every 30s
        progress = 0
        deploy_data = json.loads(deploy_json)
	DeployDirectory = os.getcwd()+"/workers/openstack-setup/"

	settings=open(DeployDirectory+'settings','w')
	settings.write('HOST_IP="'+deploy_data["deploy_hosts"][0]+'"\n')
	settings.write('MYSQL_HOST="'+deploy_data["deploy_hosts"][0]+'"\n')
	settings.write('ADMIN_PASSWORD="'+deploy_data["admin_password"]+'"\n')
	settings.write('MYSQL_ROOT_PASS="'+deploy_data["mysql_root_password"]+'"\n')
	settings.write('MYSQL_NOVA_PASS="'+deploy_data["mysql_nova_password"]+'"\n')
	settings.write('MYSQL_GLANCE_PASS="'+deploy_data["mysql_glance_password"]+'"\n')
	settings.write('MYSQL_KEYSTONE_PASS="'+deploy_data["mysql_keystone_password"]+'"\n')
	settings.write('MYSQL_HORIZON_PASS="'+deploy_data["mysql_horizon_password"]+'"\n')
	settings.write('SERVICE_TOKEN="'+deploy_data['service_token']+'"\n')
	settings.write('NETWORK_TYPE="'+deploy_data['network_type']+'"\n')
	settings.write('PUBLIC_INTERFACE="'+deploy_data['public_interface']+'"\n')
	settings.write('VLAN_INTERFACE="'+deploy_data['vlan_interface']+'"\n')
	settings.write('FIXED_RANGE_NET="'+deploy_data['fixed_range_net']+'"\n')
	settings.write('FIXED_RANGE_BITS="'+deploy_data['fixed_range_bits']+'"\n')
	settings.write('FIXED_RANGE_MASK="'+deploy_data['fixed_range_mask']+'"\n')
	settings.write('FIXED_RANGE_NETWORK_SIZE="'+deploy_data['fixed_range_network_size']+'"\n')
	settings.write('FIXED_RANGE_NETWORK_COUNT="'+deploy_data['fixed_range_network_count']+'"\n')
	settings.write('FLOATING_RANGE="'+deploy_data['floating_range']+'"\n')
	settings.write('REGION="'+deploy_data['region']+'"\n')
	
	settings_common = \
"""
LIBVIRT_TYPE=${LIBVIRT_TYPE:-kvm}

if [[ "$LIBVIRT_TYPE" == "kvm" ]]; then
    modprobe kvm || true
    if [ ! -e /dev/kvm ]; then
	LIBVIRT_TYPE=qemu
    fi
fi
	
FIXED_RANGE="${FIXED_RANGE_NET}/${FIXED_RANGE_BITS}"
export NOVA_PROJECT_ID="admin"
export NOVA_USERNAME="admin"
export NOVA_API_KEY=$ADMIN_PASSWORD
export NOVA_URL="http://$HOST_IP:5000/v2.0/"
export NOVA_VERSION=1.1
export NOVA_REGION_NAME=$REGION
"""
	settings_apt = \
"""
DIR_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
mv /etc/apt/sources.list /etc/apt/sources.list.ori
echo 'deb file:'$DIR_PATH'/debs ./' > /etc/apt/sources.list
"""

	settings_myip = \
"""
IP=`ifconfig $PUBLIC_INTERFACE | grep 'inet addr:' | cut -d: -f2 | awk '{print $1}'`
cat "--my_ip=$IP" >> /etc/nova/nova.conf 
"""

	settings.write(settings_common)
	settings.write(settings_apt)
	settings.close()

        while progress < 100:
            zone_deploy.update_progress(progress, 'working on deploying')
            time.sleep(1)
    
	    deploy_hosts = {}

	    for host in deploy_data['deploy_hosts']:
		interval=len(deploy_data['deploy_hosts'])
		if host == deploy_data['deploy_hosts'][0]:
		    print 'controller node: '+host
		    source=DeployDirectory
		    destination='/mnt2/hostdata/'+host+'/openstack-setup'
		    rmtree(destination,ignore_errors=True)
		    print 'copy deploy file to '+host
		    copytree(source, destination)
		    print 'copy deploy file to '+host+' complete'

		    command_prefix = 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no '
		    command_host = host
		    command_run = ' \" cd /mnt2/openstack-setup; ./all-in-one.sh > deploy.log\"'
		    run_command = command_prefix+command_host+command_run
		    print 'running command: '+run_command
		    commands.getstatusoutput(run_command)
	
		    deploy_hosts[host] = 'controller'
		else:
		    print 'compute node:'+host
		    source=DeployDirectory
		    destination='/mnt2/hostdata/'+host+'/openstack-setup'
		    rmtree(destination,ignore_errors=True)
		    print 'copy deploy file to '+host
		    copytree(source, destination)
		    print 'copy deploy file to '+host+' complete'
		    deploy_hosts[host] = 'compute'

		progress = progress + (100/interval)
		zone_deploy.update_progress(progress, 'working on deploying')

	    zone_deploy.update_progress(100, 'deployment done!', data='success')

	deploy_result = {
	    'deploy_hosts': deploy_hosts,
	    'dashboard_url': 'http://192.168.11.6/'
	}
	result = {
	    'result': True,
	    'msg': 'Deployment Complete',
	    'data': deploy_result
	}
	return result


@task
def zone_deploy(deploy_json):
    '''
    do the installation, bootstrap stuff here
    '''
    print 'installing server'
    print deploy_json

    countdown = 0
    print 'worker id', zone_deploy.task_info.worker_id
    print 'task id', zone_deploy.task_info.task_id
    while countdown < 2:
        time.sleep(1)
        countdown += 1
        zone_deploy.update_progress(countdown * 10, 'working hard...')
    zone_deploy.update_progress(100, 'zone_deploy done!!!')
    return 'success'

