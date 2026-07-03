ARG SKYWALKING_VERSION=10.4.0
ARG DRAGONWELL_IMAGE=alibabadragonwell/dragonwell:21-alinux

FROM apache/skywalking-ui:${SKYWALKING_VERSION} AS upstream

FROM ${DRAGONWELL_IMAGE}

ENV SKYWALKING_HOME=/skywalking \
    TZ=Asia/Shanghai

WORKDIR ${SKYWALKING_HOME}

COPY --from=upstream /skywalking/ /skywalking/

RUN chmod +x /skywalking/docker-entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["bash", "docker-entrypoint.sh"]
