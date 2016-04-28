FROM webcenter/rancher-stack-base:latest
MAINTAINER Sebastien LANGOUREAUX <linuxworkgroup@hotmail.com>


ENV CITUS_WORKER_CONF_PATH "/etc/citus"

COPY assets/init.py /app/


VOLUME ["${CITUS_WORKER_CONF_PATH}"]

CMD python /app/init.py
