FROM bitnami/spark:latest
USER root
RUN pip install numpy
WORKDIR /service
ADD ./service .
