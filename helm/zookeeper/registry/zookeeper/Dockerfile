ARG BASE_IMAGE=crpi-wsxiy5y9ovijxdks.cn-hangzhou.personal.cr.aliyuncs.com/jockey/sealos:base-dragonwell8-python3
ARG ZOOKEEPER_VERSION=3.7.2

FROM alpine:3.20 AS zookeeper

ARG ZOOKEEPER_VERSION

RUN set -eux; \
    wget -O /tmp/zookeeper.tar.gz "https://archive.apache.org/dist/zookeeper/zookeeper-${ZOOKEEPER_VERSION}/apache-zookeeper-${ZOOKEEPER_VERSION}-bin.tar.gz"; \
    mkdir -p /zookeeper; \
    tar -xzf /tmp/zookeeper.tar.gz -C /zookeeper --strip-components=1; \
    rm -f /tmp/zookeeper.tar.gz

FROM ${BASE_IMAGE}

ARG ZOOKEEPER_VERSION

ENV ZOOKEEPER_HOME=/opt/zookeeper \
    ZOO_LOG_DIR=/var/lib/zookeeper/logs \
    PATH=/opt/zookeeper/bin:${PATH} \
    TZ=Asia/Shanghai

COPY --from=zookeeper /zookeeper/ /opt/zookeeper/

RUN set -eux; \
    detected_java_home="$(dirname "$(dirname "$(readlink -f "$(command -v java)")")")"; \
    ln -sfn "${detected_java_home}" /opt/java; \
    mkdir -p /var/lib/zookeeper/data /var/lib/zookeeper/data-log /var/lib/zookeeper/logs; \
    chmod -R 0775 /opt/zookeeper /var/lib/zookeeper

ENV JAVA_HOME=/opt/java

WORKDIR /opt/zookeeper

EXPOSE 2181 2888 3888 8080

CMD ["/opt/zookeeper/bin/zkServer.sh", "print-cmd"]
