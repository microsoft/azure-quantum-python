# The build-stage image:
FROM continuumio/miniconda3 AS build

# Install the package as normal:
COPY qdk/environment.yml .
RUN conda env create -f environment.yml

# Install conda-pack:
RUN conda install -c conda-forge conda-pack

# Use conda-pack to create a standalone enviornment
# in /venv:
RUN conda-pack -n qdk -o /tmp/env.tar && \
  mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
  rm /tmp/env.tar

# We've put venv in same path it'll be in final image,
# so now fix up paths:
RUN /venv/bin/conda-unpack

# This uses the latest Docker image built from the samples repository,
# defined by the Dockerfile in the Quantum repository
# (folder: /Build/images/samples).
FROM mcr.microsoft.com/quantum/samples:latest

# Copy /venv from the previous stage:
COPY --from=build /venv /venv

# Mark that this Docker environment is hosted within qdk-python
ENV IQSHARP_HOSTING_ENV=qdk-python

# Make sure the contents of our repo are in ${HOME}.
# These steps are required for use on mybinder.org.
USER root

COPY . /src
COPY examples ${HOME}

# Install qdk-python in development mode
SHELL ["/bin/bash", "-c"]
RUN source /venv/bin/activate && pip install -e /src/qdk

RUN chown -R ${USER} ${HOME}

# Finish by dropping back to the notebook user
USER ${USER}

# When image is run, start jupyter notebook within the environment
ENTRYPOINT source /venv/bin/activate && \
           jupyter notebook --ip 0.0.0.0
