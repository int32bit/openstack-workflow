# Openstack Sequence Diagrams

Draw Openstack operation sequence diagrams using[websequence diagrams tool](https://www.websequencediagrams.com/). An easiest way to track the workflow of Openstack. It may be useful for user to learn Openstack or problem troubleshooting. 

## Quick start

### 1. Remove old diagrams

If you need re-generate latest diagrams, Please cleanup the old diagrams first.

```
make clean
```

### 2. Generate new diagrams

To compile the diagrams on your localhost, ensure that your machine can access the Internet and the `make` tools hava been installed.

```
make
```

All diagrams generated will be put in `./output`, just use your image viewer to show.

## Demo

### 1. Create Server Workflow

![create server workflow](output/nova/create.png)

### 2. Reboot Server

 
![reboot server](output/nova/reboot.png)


## Need more diagrams ?

DYI, as you need!

## License 

MIT
