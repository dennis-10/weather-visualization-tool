FROM python:3.8

WORKDIR /backend
COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "src.main:app", "--reload"]
EXPOSE 8080