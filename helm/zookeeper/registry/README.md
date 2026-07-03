# ZooKeeper Runtime Image

This directory builds the Apache ZooKeeper 3.7.2 runtime image used by the Helm chart.

```bash
cd /Users/shoufengxia/Desktop/Code/templates/helm/zookeeper/registry
REGISTRY=crpi-wsxiy5y9ovijxdks.cn-hangzhou.personal.cr.aliyuncs.com/jockey ./build-zookeeper-image.sh
```

The image is built from:

```text
crpi-wsxiy5y9ovijxdks.cn-hangzhou.personal.cr.aliyuncs.com/jockey/sealos:base-dragonwell8-python3
```
