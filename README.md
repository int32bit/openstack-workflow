[👉English](./README.md)

## 1 关于该项目

### 1.1 谈谈Openstack的历史

OpenStack是一个面向IaaS层的云管理平台开源项目，用于实现公有云和私有云的部署及管理。最开始Openstack只有两个组件，分别为提供计算服务的Nova项目以及提供对象存储服务的Swift，其中Nova不仅提供虚拟机服务，还包含了网络服务、块存储服务、镜像服务以及裸机管理服务。之后随着项目的不断发展，从Nova中拆分成多个独立的项目提供不同的服务，如nova-volume拆分为Cinder项目提供块存储服务，nova-image拆分为Glance项目，提供镜像存储服务，nova-network则是neutron的前身，裸机管理也从Nova中分离出来为Ironic项目。最开始容器服务也是由Nova提供支持的，作为Nova的driver之一来实现，而后迁移到Heat，到现在已经分离成独立的项目Magnum，后来Magnum主要提供容器编排服务，单纯的容器服务由Zun项目负责。最开始Openstack并没有认证，从E版开始才加入认证服务Keystone，至此Openstack 6个核心服务才终于聚齐了。

* Keystone 认证服务。
* Glance 镜像服务。
* Nova 计算服务。
* Cinder 块存储服务。
* Neutorn 网络服务。
* Swift 对象存储服务。

E版之后，在这些核心服务之上，又不断涌现新的服务，如面板服务Horizon、服务编排服务Heat、数据库服务Trove、文件共享服务Manila、大数据服务Sahara以及前面提到的Magnum等，这些服务几乎都依赖于以上的核心服务。比如Sahara大数据服务会先调用Heat模板服务，Heat又会调用Nova创建虚拟机，调用Glance获取镜像，调用Cinder创建数据卷，调用Neutron创建网络等。

截至现在（2016年11月27日），Openstack已经走过了6年半的岁月，最新发布的版本为第14个版本，代号为Newton，Ocata版已经处在快速开发中。

Openstack不仅服务越来越多、越来越复杂，单个服务也越来越复杂，并且不断变化发展。以Nova为例，从开始的使用nova-conductor代理数据库访问增强安全性，引入objects对象模型来支持对象版本控制，现在正在开发Cell项目来支持大规模的集群部署以及将要分离的Nova-EC2项目，截至到现在Nova包含nova-api、nova-conductor、nova-scheduler、nova-compute、nova-cell、nova-console等十多个组件。这么庞大的分布式系统需要深刻理解其工作原理，理清它们的交互关系非常不容易，尤其对于新手来说。

## 1.2 Openstack源码阅读的正确姿势

由于Openstack使用python语言开发，而python是动态类型语言，参数类型不容易从代码中看出，因此首先需要部署一个allinone的Openstack开发测试环境，建议使用RDO部署：[Packstack quickstart](https://www.rdoproject.org/install/quickstart/)，当然乐于折腾使用devstack也是没有问题的。

其次需要安装科学的代码阅读工具，图形界面使用pycharm没有问题，不过通常在虚拟机中是没有图形界面的，首选vim，需要简单的配置使其支持代码跳转和代码搜索，可以参考[GitHub - int32bit/dotfiles: A set of vim, zsh, git, and tmux configuration files.](https://github.com/int32bit/dotfiles)。

学习Openstack的最佳步骤是:

* 看文档
* 部署allineone
* 使用
* 部署多节点
* 再次看文档
* 深度使用
* 阅读源码
* 参与社区开发

阅读源码的首要问题就是就要对代码的结构了然于胸，需要强调的是，Openstack项目的目录结构并不是根据组件严格划分的，而是根据功能划分的，以Nova为例，compute目录并不是一定在nova-compute节点上运行，而主要是和compute相关(虚拟机操作相关）的功能实现，同样的，scheduler目录代码并不全在scheduler服务节点运行，但主要是和调度相关的代码。好在目录结构并不是完全混乱的，它是有规律的。

通常一个服务的目录都会包含api.py、rpcapi.py、manager.py，这个三个是最重要的模块。

* api.py： 通常是供其它组件调用的库。换句话说，该模块通常并不会由本模块调用。比如compute目录的api.py，通常由nova-api服务的controller调用。
* rpcapi.py：这个是RPC请求的封装，或者说是RPC实现的client端，该模块封装了RPC请求调用。
* manager.py： 这个才是真正服务的功能实现，也是RPC的服务端，即处理RPC请求的入口，实现的方法通常和rpcapi实现的方法对应。

前面提到Openstack项目的目录结构是按照功能划分的，而不是服务组件，因此并不是所有的目录都能有对应的组件。仍以Nova为例:

* cmd：这是服务的启动脚本，即所有服务的main函数。看服务怎么初始化，就从这里开始。
* db: 封装数据库访问，目前支持的driver为sqlalchemy。
* conf：Nova的配置项声明都在这里。
* locale: 本地化处理。
* image: 封装Glance调用接口。
* network: 封装网络服务接口，根据配置不同，可能调用nova-network或者neutron。
* volume: 封装数据卷访问接口，通常是Cinder的client封装。
* virt: 这是所有支持的hypervisor驱动，主流的如libvirt、xen等。
* objects: 对象模型，封装了所有实体对象的CURD操作，相对以前直接调用db的model更安全，并且支持版本控制。
* policies： policy校验实现。
* tests: 单元测试和功能测试代码。

根据进程阅读源码并不是什么好的实践，因为光理解服务如何初始化、如何通信、如何发送心跳等就不容易，各种高级封装太复杂了。而我认为比较好的阅读源码方式是追踪一个任务的执行过程，比如看启动虚拟机的整个流程。而不管是任何操作，一定是先从API开始的，RESTFul API是Openstack服务的唯一入口，也就是说，阅读源码就从api开始。而api组件也是根据实体划分的，不同的实体对应不同的controller，比如servers、flavors、keypairs等，controller的index方法对应list操作、show方法对应get操作、create创建、delete删除、update更新等。

以创建虚拟机为例:

** S1 nova-api **

入口为nova/api/openstack/compute/servers.py的create方法，该方法检查了一堆参数以及policy后，调用`compute_api`的create方法，这里的`compute_api`即前面说的`nova/compute/api.py`模块的API。

`compute_api`会创建数据库记录、检查参数等，然后调用`compute_task_api`的`build_instances`方法，`compute_task_api`即conductor的api.py。

conductor的api并没有执行什么操作，直接调用了`conductor_compute_rpcapi`的`build_instances`方法，该方法即时conductor RPC调用api，即`nova/conductor/rpcapi.py`模块，该方法除了一堆的版本检查，剩下的就是对RPC调用的封装，代码只有两行:

```
cctxt = self.client.prepare(version=version)
cctxt.cast(context, 'build_instances', **kw)
```

其中cast表示异步调用，`build_instances`是远程调用的方法，`kw`是传递的参数。参数就是字典类型，没有复杂对象结构，因此不需要特别的序列化操作。

截至到现在，虽然目录由`api->compute->conductor`，但仍在nova-api进程中运行，直到cast方法执行，该方法由于是异步调用，因此nova-api进程结束。

** S2 nova-conductor **

由于是向nova-conductor发起的RPC调用，而前面说了接收端肯定是`manager.py`，因此进程跳到`nova-conductor`服务，入口为`nova/conductor/manager.py`的`build_instances`方法。

该方法首先调用了`_schedule_instances`方法，该方法调用了`scheduler_client`的`select_destinations`方法，`scheduler_client`和`compute_api`以及`compute_task_api`都是一样对服务的client调用，不过scheduler没有api.py，而是有个单独的client目录，实现在client目录的`__init__.py`目录，这里仅仅是调用query.py下的SchedulerQueryClient的`select_destinations`实现，然后又很直接的调用了`scheduler_rpcapi`的`select_destinations`方法，终于又到了RPC调用环节。

毫无疑问，RPC封装同样是在scheduler的rpcapi中实现。该方法RPC调用代码如下:

```
return cctxt.call(ctxt, 'select_destinations', **msg_args)
```

注意这里调用的call方法，即同步调用，此时nova-conductor并不会退出，而是堵塞等待直到nova-scheduler放回。

** S3 nova-scheduler **

同理找到scheduler的manager.py模块的`select_destinations`方法，该方法会调用driver的方法，这里的driver其实就是调度算法实现，通常用的比较多的就是`filter_scheduler`的，对应`filter_scheduler.py`模块，该模块首先通过`host_manager`拿到所有的计算节点信息，然后通过filters过滤掉不满足条件的计算节点，剩下的节点通过weigh方法计算权值，最后选择权值高的作为候选计算节点返回。nova-scheduler进程结束。

** S4 nova-condutor **

回到`scheduler/manager.py`的`build_instances`方法，nova-conductor等待nova-scheduler返回后，拿到调度的计算节点列表，然后调用了`compute_rpcapi`d的`build_and_run_instance`方法。看到xxxrpc立即想到对应的代码位置，位于`compute/rpcapi`模块，该方法向nova-compute发起RPC请求:

```
cctxt.cast(ctxt, 'build_and_run_instance', ...)
```

可见发起的是异步RPC，因此nova-conductor结束，紧接着终于该轮到nova-compute登场了。

** S5 nova-compute **

到了nova-compute服务，入口为compute/manager.py，找到`build_and_run_instance`方法，该方法调用了driver的spawn方法，这里的driver就是各种hypervisor的实现，所有实现的driver都在virt目录下，入口为`driver.py`，比如libvirt driver实现对应为`virt/libvirt/driver.py`，找到spawn方法，该方法拉取镜像创建根磁盘、生成xml文件、define domain，启动domain等。最后虚拟机完成创建。nova-compute服务结束。

以上是创建虚拟机的各个服务的交互过程以及调用关系，需要注意的是，所有的数据库操作，比如`instance.save（）`以及`update`操作，如果配置`use_local`为false，则会向nova-conductor发起RPC调用，由nova-conductor代理完成数据库更新，而不是由nova-compute直接访问数据库，这里的RPC调用过程在以上的分析中省略了。

### 1.3 关于此项目

本项目使用在线绘图工具[web sequencediagrams](https://www.websequencediagrams.com/)完成，目标是图形化Openstack的所有操作流程，通过操作序列图能快速学习Openstack的工作原理，理清各个组件的关系，运维人员也能根据操作序列图进行更精确的故障定位和排查.

注意，该操作序列图基于L版Openstack源码，未来版本的操作可能会有变化，请以最新版的源码为准，该项目提供的序列图仅供参考。

## 2 操作序列图

### 2.1 虚拟机操作列表

- [x] [boot](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/create.png)
- [x] [start](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/start.png)
- [x] [stop](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/stop.png)
- [x] [reboot](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/reboot.png)
- [x] [rebuild](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/rebuild.png)
- [x] [resize](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/resize.png)
- [x] [list](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/list.png)
- [x] [delete](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/delete.png)
- [x] [reset-state](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/reset_state.png)
- [x] [create-image(快照)](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/snapshot.png)
- [x] [set-password](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/changePassword.png)
- [x] [evacuate(疏散迁移)](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/evacuate.png)
- [x] [pause](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/pause.png)
- [x] [unpause](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/unpause.png)
- [x] [suspend](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/suspend.png)
- [x] [resume](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/resume.png)
- [x] [reset-network](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/reset_network.png)
- [x] [migrate(冷迁移)](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/migrate.png)
- [x] [live-migrate(在线迁移)](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/live_migrate.png)
- [x] [Shelve](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/shelve.png)
- [x] [Shelve-offload](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/shelve_offload.png)
- [x] [Unshelve](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/unshelve.png)
- [x] [lock](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/lock.png)
- [x] [unlock](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/unlock.png)
- [x] [backup](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/backup.png)
- [x] [Refresh Network](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/reset_network.png)
- [x] [rename/update](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/rename.png)
- [x] [rescue](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/rescue.png)
- [x] [unrescue](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/unrescue.png)
- [x] [volume-attach](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/volume_attach.png)
- [x] [volume-detach](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/volume-detach.png)
- [x] [interface-attach](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/interface-attach.png)
- [x] [interface-detach](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/nova/interface-detach.png)


### 2.2 Todo列表

- [ ] Cinder
- [ ] Neutron
- [ ] Sahara

    * - [x] [create(创建集群)](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/sahara/create_cluster.png)

![create cluster](https://raw.githubusercontent.com/int32bit/openstack-workflow/master/output/sahara/create_cluster.png)

- [ ] Magnum
- [ ] ...

## 3 如何工作


### 3.1 编译图形

生成最新图片需要连接外网并且依赖于Make工具，请确保所依赖的包已经安装。

直接执行make即可扫描所有的源码并自动生成操作序列图.

```
make
```

生成的图片默认会保存在`./output`路径下.

### 3.2 删除图片

执行以下命令可清理所有的图片:

```
make clean
```

### 3.3 操作流程案例分析

注意: 

* 图中蓝色线表示当前进程是active的，因此可以很容易看出是RPC同步调用还是异步调用的。
* Nova conductor配置use_local为false，访问数据库需要通过RPC调用conductor，但图中为了方便表示数据库操作，省略了RPC调用conductor访问数据库的过程。Nova已经使用objects模型封装了数据库操作,代码位于`nova/objects`目录。

#### 1. 创建虚拟机

![create server workflow](output/nova/create.png)

从操作序列图看，虚拟机的创建主要分为三步：第一步是nova api对用户创建虚拟机的参数进行检查，如果参数没有问题，nova api会在数据库中创建相应的表项用来记录用户的请求，然后给nova-conductor发起一个异步RPC调用，conductor会对调度时的filters spect进行初始化，并向nova-scheduler发起RPC同步调用，nova-scheduler收到nova conductor发来的请求之后筛选能够满足虚拟机资源需求的hypervisor，并按照一定的策略选取其中的一台hypervisor，返回给nova-conductor，conductor然后给候选的计算节点nova compute发起一个run_instance的RPC调用。 Nova compute收到run_instance的请求之后，会为虚拟机的运行分配各种资源，如：ip地址、磁盘、网络等。分配完各种资源之后，nova会调用libvirt创建根磁盘、xml文件等,并启动虚拟机。到此，虚拟机的创建基本上就结束了，等虚拟机启动完成，用户就可以登录和控制虚拟机了。

#### 2. 重启虚拟机

Nova中reboot操作可以分成两种：soft reboot和hard reboot。Soft reboot通过发送acpid或者guest agent信号给虚拟机,虚拟机接收到信号号主动执行重启操作。虚拟机必须支持appid或者运行qemu guest agent才能执行soft reboot。若soft reboot失败或者超时(默认120秒)，则会进入hard reboot。hard reboot将执行强制重启（相当于强制切电源），虚拟机重启的序列图如下：

![reboot server](output/nova/reboot.png)

从上图可以看出，soft reboot和hard reboot最主要的差别是libvirt所执行的操作不同，soft reboot关机时执行shutdown操作，而hard reboot执行destroy操作，可能导致正在运行的虚拟机异常关机导致数据丢失。

#### 3. 修改管理员密码

![change password](output/nova/changePassword.png)

从上图中看出，修改管理员密码是通过libvirt调用qemu guest agent执行的，因此虚拟机必须安装了qemu-guest-agent服务并且处于运行状态。

注意L版修改管理员密码只支持使用kvm/qemu hypervisor。

#### 4. 在线迁移

Live migrate是在不停止虚拟机的情况下，将虚拟机从一台宿主机上迁移到另外一台宿主机。在线迁移操作序列图如下：

![live migrage](output/nova/live_migrate.png)

在线迁移相对复杂，不过从图中看还是比较清晰的。如果不使用共享存储，传输虚拟机磁盘会花很长一段时间，导致虚拟机迁移很慢，因此建议使用统一共享分布式存储做Openstack存储后端。
在线迁移会不断的增量同步内存状态信息，直到收敛到很小的变化时，虚拟机会freeze一段时间，即处于downtime状态，完成最后的状态同步。迁移完成后，原来的虚拟机会自动删除。

#### 更多的操作序列图

所有的图形均使用工具生成，并且是可编程的。你只需要阅读源代码并使用[Websequence Diagrams Tool](https://www.websequencediagrams.com/)语法编写代码，语法请参考官方文档。以pause操作为例，对应源码为:

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

新增了源码后，只需要重新执行`make`命令即可生成新的图片。

## 4 贡献列表

以下这些开发者参与了该项目:

* AndiaQ: 喜爱研究Openstack的萌妹纸，她的博客: `https://andiaq.github.io`。
* int32bit: 从2013年开始折腾Openstack H版本，研究生期间曾在英特尔实习研究nova、ironic项目, 毕业后在UnitedStack负责cinder、nova开发和运维，现供职于云极星创，主要研究nova和容器相关技术。nova、cinder以及oslo的代码贡献者。
* ljjjustin: Openstack专家, 更多资料查看[他的博客](https://www.ljjjustin.xyz/about/)

感谢你们! (如果我遗忘了你的名字，请提醒我补充)。

## 附: Nova虚拟机操作列表

* boot: 创建虚拟机。
* delete: 删除虚拟机。
* force-delete: 无视虚拟机当前状态，强制删除虚拟机。即使开启了软删除功能，该操作也会立即清理虚拟机资源。
* list: 显示虚拟机列表。
* show: 查看指定虚拟机的详细信息。
* stop: 关机虚拟机。
* start: 开机虚拟机。
* reboot: 重启虚拟机。默认先尝试软重启，当软重启尝试120后失败，将执行强制重启。
* migrate: 冷迁移虚拟机，迁移过程中虚拟机将关机。
* live-migrate: 在线迁移虚拟机，虚拟机不会关机。
* resize: 修改虚拟机配置，即使用新的flavor重建虚拟机。
* rebuild: 重建虚拟机，指定新的image，如果指定快照，则相当于虚拟机状态回滚。
* evacuate: 疏散迁移，只有当compute服务down时执行，能够迁移虚拟机到其它正常计算节点中。
* reset-state: 手动重置虚拟机状态为error或者active。
* create-image: 创建虚拟机快照。
* backup: 定期创建虚拟机快照。
* volume-attach: 挂载volume卷。
* volume-detach: 卸载volume卷。
* lock/unlock: 锁定虚拟机，锁定后的虚拟机普通用户不能执行删除、关机等操作。
* set-password: 修改管理员密码，虚拟机需要运行qemu guest agent服务。
* pause/unpause: 暂停运行的虚拟机，如果底层的虚拟化使用的是libvirt，那么libvirt会在将虚拟机的信息保存到内存中，KVM/QEMU进程仍然在运行，只是暂停执行虚拟机的指令。
* suspend/resume: 挂起虚拟机，将虚拟机内存中的信息保存到磁盘上，虚拟机对于的KVM/QEMU进程会终止掉，该操作对应于libvirt中的save操作。resume从挂起的虚拟机恢复。
* reset-network: 重置虚拟机网络，在使用libvirt时，该操作不执行任何实际的动作，因此功能尚未实现。
* shelve/unshelve: 虚拟机关机后仍占用资源，如果虚拟机长期不使用，可以执行shelve操作，该操作先创建虚拟机快照，然后删除虚拟机，恢复时从快照中重建虚拟机。
* rename: 重命名虚拟机, 后期版本将被update操作替代。
* update: 修改虚拟机名称、description信息等。
* rescue/unrescue: 虚拟机进入拯救模式。原理是创建一台新的虚拟机，并把需要rescue的虚拟机的根磁盘作为第二块硬盘挂载到新创建的虚拟机。当原虚拟机根磁盘破坏不能启动时该操作非常有用。
* interface-attach/interface-dettach: 绑定/解绑网卡。
* trigger-crash-dump: 使虚拟机触发crash dump错误，测试使用。
* resize-confirm: 确认resize操作，此时原来的虚拟机将被删除, 可以配置为自动确认。
* resize-revert: 撤销resize操作，新创建的虚拟机删除，并使用原来的虚拟机。
* console-log: 查看虚拟机日志。
* get-vnc-console: 获取虚拟机vnc地址, 通常使用novnc协议。
* restore: 恢复虚拟机。如果配置了软删除功能，当虚拟机被删除时，不会立即删除，而仅仅标识下，此时能够使用restore操作恢复删除的虚拟机。
* instance-action-list: 查看虚拟机的操作日志。
* instance-action：查看某个虚拟机操作的详细信息，如操作用户、操作时间等。

## 5 协议

MIT

## 6 如何贡献

欢迎有兴趣的读者补充更多的操作序列图或者参与讨论。

* 如果你有任何问题，请直接创建issure。
* 如果你要贡献代码，请直接PR。

## 更多项目

* [dotfiles](https://github.com/int32bit/dotfiles): vim、tmux、zsh、iterm配置，阅读Openstack源码必备，vim支持标签列表、函数跳转、代码搜索、智能补全功能。
* [openstack-cheat-sheet](https://github.com/int32bit/openstack-cheat-sheet): 汇集所有Openstack相关的资料。
* [int32bit's blog](http://int32bit.me/): int32bit的博客，主要专注于Openstack、Docker、Ceph相关。

**--by int32bit(nova、cinder、oslo contributor).**
