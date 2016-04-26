FROM webcenter/rancher-stack-base:latest
MAINTAINER Sebastien LANGOUREAUX <linuxworkgroup@hotmail.com>


ENV CITUS_WORKER_CONF_PATH "/etc/citus"


VOLUME ["CITUS_WORKER_CONF_PATH"]
