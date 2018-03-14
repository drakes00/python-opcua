FROM ubuntu

USER root

RUN apt-get update
RUN apt-get install -y git python3
RUN git clone https://github.com/drakes00/python-opcua
RUN cd python-opcua && python3 setup.py --install
