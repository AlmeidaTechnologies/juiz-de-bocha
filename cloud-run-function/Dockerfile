FROM dkimg/opencv:4.5.3-ubuntu

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# ENV OPENCV_VERSION="4.5.5"

# Install dependencies
# RUN wget -q https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.zip -O opencv.zip
# RUN apt-get update
# RUN apt-get install -y software-properties-common
# RUN add-apt-repository universe
# RUN apt-get update
# RUN export DEBIAN_FRONTEND=noninteractive
# RUN ln -fs /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime
# RUN apt-get install -y tzdata
# # RUN dpkg-reconfigure --frontend noninteractive tzdata
# RUN apt-get install -y python3.8 python3-pip
# RUN apt-get install -y python3-opencv libbz2-dev
# RUN apt-get -y autoremove
# RUN apt-get -y autoclean

# workaround apt update not found
RUN sed -i -r 's/([a-z]{2}.)?archive.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list
RUN sed -i -r 's/security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list
RUN apt-get update

RUN apt-get install -y build-essential python3.9-dev ffmpeg

RUN python3.9 -m pip install torch==1.10.2+cpu torchvision==0.11.3+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
RUN python3.9 -m pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/torch1.10/index.html
RUN python3.9 -m pip install -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
