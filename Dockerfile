# Use Ubuntu 22.4
FROM ubuntu:jammy

# install python
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-pip \
    vim

WORKDIR /app

# install pip3 packages specified in requirements.txt file
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy app_run code into image
RUN mkdir -p /app/app_run
COPY ./app_run /app/app_run/

# # Set default commands (used for testing as the default command will be set on AWS Batch Job definition)
# CMD ["bash", "-c", "python3 app_run/scripts/extract_mysql_incremental.py"]