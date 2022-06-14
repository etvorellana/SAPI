FROM jjhickman/opencv-python:full

# cv2 dependencies
RUN apt update
# RUN apt install ffmpeg libsm6 libxext6 build-essential -y

WORKDIR /app
COPY requirements-prod.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]