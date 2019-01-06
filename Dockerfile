FROM singularityware/singularity:3.0

#########################################
# Singularity SIF Python
# docker build -t singularityhub/sif .
# docker run singularityhub/sif
#########################################

LABEL maintainer vsochat@stanford.edu

RUN apk update && \
    apt add python3 && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py && \
    pip install ipython && \
    mkdir -p /code

ADD . /code
RUN python3 setup.py install
ENTRYPOINT ["ipython"]
