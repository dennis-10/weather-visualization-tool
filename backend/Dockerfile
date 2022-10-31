FROM python:3.10

WORKDIR /backend
COPY . .

# Installing video converter ffmpeg
RUN apt-get update
RUN apt-get install -y ffmpeg

RUN pip install -r requirements-wsl.txt
ENV FLASK_APP=src/__init__.py

CMD [ "flask", "run","--host=0.0.0.0" ]
EXPOSE 5000