# Openstack Sequence Diagrams

Draw Openstack operation sequence diagrams using [Websequence Diagrams Tool](https://www.websequencediagrams.com/). An easiest way to track the workflow of Openstack and can be useful for user to learn Openstack or administer to problem troubleshooting. 

## Action List

### 1. Virtual Machine Manager

- [x] [Boot](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/create.png)
- [x] [Start](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/start.png)
- [x] [Stop](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/stop.png)
- [x] [Reboot](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/reboot.png)
- [x] [Rebuild](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/rebuild.png)
- [x] [Resize](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/resize.png)
- [x] [List](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/list.png)
- [x] [Delete](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/delete.png)
- [x] [Reset State](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/reset_state.png)
- [x] [Create Image](Snapshot)(https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/snapshot.png)
- [x] [Change Admin Password](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/changePassword.png)
- [x] [Evacuate](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/evacuate.png)
- [x] [Pause](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/pause.png)
- [x] [Unpause](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/unpause.png)
- [x] [Suspend](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/suspend.png)
- [x] [Reset Network](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/reset_network.png)
- [ ] Cold Migrate
- [ ] Live Miagrate
- [ ] Shelve
- [ ] Shelve-offload
- [ ] Lock
- [ ] Unlock
- [ ] Backup
- [ ] Meta
- [ ] Refresh Network
- [ ] Rename
- [ ] Rescue
- [ ] volume Attach
- [ ] Volume Detach
- [ ] Interface Attach
- [ ] Interface Detach


### 2. Todo

- [ ] Cinder
- [ ] Neutron
- [ ] Sahara
- [ ] Magnum
- [ ] ...

## Quick Start


### 1. Generate diagrams

To compile the diagrams on your localhost, ensure that your machine can access the Internet and the `make` tools hava been correctly installed.

```
make
```

All diagrams generated will be put in `./output` by default, use your image viewer to show.

### 2. Remove diagrams

To cleanup the diagrams, just run this:

```
make clean
```


## Some demo

### 1. Create Server Workflow

![create server workflow](output/nova/create.png)

### 2. Reboot Server

 
![reboot server](output/nova/reboot.png)

### 3. Stop Server

![stop server](output/nova/stop.png)

### 4. Rebuild Server

![rebuild server](output/nova/rebuild.png)


## Need more diagrams ?

DYI, as you need!

For example:

```
title pause a server

participant client
participant nova_api

client->nova_api: pause
activate client
activate nova_api

# nova/api/openstack/compute/pause_server.py _pause()
note over nova_api: authrize context
nova_api->database: get instance by uuid
database->nova_api: done

# nova/compute/api.py pause()
note over nova_api: check policy
note over nova_api: check instance lock
note over nova_api: check instance cell
note over nova_api: ensure instance state is ACTIVE
nova_api->database: task_state = PAUSING
database->nova_api: done

note over nova_api: record pause action
# nova/compute/rpcapi.py pause_instance()
nova_api->nova_compute: pause_instance
deactivate nova_api
deactivate client
activate nova_compute

# nova/compute/manager.py pause_instance()
note over nova_compute: notify: pause.start
nova_compute->libvirt: pause
activate libvirt

# nova/virt/libvirt/driver.py pause()
note over libvirt: get domain
note over libvirt: domain.suspend()
libvirt->nova_compute: done
deactivate libvirt
# nova/compute/manager.py pause_instance()
nova_compute->database: vm_state = vm_states.PAUSED\ntask_state = None
database->nova_compute: done
note over nova_compute: notify: pause.end
deactivate nova_compute
```

## License 

MIT
