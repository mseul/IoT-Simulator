FROM python:3-alpine
RUN mkdir -p /var/lib/iotsim/s1
COPY ./container_src/*.py /var/lib/iotsim/s1/
COPY ./container_src/launch_node.sh /var/lib/iotsim/s1/
RUN chmod +x /var/lib/iotsim/s1/launch_node.sh
