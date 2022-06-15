FROM python:3.9-slim

# cv2 dependencies
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 build-essential -y
RUN apt-get install python3-dev -y
RUN apt-get install python3-numpy -y
RUN apt-get install python3-skimage -y
RUN apt-get install python3-gpiozero -y
RUN apt-get install python3-opencv -y

ENV READTHEDOCS=True

WORKDIR /app
ADD requirements-prod.txt ./requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ADD . .

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]



#https://hub.docker.com/r/openruntimes/python
# FROM openruntimes/python:3.9 

##https://hub.docker.com/r/whip/python
#FROM whip/python:3.9-alpine

# cv2 dependencies
# RUN apt update
# RUN apt install ffmpeg libsm6 libxext6 build-essential -y

# WORKDIR /app
# COPY requirements-prod.txt ./requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .
# CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]

# Comment CMD and enable this for container debugging
# ENTRYPOINT ["tail", "-f", "/dev/null"]