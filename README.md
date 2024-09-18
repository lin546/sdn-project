# sdn-project
基于SDN的流量劫持系统

### 1、如何运行
* 导入sql文件，配置数据库
* 安装 Mininet、Ryu、Docker

```sh
docker pull iwaseyusuke/ryu-mininet
# 创建两个容器
docker run -it --rm --privileged -e DISPLAY \
						 -p 8080:8080 \
						 --name container1 \
             iwaseyusuke/ryu-mininet
```

* 配置 mininet、Ryu

```sh
docker exec -it container1 /bin/bash

ryu-manager ofctl_rest.py,simple_switch_rest.py

mn --controller=remote --topo=single,3
```

* 配置 vxlan 网络

```sh
1、分别在vm1和vm2中创建网络拓扑
mn --controller=remote --topo=single,3
2、分别在vm1和vm2中创建vxlan接口：
ovs-vsctl add-port s1 vxlan  
3、配置vm1和vm2中的vxlan接口：
sh ovs-vsctl set interface vxlan type=vxlan option:remote_ip=target_ip option:key=5566
4、设置vm1和vm2中的主机IP：
h1 ifconfig h1-eth0 target_ip
```



