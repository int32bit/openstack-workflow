# Openstack操作系列图

Draw Openstack operation sequence diagrams using[websequence diagrams tool](https://www.websequencediagrams.com/). An easy way to learn of the workflow of Openstack. It may be useful for user to learn Openstack or problem troubleshooting. 

## Quick start

### 1. Remove old diagrams

If you need re-generate latest diagrams, Please remove old one first.

```
make clean
```

### 2. Generate new diagrams


```
make
```

All diagrams generated will be put in `./output`, use your image viewer to show them.

## Demo

### 1. Create Server Workflow

![create server workflow](output/nova/create.png)

### 2. Reboot Server

 
![create server workflow](output/nova/reboot.png)


## How to add new diagrams

 
