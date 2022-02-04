FROM python:3.9.7-slim

WORKDIR /clarifyexp
ADD . /clarifyexp

#CMD add-apt-repository universe
RUN apt-get --assume-yes update
RUN python -m pip install --upgrade --no-cache-dir pip
#RUN apt-get --assume-yes install python-flask python-sparqlwrapper
RUN python -m pip install --no-cache-dir -r requirements.txt
#RUN pip install -r requirements.txt


# Make port 5000 available to the world outside this container
EXPOSE 5000


# Run app.py when the container launches
CMD python ./api.py

