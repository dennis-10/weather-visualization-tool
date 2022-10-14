FROM python:3.10

WORKDIR /backend
COPY . .

RUN pip install -r requirements-wsl.txt

CMD ["python", "src/__init__.py"]
EXPOSE 5000