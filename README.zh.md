[👉English](./README.md)

# Openstack 操作序列图

本项目使用[Websequence Diagrams Tool](https://www.websequencediagrams.com/)绘制Openstack操作序列图. 通过操作序列图能够快速追踪Openstack源代码，对初学者学习Openstack源码很有帮助，也 An easiest way to track the source of Openstack and can be useful for user to learn Openstack or administer to problem troubleshooting. Noted that all these works are based on Openstack Liberty version, it may be changed in the future version, be careful to use if your Openstack version is not Liberty.

## 操作列表

### 1. 虚拟机管理

- [x] [启动虚拟机](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/create.png)
- [x] [开机](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/start.png)
- [x] [关机](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/stop.png)
- [x] [重启](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/reboot.png)
- [x] [重建](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/rebuild.png)
- [x] [扩容(修改Flavor配置)](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/resize.png)
- [x] [打印虚拟机列表](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/list.png)
- [x] [删除虚拟机](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/delete.png)
- [x] [重置状态](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/reset_state.png)
- [x] [创建快照](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/snapshot.png)
- [x] [修改管理员密码](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/changePassword.png)
- [x] [疏散迁移](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/evacuate.png)
- [x] [停止虚拟机](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/pause.png)
- [x] [从pause的虚拟机恢复](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/unpause.png)
- [x] [挂起虚拟机](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/suspend.png)
- [x] [恢复虚拟机](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/resume.png)
- [x] [重置网络](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/reset_network.png)
- [x] [冷迁移](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/migrate.png)
- [x] [在线迁移](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/live_migrate.png)
- [x] [Shelve](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/shelve.png)
- [x] [Shelve-offload](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/shelve_offload.png)
- [x] [Unshelve](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/unshelve.png)
- [x] [锁定虚拟机](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/lock.png)
- [x] [解锁虚拟机](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/unlock.png)
- [x] [定时备份虚拟机](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/backup.png)
- [x] [Refresh Network](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/reset_network.png)
- [x] [重命名虚拟机](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/rename.png)
- [x] [拯救模式](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/rescue.png)
- [x] [Unrescue](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/unrescue.png)
- [x] [挂载volume](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/volume_attach.png)
- [x] [卸载volume](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/volume-detach.png)
- [x] [挂载网卡](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/interface-attach.png)
- [x] [卸载网卡](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/interface-detach.png)


### 2. Todo列表

- [ ] Cinder
- [ ] Neutron
- [ ] Sahara

    * - [x] [创建集群](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/sahara/create_cluster.png)

![create cluster](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/sahara/create_cluster.png)

- [ ] Magnum
- [ ] ...

## 快速开始


### 1. 生成图片

Before generate the diagrams on your localhost, ensure your machine can access the Internet and the `make` tools hava been correctly installed.

```
make
```

生成的图片默认保存在`./output`路径下.

### 2. 清除图片

执行以下命令删除生成的图片

```
make clean
```


## Demo实例

### 1. 创建虚拟机

![create server workflow](output/nova/create.png)

### 2. 重启虚拟机

 
![reboot server](output/nova/reboot.png)

### 3. 关机虚拟机

![stop server](output/nova/stop.png)

### 4. 重建虚拟机

![rebuild server](output/nova/rebuild.png)


## 需要更多的操作序列图?

阅读源代码并使用[Websequence Diagrams Tool](https://www.websequencediagrams.com/)语法编写脚本，比如:

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

## 贡献列表

以下这些人参与了该项目开发:

* AndiaQ
* int32bit
* ljjjustin

感谢你们! (如果我遗忘了你的名字，请让我知道)

## 协议

MIT
