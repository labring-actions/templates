# HDFS Runtime Image

The Helm chart expects this runtime image by default:

```text
crpi-wsxiy5y9ovijxdks.cn-hangzhou.personal.cr.aliyuncs.com/jockey/sealos:hdfs-3.3.6
```

The image must include Apache Hadoop 3.3.6 under `/opt/hadoop`, Java under `/opt/java`, plus `bash` and `python3`.

This chart does not build the runtime image automatically. The `registry/` directory is kept so Sealos can package registry metadata when building the cluster image.
