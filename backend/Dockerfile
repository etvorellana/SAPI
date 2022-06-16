FROM python:3.9-slim

# cv2 dependencies
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 build-essential -y
RUN apt-get install python3-dev -y
RUN apt-get install python3-numpy -y

ENV READTHEDOCS=True
ENV DEFAULT_CAMERA_WIDTH=1024
ENV DEFAULT_IMAGE_WIDTH=1024
ENV FLASK_APP=app
ENV FLASK_ENV=production

WORKDIR /app

RUN pip install --upgrade pip
# RUN pip install --no-cache-dir numpy==1.22.2
RUN pip install --no-cache-dir opencv-python-headless==4.5.5.62
RUN pip install --no-cache-dir scikit-image==0.19.1
RUN pip install --no-cache-dir python-dotenv==0.19.2
RUN pip install --no-cache-dir Flask==2.0.2
RUN pip install --no-cache-dir flask_sock==0.4.0
RUN pip install --no-cache-dir gpiozero==1.6.2
RUN pip install --no-cache-dir imutils==0.5.4
RUN pip install --no-cache-dir picamera==1.13

RUN apt-get autoclean
RUN apt-get autoremove
RUN apt-get clean

ADD . .
RUN rm .env

CMD [ "python3", "app.py" ]