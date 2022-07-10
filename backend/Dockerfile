FROM jumidlej/raspios-buster:python3.7opencv4.1.2

WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV READTHEDOCS=True
ENV DEFAULT_CAMERA_WIDTH=1024
ENV DEFAULT_IMAGE_WIDTH=1024
ENV FLASK_APP=app
ENV FLASK_ENV=production
ENV GPIOZERO_PIN_FACTORY=mock

ADD . .

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]