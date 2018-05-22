# Dockerfile 

# base image
FROM python:2.7
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
WORKDIR /app
CMD ["./start.sh"]
