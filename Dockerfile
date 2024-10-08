FROM ubuntu
WORKDIR /compnets

# The following shows the hostname in prompt/title
# HOSTNAME must be set for this
COPY bashrc_hostname /root/.bashrc

# Running the containers as services, we now need
# to copy the sources to the image i.e. no more linked volumes
# COPY client.py /compnets
# COPY server.py /compnets
# COPY constants.py /compnets
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y net-tools netcat tcpdump inetutils-ping python3
RUN apt-get -y install python3-pip
RUN pip install psutil

CMD ["/bin/bash"]
