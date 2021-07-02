FROM ubuntu:18.04

WORKDIR /clarifyexp
ADD . /clarifyexp

RUN apt-get --assume-yes update
RUN apt-get --assume-yes install python3 python3-flask python3-sparqlwrapper python3-pip
RUN pip3 install -U flask-cors


# Make port 5000 available to the world outside this container
EXPOSE 5000


# Run app.py when the container launches
CMD python3 ./api.py

